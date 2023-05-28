from engine.fragment.directory import FunctionExport
from engine.fragment.fragment import Fragment, FragmentCall
from minecraft.command.argument.resource_location import ResourceLocation
from minecraft.command.base import Command, SubCommand
from minecraft.command.command.execute import ExecuteCommand, ExecuteConditionCommand
from minecraft.command.command.function import FunctionCommand
from minecraft.datapack.function import Function

UNDEFINED = -1
DISCARD = 0
EMBED = 1
EXPORT = 2
INLINE = 3
FORCE = 4


def exportFunctions():
    return list(Solver().solve())


class FragmentNode:
    fragment: Fragment
    to_: set[FragmentCall]
    from_: set[FragmentCall]
    export: int
    reachable: bool
    location: ResourceLocation

    def __init__(self, fragment) -> None:
        self.fragment = fragment
        self.from_ = set()
        self.to_ = set()
        self.export = UNDEFINED
        self.reachable = False


class Solver:
    def __init__(self) -> None:
        self.fragmentMap: dict[Fragment, FragmentNode] = {
            fragment: FragmentNode(fragment) for fragment in Fragment.fragements
        }

        for call in FragmentCall.calls:
            self.fragmentMap[call.from_].to_.add(call)
            self.fragmentMap[call.to_].from_.add(call)

    def define_node_export_state(self, node: FragmentNode):
        """
        ノードの出力設定の決定
        一つのノードに対して何回も呼ばれる
        """
        # 必ず破棄/出力する設定の場合無視
        if node.export in {DISCARD, FORCE}:
            return

        if node.fragment.location is not None:
            # locationが設定されている場合export=FORCE
            node.export = FORCE
            return

        command_count = len(node.fragment.commands)
        from_count = len(node.from_)

        if command_count == 0:
            # コマンドがない場合削除
            node.export = DISCARD
            return

        if from_count == 0:
            # 呼び出し元がない場合削除
            node.export = DISCARD
            return

        if command_count == 1:
            if isinstance(node.fragment.commands[0], Command):
                # 1つのコマンドしかない場合はインライン埋め込み
                node.export = INLINE
                return

        if from_count >= 2:
            # 呼び出し元が複数ある場合はexport=EXPORT
            node.export = EXPORT
            return

        [from_call] = node.from_

        if len(from_call.subcommands) == 0:
            if all(map(lambda x: isinstance(x, Command), node.fragment.commands)):
                # 呼び出しにサブコマンドがなく、CallFragmentもない場合埋め込み
                node.export = EMBED
                return

        # それ以外の場合は出力
        node.export = EXPORT

    def resolve_discarded(self, node: FragmentNode):
        if node.export in {DISCARD, EMBED, INLINE}:
            self.modified = True
            # EMBED/DISCARD/INLINEなノードをfragmentMapから削除
            self.fragmentMap.pop(node.fragment)
            return

        commands: list[Command | FragmentCall] = []

        for cmd in node.fragment.commands:
            if isinstance(cmd, Command):
                commands.append(cmd)
                continue

            to_node = self.fragmentMap[cmd.to_]

            # UNDEFINED EXPORT FORCE はそのまま
            if to_node.export not in {INLINE, EMBED, DISCARD}:
                commands.append(cmd)
                continue

            self.modified = True

            # 呼び出し先の登録を解除
            node.to_.remove(cmd)

            # DISCARDを削除
            if to_node.export == DISCARD:
                continue

            # EMBEDを埋め込む
            if to_node.export == EMBED:
                assert len(cmd.subcommands) == 0
                commands.extend(to_node.fragment.commands)
                continue

            # INLINEを埋め込む
            if to_node.export == INLINE:
                to_cmd = to_node.fragment.commands[0]
                match to_cmd:
                    case ExecuteCommand():
                        new_cmd = ExecuteCommand([*cmd.subcommands, *to_cmd.sub_commands], to_cmd.command)
                    case ExecuteConditionCommand():
                        new_cmd = ExecuteConditionCommand([*cmd.subcommands, *to_cmd.sub_commands], to_cmd.condition)
                    case Command():
                        new_cmd = ExecuteCommand(cmd.subcommands, to_cmd)
                    case FragmentCall():
                        raise AssertionError
                commands.append(new_cmd)

    def mark_reachable(self, node: FragmentNode):
        """ノードが到達可能であることをマークし、子ノードも到達可能として再帰的にマークする"""
        if node.reachable:
            return

        node.reachable = True
        for to_ in node.to_:
            self.mark_reachable(self.fragmentMap[to_.to_])

    def reflesh_reachablity(self):
        # 全ノードを到達不可の状態でリセット
        for node in self.fragmentMap.values():
            node.reachable = False

        # FORCEのノードから到達可能性を再帰的に確認
        for node in self.fragmentMap.values():
            if node.export == FORCE:
                self.mark_reachable(node)

        # 到達不可のノードの出力設定をDISCARDに
        for node in self.fragmentMap.values():
            if not node.reachable:
                node.export = DISCARD

    def loop(self):
        """すべてのノードの出力状態が決定するまで繰り返す内容"""
        self.modified = False

        # 出力状態の更新
        for node in self.fragmentMap.values():
            self.define_node_export_state(node)

        # FORCEなFragmentから到達できるかのチェック
        self.reflesh_reachablity()

        # 破棄の反映
        for node in self.fragmentMap.values():
            self.resolve_discarded(node)

    def solve(self):
        self.modified = True
        while self.modified:
            self.loop()

        return self.gen_functions()

    def gen_functions(self):
        for node in self.fragmentMap.values():
            assert node.export in {EXPORT, FORCE}
            node.location = node.fragment.location or FunctionExport.provide()

        return map(self.gen_function, self.fragmentMap.values())

    def gen_function(self, node: FragmentNode):
        commands: list[Command] = []

        for cmd in node.fragment.commands:
            if isinstance(cmd, Command):
                commands.append(cmd)
                continue

            to_node = self.fragmentMap[cmd.to_]
            new_cmd = FunctionCommand(to_node.location)
            if len(cmd.subcommands) > 0:
                new_cmd = ExecuteCommand(cmd.subcommands, new_cmd)
            commands.append(new_cmd)
            continue

        return Function(node.location, commands)
