import os.path
from objects import Battle, Player
from typing import List, Union, Tuple, Callable, cast
import gzip
import ujson
import json
import zlib
import ciso8601
from core import hasBattles, getValMultiDimensional


def filterBattles(
    location,
    data: Union[str, List[bytes]],
    filterFunctions: List[Callable],
    outpath,
    mode="",
) -> Union[Tuple[str, str], Tuple[List[bytes], List[bytes]]]:
    if location == "disk":
        if not (
            os.path.exists(cast(str, data[:-6]) + "/" + outpath + ".jl.gz")
            and os.path.exists(cast(str, data[:-6]) + "/not" + outpath + ".jl.gz")
        ):
            with gzip.open(cast(str, data), "rt") as reader:
                if hasBattles("disk", data):
                    with gzip.open(
                        cast(str, data[:-6]) + "/" + outpath + ".jl.gz",
                        "at",
                        encoding="utf8",
                    ) as writerA:
                        with gzip.open(
                            cast(str, data[:-6]) + "/not" + outpath + ".jl.gz",
                            "at",
                            encoding="utf8",
                        ) as writerB:
                            for line in reader:
                                battle = Battle(**ujson.loads(line))
                                if mode == "and":
                                    filterCondition = True
                                    for funct in filterFunctions:
                                        filterCondition = filterCondition and funct(
                                            battle
                                        )
                                elif mode == "or":
                                    filterCondition = False
                                    for funct in filterFunctions:
                                        filterCondition = filterCondition or funct(
                                            battle
                                        )
                                else:
                                    filterCondition = filterFunctions[0](battle)
                                if filterCondition:
                                    writerA.write(line)
                                    writerA.write("\n")
                                else:
                                    writerB.write(line)
                                    writerB.write("\n")
        return (
            cast(str, data[:-6]) + "/" + outpath + ".jl.gz",
            cast(str, data[:-6]) + "/not" + outpath + ".jl.gz",
        )
    jobsWith: List[bytes] = []
    jobsWithout: List[bytes] = []
    for battleLine in cast(List[bytes], data):
        battle = Battle(**ujson.loads(zlib.decompress(battleLine)))
        if mode == "and":
            filterCondition = True
            for funct in filterFunctions:
                filterCondition = filterCondition and funct(battle)
        elif mode == "or":
            filterCondition = False
            for funct in filterFunctions:
                filterCondition = filterCondition or funct(battle)
        else:
            filterCondition = filterFunctions[0](battle)
        if filterCondition:
            jobsWith.append(battleLine)
        else:
            jobsWithout.append(battleLine)
    return (jobsWith, jobsWithout)


def filterBattlesCondition(
    location, data: Union[str, List[bytes]], attribute, values, comparison, mode=""
):
    filterFunctions: List[Callable] = []
    try:
        os.mkdir(cast(str, data[:-6]))
    except FileExistsError:
        pass
    outPath = ""
    for attr in attribute:
        outPath += str(attr)
    for val in values:
        outPath += str(val)
        if comparison == ">":
            filterFunctions.append(
                lambda battle, val=val, attribute=attribute: getValMultiDimensional(
                    battle, attribute
                )
                > val
            )
        elif comparison == "<":
            filterFunctions.append(
                lambda battle, val=val, attribute=attribute: getValMultiDimensional(
                    battle, attribute
                )
                < val
            )
        elif comparison == "!=":
            filterFunctions.append(
                lambda battle, val=val, attribute=attribute: getValMultiDimensional(
                    battle, attribute
                )
                != val
            )
        elif comparison == "<=":
            filterFunctions.append(
                lambda battle, val=val, attribute=attribute: getValMultiDimensional(
                    battle, attribute
                )
                <= val
            )
        elif comparison == ">=":
            filterFunctions.append(
                lambda battle, val=val, attribute=attribute: getValMultiDimensional(
                    battle, attribute
                )
                >= val
            )
        else:
            filterFunctions.append(
                lambda battle, val=val, attribute=attribute: getValMultiDimensional(
                    battle, attribute
                )
                == val
            )
    return filterBattles(location, data, filterFunctions, outPath, mode)


