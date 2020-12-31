import os.path
from objects import Battle
from typing import List, Union, Tuple, Callable
import gzip
import ujson
import json
import zlib
from core import hasBattles, getValMultiDimensional


def filterBattles(
    location, data, filterFunctions: List[Callable], outpath, mode=""
) -> Union[Tuple[str, str], Tuple[List[bytes], List[bytes]]]:
    if location == "disk":
        if not (
            os.path.exists(data[0:-6] + "/" + outpath + ".jl.gz")
            and os.path.exists(data[0:-6] + "/not" + outpath + ".jl.gz")
        ):
            with gzip.open(data) as reader:
                if hasBattles("disk", data):
                    with gzip.open(
                        data[0:-6] + "/" + outpath + ".jl.gz",
                        "at",
                        encoding="utf8",
                    ) as writerA:
                        with gzip.open(
                            data[0:-6] + "/not" + outpath + ".jl.gz",
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
            data[0:-6] + "/" + outpath + ".jl.gz",
            data[0:-6] + "/not" + outpath + ".jl.gz",
        )
    jobsWith: List[bytes] = []
    jobsWithout: List[bytes] = []
    for line in data:
        battle = Battle(**ujson.loads(zlib.decompress(line)))
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
            jobsWith.append(line)
        else:
            jobsWithout.append(line)
    return (jobsWith, jobsWithout)


def filterBattlesCondition(location, data, attribute, values, comparison, mode):
    filterFunctions: List[Callable] = []
    outPath = ""
    for attribute in attributes:
        outPath += str(attribute)
    for val in values:
        outPath += str(val)
        filterFunctions = (
            lambda battle=battle, val=val, attribute=attribute: getValMultiDimensional(
                battle, attribute
            )
            == val
        )
    return filterBattles(location, data, filterFunctions, outPath, mode)
