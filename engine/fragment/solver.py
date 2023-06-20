from __future__ import annotations
from dataclasses import dataclass
from enum import Enum, auto
from engine.fragment.directory import FunctionExport
from engine.fragment.fragment import Fragment, FragmentCall
from minecraft.command.argument.resource_location import ResourceLocation
from minecraft.command.base import Command, IConditionSubCommand, SubCommand
from minecraft.command.command.execute import ExecuteCommand, ExecuteConditionCommand
from minecraft.command.command.function import FunctionCommand
from minecraft.datapack.function import Function


class FragmentExportEnum(Enum):
    UNDEFINED = auto()
    FORCE = auto()


class _Node:
    pass


@dataclass
class CommandNode(_Node):
    command: Command | IConditionSubCommand


@dataclass
class FragmentNode(_Node):
    location: ResourceLocation | None
    commands: list[FragmentEdge]
    in_: set[FragmentEdge]
    reachable = False

    def __hash__(self) -> int:
        return id(self)


@dataclass
class FragmentEdge:
    subcommands: list[SubCommand]
    from_: FragmentNode
    to_: _Node

    def __hash__(self) -> int:
        return id(self)


class FragmentSolver:
    def __init__(self, fragments: list[Fragment]) -> None:
        self.roots: list[FragmentNode] = []
        """最終的にfunctionとして出力するノードのリスト。in_は必ず空集合"""

        self.fragments = fragments
        nodes = {fragment: FragmentNode(fragment.location, [], set()) for fragment in fragments}
        for fragment, node in nodes.items():
            for command in fragment.commands:
                match command:
                    case FragmentCall():
                        edge = FragmentEdge(command.subcommands, node, nodes[command.to_])
                        nodes[command.to_].in_.add(edge)
                    case ExecuteCommand():
                        cmdnode = CommandNode(command.command)
                        edge = FragmentEdge(command.sub_commands, node, cmdnode)
                    case ExecuteConditionCommand():
                        cmdnode = CommandNode(command.condition)
                        edge = FragmentEdge(command.sub_commands, node, cmdnode)
                    case Command():
                        cmdnode = CommandNode(command)
                        edge = FragmentEdge([], node, cmdnode)
                node.commands.append(edge)

        self.non_roots = set(nodes.values())

    def set_root(self, node: FragmentNode):
        """指定したノードをルートとして登録(書き出すようにする)。ノードの呼び出しはFunctionCommandに置き換えられる"""
        node.location = node.location or FunctionExport.provide()
        self.non_roots.remove(node)
        self.roots.append(node)
        for i in node.in_:
            i.to_ = CommandNode(FunctionCommand(node.location))

    def remove_node(self, node: FragmentNode):
        """指定したノードをグラフから削除。呼び出し元、呼び出し先からの参照も消える"""
        self.non_roots.remove(node)

        # 呼び出し先からの参照を削除
        for edge in node.commands:
            to_node = edge.to_
            if isinstance(to_node, FragmentNode):
                to_node.in_.remove(edge)

        # 呼び出し元からの参照を削除
        for edge in node.in_:
            edge.from_.commands.remove(edge)

    def embed(self, edge: FragmentEdge):
        """指定したEdgeを省略して子ノードの内容を親ノードに埋め込む"""
        assert len(edge.subcommands) == 0
        root_node = edge.from_
        embed_node = edge.to_
        assert isinstance(embed_node, FragmentNode)
        # 埋め込みノードを削除
        self.non_roots.remove(embed_node)

        commands: list[FragmentEdge] = []
        for e in root_node.commands:
            if e == edge:
                for sub_edge in embed_node.commands:
                    sub_edge.from_ = root_node
                    commands.append(sub_edge)
            else:
                commands.append(e)
        root_node.commands = commands

    def inline(self, node: FragmentNode):
        """指定したノード{embed_node}を親ノード{root_node}にインライン埋め込み。"""
        assert len(node.commands) == 1
        # ノードをnon_rootsから削除
        self.non_roots.remove(node)

        out_edge = node.commands[0]

        # 呼び出し先からみた呼び出し元を変更
        to_node = out_edge.to_
        if isinstance(to_node, FragmentNode):
            to_node.in_.remove(out_edge)

        for in_edge in node.in_:
            in_edge.subcommands += out_edge.subcommands

            in_edge.to_ = out_edge.to_

            # 呼び出し先からみた呼び出し元を変更
            if isinstance(to_node, FragmentNode):
                to_node.in_.add(in_edge)

    def set_named_fragments_as_root(self):
        """あらかじめlocationが設定されたFragmentをrootとして登録"""
        for node in [*self.non_roots]:
            if node.location is not None:
                self.set_root(node)

    def remove_unreachable_fragments(self):
        """rootからたどり着けないNodeを削除"""
        def mark_reachable(node: FragmentNode):
            if node.reachable:
                return
            node.reachable = True
            for edge in node.commands:
                child = edge.to_
                if isinstance(child, FragmentNode):
                    mark_reachable(child)

        # 到達可能なフラグメントにチェック
        for root in self.roots:
            mark_reachable(root)

        # 到達不能なフラグメントを削除
        for node in [*self.non_roots]:
            if not node.reachable:
                self.remove_node(node)

    def remove_empty_fragments(self):
        """空のフラグメントを削除する"""
        # 空である可能性のあるFragmentNode一覧(最初はルート以外全部)
        checklist = [*self.non_roots]
        # 唯一の呼び出し先が消えた場合も空になるのでwhileで繰り返し実行
        while checklist:
            _checklist: list[FragmentNode] = []
            for node in checklist:
                if not node.commands:
                    _checklist.extend(edge.from_ for edge in node.in_)
                    self.remove_node(node)
            checklist = _checklist

    def resolve_single_in_multi_out(self):
        """呼び出し元が一つで複数コマンドを呼び出すフラグメントを解決する"""
        # 呼び出し元が一つで複数コマンドを呼び出す可能性のあるFragmentNode一覧(最初はルート以外全部)
        checklist = [*self.non_roots]
        while checklist:
            _checklist: list[FragmentNode] = []
            for node in checklist:
                if len(node.in_) != 1:
                    continue
                if len(node.commands) <= 2:
                    continue
                # 呼び出し元が一つで複数コマンドを呼び出す場合
                in_edge, *_ = node.in_

                if in_edge.subcommands:
                    # サブコマンド付き呼びだしの場合はルートにする
                    self.set_root(node)
                    continue

                else:
                    # サブコマンドなし呼びだしの場合は埋め込む
                    self.embed(in_edge)
                    # 埋め込み元が再埋め込みできる可能性があるので_checklistに追加
                    _checklist.append(in_edge.from_)
                    continue
            checklist = _checklist

    def resolve_single_in_single_out(self):
        """呼び出し元が一つで一つだけのコマンドを呼び出すフラグメントを解決する"""
        # 一度の解決ですべて解決されるはずなのでwhileの必要なし
        for node in [*self.non_roots]:
            if len(node.in_) != 1:
                continue
            if len(node.commands) != 1:
                continue
            # 呼び出し元が一つで一つだけのコマンドを呼び出す場合インライン化
            self.inline(node)

    def resolve_multi_in(self):
        """呼び出し元が複数のフラグメントを解決する"""
        for node in [*self.non_roots]:
            # 複数コマンドある場合は出力
            if len(node.commands) >= 2:
                self.set_root(node)
                continue
            # 自分自身で再帰している場合は出力
            if any(edge.from_ == node for edge in node.in_):
                self.set_root(node)
                continue
            # 自己再帰以外の単一コマンドの場合はインライン化
            self.inline(node)

    def solve(self):
        """Fragmentの呼び出しグラフを単純化しFunction化して出力"""
        self.set_named_fragments_as_root()
        self.remove_unreachable_fragments()
        self.remove_empty_fragments()
        self.resolve_single_in_multi_out()
        self.resolve_single_in_single_out()
        self.resolve_multi_in()
        assert len(self.non_roots) == 0
        return self.gen_functions()

    def gen_functions(self):
        funcs: list[Function] = []
        for root in self.roots:
            assert root.location
            cmds: list[Command] = []
            for edge in root.commands:
                cmd = edge.to_
                assert isinstance(cmd, CommandNode)
                match cmd.command:
                    case IConditionSubCommand():
                        command = ExecuteConditionCommand(edge.subcommands, cmd.command)
                    case Command():
                        if edge.subcommands:
                            command = ExecuteCommand(edge.subcommands, cmd.command)
                        else:
                            command = cmd.command
                cmds.append(command)

            funcs.append(Function(root.location, cmds))
        return funcs