def filterStage(
    location, data: Union[str, List[bytes]], stages: List[str]
) -> Union[Tuple[str, str], Tuple[List[bytes], List[bytes]]]:
    return filterBattlesCondition(location, data, ["map", "key"], stages, "=", "or")


def filterMode(
    location, data: Union[str, List[bytes]], modes: List[str]
) -> Union[Tuple[str, str], Tuple[List[bytes], List[bytes]]]:
    return filterBattlesCondition(location, data, ["mode", "key"], modes, "=", "or")


def filterRule(
    location, data: Union[str, List[bytes]], rules: List[str]
) -> Union[Tuple[str, str], Tuple[List[bytes], List[bytes]]]:
    return filterBattlesCondition(location, data, ["rule", "key"], rules, "=", "or")


def filterWeapon(
    location, data: Union[str, List[bytes]], weapons: List[str]
) -> Union[Tuple[str, str], Tuple[List[bytes], List[bytes]]]:
    return filterBattlesCondition(location, data, ["weapon", "key"], weapons, "=", "or")


def filterWeaponType(
    location, data: Union[str, List[bytes]], weaponType: List[str]
) -> Union[Tuple[str, str], Tuple[List[bytes], List[bytes]]]:
    return filterBattlesCondition(
        location, data, ["weapon", "type", "key"], weaponType, "=", "or"
    )


def filterWeaponCategory(
    location, data: Union[str, List[bytes]], weaponCategory: List[str]
) -> Union[Tuple[str, str], Tuple[List[bytes], List[bytes]]]:
    return filterBattlesCondition(
        location, data, ["weapon", "type", "category", "key"], weaponCategory, "=", "or"
    )


def filterWeaponMainRef(
    location, data: Union[str, List[bytes]], weaponMainRef: List[str]
) -> Union[Tuple[str, str], Tuple[List[bytes], List[bytes]]]:
    return filterBattlesCondition(
        location, data, ["weapon", "main_ref"], weaponMainRef, "=", "or"
    )


def filterRank(
    location, data: Union[str, List[bytes]], ranks: List[str]
) -> Union[Tuple[str, str], Tuple[List[bytes], List[bytes]]]:
    filterFunctions: List[Callable] = []
    try:
        os.mkdir(cast(str, data[:-6]))
    except FileExistsError:
        pass
    outPath = "rank"
    for rank in ranks:
        outPath += rank
        filterFunctions.append(
            lambda battle, rank=rank: getValMultiDimensional(
                battle,
                [
                    "user",
                    "stats",
                    "v2",
                    "gachi",
                    "rules",
                    getValMultiDimensional(battle, ["rule", "key"])
                    if getValMultiDimensional(battle, ["rule", "key"]) != "nawabari"
                    else "none",
                    "rank_current",
                ],
            )
            == rank
        )
    return filterBattles(location, data, filterFunctions, outPath, "or")


def filterWinLoss(
    location, data: Union[str, List[bytes]]
) -> Union[Tuple[str, str], Tuple[List[bytes], List[bytes]]]:
    return filterBattlesCondition(location, data, ["result"], ["win"], "=")


def filterWithPlayers(
    location, data: Union[str, List[bytes]], players: List[str], mode
) -> Union[Tuple[str, str], Tuple[List[bytes], List[bytes]]]:
    try:
        os.mkdir(cast(str, data[:-6]))
    except FileExistsError:
        pass
    outPath = "withPlayers"
    filterFunctions: List[Callable] = []
    for player in players:
        filterFunctions.append(
            lambda battle, player=player: any(
                val.splatnet_id == player and val.team == "my"
                for val in (getValMultiDimensional(battle, ["players"]))
            )
        )
        outPath += player + mode
    return filterBattles(location, data, filterFunctions, outPath, mode)


