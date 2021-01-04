import os.path
from objects import Battle
from typing import List, Union, Tuple, Callable, cast
import gzip
import ujson
import json
import zlib
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
    location, data: Union[str, List[bytes]], attribute, values, comparison, mode
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
