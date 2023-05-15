from __future__ import annotations
from dataclasses import dataclass, field
import dataclasses
from typing import ClassVar, Generic, Literal, TypeVar, overload
from core.command.argument.nbt_tag import NbtCompoundTag
from core.command.argument.resource_location import ResourceLocation
from core.command.base import Argument


Gamemode = Literal["survival", "creative", "adventure", "spectator"]
Sort = Literal["arbitrary", "random", "nearest", "furthest"]
Advancements = dict[ResourceLocation, bool | dict[str, bool]]

N = TypeVar("N", bound=int | float)
SELF = TypeVar("SELF", bound="IRange")

INTMAX = 2**31 - 1


class IRange(Generic[N]):
    MAX: N
    MIN: N

    def __init__(self, value: N | tuple[N | None, N | None]) -> None:
        match value:
            case (min, max):
                self.min = self.MIN if min is None else min
                self.max = self.MAX if max is None else max
            case _:
                self.min = value
                self.max = value
        assert self.MIN <= self.min <= self.MAX
        assert self.MIN <= self.max <= self.MAX

    def union(self: SELF, other: SELF) -> SELF:
        vmin = max(self.min, other.min)
        vmax = min(self.max, other.max)
        assert vmin <= vmax
        return self.__class__((vmin, vmax))

    @property
    def tostr(self):
        if self.min == self.max:
            return str(self.min)
        if self.min == self.MIN:
            return f"..{self.max}"
        if self.max == self.MAX:
            return f"{self.min}.."
        return f"{self.min}..{self.max}"


class IntRange(IRange[int]):
    MAX = INTMAX
    MIN = -(2**31)


class FloatRange(IRange[float]):
    MAX: float = float("infinity")
    MIN: float = -float("infinity")