def filterAgainstPlayers(
    location, data: Union[str, List[bytes]], players: List[str], mode
) -> Union[Tuple[str, str], Tuple[List[bytes], List[bytes]]]:
    try:
        os.mkdir(cast(str, data[:-6]))
    except FileExistsError:
        pass
    outPath = "againstPlayers"
    filterFunctions: List[Callable] = []
    for player in players:
        filterFunctions.append(
            lambda battle, player=player: any(
                val.splatnet_id == player and val.team == "his"
                for val in (getValMultiDimensional(battle, ["players"]))
            )
        )
        outPath += player + mode
    return filterBattles(location, data, filterFunctions, outPath, mode)


def filterIncludesPlayers(
    location, data: Union[str, List[bytes]], players: List[str], mode
) -> Union[Tuple[str, str], Tuple[List[bytes], List[bytes]]]:
    try:
        os.mkdir(cast(str, data[:-6]))
    except FileExistsError:
        pass
    outPath = "includesPlayers"
    filterFunctions: List[Callable] = []
    for player in players:
        filterFunctions.append(
            lambda battle, player=player: any(
                val.splatnet_id == player
                for val in (getValMultiDimensional(battle, ["players"]))
            )
        )
        outPath += player + mode
    return filterBattles(location, data, filterFunctions, outPath, mode)


def filterDisconnect(
    location, data: Union[str, List[bytes]]
) -> Union[Tuple[str, str], Tuple[List[bytes], List[bytes]]]:
    try:
        os.mkdir(cast(str, data[:-6]))
    except FileExistsError:
        pass
    outPath = "disconnect"
    filterFunctions: List[Callable] = [
        lambda battle: any(
            val.point == 0
            for val in (
                battle.players
                if battle.players is not None
                else [
                    Player(
                        None,
                        None,
                        None,
                        None,
                        None,
                        None,
                        None,
                        None,
                        None,
                        None,
                        None,
                        None,
                        None,
                        None,
                        None,
                        None,
                        None,
                        None,
                        None,
                        None,
                    )
                ]
            )
        )
    ]
    return filterBattles(location, data, filterFunctions, outPath)


def filterStartAtInt(
    location, data: Union[str, List[bytes]], time, comparison
) -> Union[Tuple[str, str], Tuple[List[bytes], List[bytes]]]:
    return filterBattlesCondition(
        location, data, ["start_at", "time"], [time], comparison
    )


def filterStartAtString(
    location, data: Union[str, List[bytes]], time, comparison
) -> Union[Tuple[str, str], Tuple[List[bytes], List[bytes]]]:
    return filterStartAtInt(location, data, ciso8601.parse_datetime(time), comparison)


def filterEndAtInt(
    location, data: Union[str, List[bytes]], time, comparison
) -> Union[Tuple[str, str], Tuple[List[bytes], List[bytes]]]:
    return filterBattlesCondition(
        location, data, ["end_at", "time"], [time], comparison
    )


def filterEndAtString(
    location, data: Union[str, List[bytes]], time, comparison
) -> Union[Tuple[str, str], Tuple[List[bytes], List[bytes]]]:
    return filterEndAtInt(location, data, ciso8601.parse_datetime(time), comparison)


def filterRegisterAtInt(
    location, data: Union[str, List[bytes]], time, comparison
) -> Union[Tuple[str, str], Tuple[List[bytes], List[bytes]]]:
    return filterBattlesCondition(
        location, data, ["register_at", "time"], [time], comparison
    )


def filterRegisterAtString(
    location, data: Union[str, List[bytes]], time, comparison
) -> Union[Tuple[str, str], Tuple[List[bytes], List[bytes]]]:
    return filterRegisterAtInt(
        location, data, ciso8601.parse_datetime(time), comparison
    )