@dataclass
class TargetSelector(Argument):
    _selector: Literal["self", "player", "entity"]
    _sort: Sort | None = None
    _limit: int | None = INTMAX

    _name: str | None = None
    _gamemode: Gamemode | None = None
    _teams: dict[str, bool] | bool = field(default_factory=dict)
    _types: dict[str, bool] = field(default_factory=dict)
    _tags: dict[str, bool] | bool = field(default_factory=dict)
    _nbt: NbtCompoundTag | None = None
    _scores: dict[str, IntRange] = field(default_factory=dict)
    _advancements: Advancements = field(default_factory=dict)
    _predicates: dict[ResourceLocation, bool] = field(default_factory=dict)
    _x_rotation: IntRange | None = None
    _y_rotation: IntRange | None = None
    _level: IntRange | None = None
    _x: float | None = None
    _y: float | None = None
    _z: float | None = None
    _dx: float | None = None
    _dy: float | None = None
    _dz: float | None = None
    _distance: FloatRange | None = None

    @overload
    def _replace(self) -> TargetSelector:
        pass

    @overload
    def _replace(
        self,
        *,
        _name: str | None = None,
        _gamemode: Gamemode | None = None,
        _teams: dict[str, bool] | bool | None = None,
        _types: dict[str, bool] | None = None,
        _tags: dict[str, bool] | bool | None = None,
        _nbt: NbtCompoundTag | None = None,
        _scores: dict[str, IntRange] | None = None,
        _advancements: Advancements | None = None,
        _predicates: dict[ResourceLocation, bool] | None = None,
        _x_rotation: FloatRange | None = None,
        _y_rotation: FloatRange | None = None,
        _level: IntRange | None = None,
        _x: float | None = None,
        _y: float | None = None,
        _z: float | None = None,
        _dx: float | None = None,
        _dy: float | None = None,
        _dz: float | None = None,
        _distance: FloatRange | None = None,
        _sort: Sort | None = None,
        _limit: int | None = None,
    ) -> TargetSelector:
        pass

    def _replace(self, **kwarg):
        return dataclasses.replace(self, **kwarg)

    def isSingle(self):
        """セレクターが単一エンティティを指しているか"""
        if self._selector == "self":
            return True
        return self._limit == 1

    @property
    def argument_str(self) -> str:
        selectors: list[tuple[str, str]] = []

        if self._name is not None:
            selectors.append(("name", self._name))

        if self._gamemode is not None:
            selectors.append(("gamemode", self._gamemode))

        match (self._teams):
            case bool():
                selectors.append(("team", "" if self._teams else "!"))
            case dict():
                for k, v in self._teams.items():
                    selectors.append(("team", ("" if v else "!") + k))

        for k, v in self._types.items():
            selectors.append(("type", ("" if v else "!") + k))

        match (self._tags):
            case bool():
                selectors.append(("tag", "" if self._teams else "!"))
            case dict():
                for k, v in self._tags.items():
                    selectors.append(("tag", ("" if v else "!") + k))

        if self._nbt is not None:
            selectors.append(("nbt", self._nbt.argument_str))

        if self._scores:
            scores = "{" + ",".join(k + "=" + v.tostr for k, v in self._scores.items()) + "}"
            selectors.append(("scores", scores))

        if self._advancements:
            advancements = (
                "{"
                + ",".join(
                    k.argument_str
                    + "="
                    + (
                        "true"
                        if v
                        else "false"
                        if isinstance(v, bool)
                        else ("{" + ",".join(vk + "=" + "true" if vv else "false" for vk, vv in v.items()) + "}")
                    )
                    for k, v in self._advancements.items()
                )
                + "}"
            )
            selectors.append(("advancements", advancements))

        for k, v in self._predicates.items():
            selectors.append(("type", ("" if v else "!") + k.argument_str))

        if self._x_rotation is not None:
            selectors.append(("x_rotation", self._x_rotation.tostr))

        if self._y_rotation is not None:
            selectors.append(("y_rotation", self._y_rotation.tostr))

        if self._level is not None:
            selectors.append(("level", self._level.tostr))

        if self._x is not None:
            selectors.append(("x", str(self._x)))
        if self._y is not None:
            selectors.append(("y", str(self._y)))
        if self._z is not None:
            selectors.append(("z", str(self._z)))

        if self._dx is not None:
            selectors.append(("dx", str(self._dx)))
        if self._dy is not None:
            selectors.append(("dy", str(self._dy)))
        if self._dz is not None:
            selectors.append(("dz", str(self._dz)))

        if self._distance is not None:
            selectors.append(("distance", self._distance.tostr))

        match (self._selector, self._sort, self._limit):
            case ("self", None, None):
                selector = "s"
            case ("entity", str() as sort, int() as limit):
                if sort != "arbitrary":
                    selectors.append(("sort", sort))
                if limit != INTMAX:
                    selectors.append(("limit", str(limit)))
                selector = "e"
            case ("player", "nearest", 1):
                selector = "p"
            case ("player", "ramdom", 1):
                selector = "r"
            case ("player", str() as sort, int() as limit):
                if sort != "arbitrary":
                    selectors.append(("sort", sort))
                if limit != INTMAX:
                    selectors.append(("limit", str(limit)))
                selector = "a"
            case e:
                raise ValueError(e)

        if selectors:
            return "@" + selector + "[" + ",".join(k + "=" + v for k, v in selectors) + "]"
        return "@" + selector

    s: ClassVar[TargetSelector]
    e: ClassVar[TargetSelector]
    p: ClassVar[TargetSelector]
    r: ClassVar[TargetSelector]
    a: ClassVar[TargetSelector]

    def name(self, name: str | None):
        if self._name is not None:
            raise ValueError
        return self._replace(_name=name)

    def gamemode(self, gamemode: Gamemode | None):
        if self._gamemode is not None:
            raise ValueError
        return self._replace(_gamemode=gamemode)

    def team_any(self, enable: bool):
        if self._teams != {}:
            raise ValueError
        return self._replace(_teams=enable)

    def team(self, team: str, enable=True):
        if isinstance(self._teams, bool):
            raise ValueError
        if team in self._teams:
            raise ValueError
        return self._replace(_teams=self._teams | {team: enable})

    def type(self, type: str, enable=True):
        if type in self._types:
            raise ValueError
        return self._replace(_types=self._types | {type: enable})

    def tag_any(self, enable: bool):
        if self._tags != {}:
            raise ValueError
        return self._replace(_tags=enable)

    def tag(self, tag: str, enable=True):
        if isinstance(self._tags, bool):
            raise ValueError
        if tag in self._tags:
            raise ValueError
        return self._replace(_tags=self._tags | {tag: enable})

    # TODO: NBTのマージ
    def nbt(self, value: NbtCompoundTag | None):
        if self._nbt is not None:
            raise ValueError
        return self._replace(_nbt=value)

    def score(self, holder: str, value: int | tuple[int | None, int | None]):
        v = IntRange(value)
        if holder in self._scores:
            v = self._scores[holder].union(v)
        return self._replace(_scores=self._scores | {holder: v})

    def advancement(self, advancement: ResourceLocation, state: bool | dict[str, bool]):
        if advancement in self._advancements:
            raise ValueError
        return self._replace(_advancements=self._advancements | {advancement: state})

    def predicate(self, predicate: ResourceLocation, enable: bool):
        if predicate in self._predicates:
            raise ValueError
        return self._replace(_predicates=self._predicates | {predicate: enable})

    def rotation(
        self, x: float | tuple[float | None, float | None] | None, y: float | tuple[float | None, float | None] | None
    ):
        if x is not None:
            if self._x_rotation is not None:
                raise ValueError
            self = self._replace(_x_rotation=FloatRange(x))
        if y is not None:
            if self._y_rotation is not None:
                raise ValueError
            self = self._replace(_y_rotation=FloatRange(y))
        return self

    def level(self, level: int | tuple[int | None, int | None]):
        v = IntRange(level)
        if self._level is not None:
            v = self._level.union(v)
        return self._replace(_level=v)

    def xyz(self, x: float | None, y: float | None, z: float | None):
        if x is not None:
            if self._x is not None:
                raise ValueError
            self = self._replace(_x=x)
        if y is not None:
            if self._y is not None:
                raise ValueError
            self = self._replace(_y=y)
        if z is not None:
            if self._z is not None:
                raise ValueError
            self = self._replace(_z=z)
        return self

    def dxyz(self, dx: float | None, dy: float | None, dz: float | None):
        if dx is not None:
            if self._dx is not None:
                raise ValueError
            self = self._replace(_dx=dx)
        if dy is not None:
            if self._dy is not None:
                raise ValueError
            self = self._replace(_dy=dy)
        if dz is not None:
            if self._dz is not None:
                raise ValueError
            self = self._replace(_dz=dz)
        return self

    def distance(self, distance: float | tuple[float | None, float | None]):
        v = FloatRange(distance)
        if self._distance is not None:
            v = self._distance.union(v)
        return self._replace(_distance=v)

    # sortは上書き可能
    def sort(self, sort: Sort):
        if self._selector == "self":
            raise ValueError("sort has no effect for @s selector")
        return self._replace(_sort=sort)

    # limitは小さいほうに上書き可能
    def limit(self, limit: int):
        if self._selector == "self":
            raise ValueError("limit has no effect for @s selector")
        assert self._limit is not None
        if limit > self._limit:
            raise ValueError("limitの値をもとより小さくすることはできません")
        return self._replace(_limit=limit)


TargetSelector.s = TargetSelector("self", _sort=None, _limit=None)

TargetSelector.a = TargetSelector("player", _sort="arbitrary", _limit=INTMAX)

TargetSelector.p = TargetSelector("player", _sort="nearest", _limit=1)

TargetSelector.r = TargetSelector("player", _sort="random", _limit=1)

TargetSelector.e = TargetSelector("entity", _sort="arbitrary")
