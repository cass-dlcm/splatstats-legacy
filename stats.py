from typing import Union, List, cast, Dict
from core import getValMultiDimensional
from objects import Battle
import numpy as np
import sys
import ujson
import zlib
import gzip
import GzipFile


def statSummary(
    location, data: Union[str, List[bytes]], stats
) -> Dict[str, Dict[str, float]]:
    """
    Find the average, min, median, and max of a stat given a data file

    :param data: str: The full file path of the data file
    :param stat: str: The stat
    :return: The resulting average, min, median, and max
    :rtype: Tuple[float, float, float, float]

    """
    if location == "disk":
        reader: Union[GzipFile, List[bytes]] = gzip.open(cast(str, data))
    else:
        reader = cast(List[bytes], data)
    statDict: Dict[str, Dict[str, Union[float, List[float]]]] = {}
    resultDict: Dict[str, Dict[str, float]] = {}
    for stat in stats:
        statDict[stat] = {
            "sum_val": 0.0,
            "max_val": 0.0,
            "min_val": sys.float_info.max,
            "vals": [],
            "count": 0.0,
        }
        resultDict[stat] = {
            "min_val": sys.float_info.max,
            "max_val": 0.0,
            "count": 0.0,
            "median": 0.0,
            "standard_deviation": 0.0,
            "mean": 0.0,
            "sum": 0.0,
        }
    for line in reader:
        if location == "disk":
            battle = Battle(**ujson.loads(line))
        else:
            battle = Battle(**ujson.loads(zlib.decompress(line)))
        for stat in statDict:
            val = float(
                getValMultiDimensional(
                    battle,
                    list(
                        map(
                            lambda ele: int(ele) if ele.isdigit() else ele, stat.split()
                        )
                    ),
                )
            )
            cast(Dict[str, float], statDict[stat])["sum_val"] += val
            cast(Dict[str, float], statDict[stat])["count"] += 1.0
            statDict[stat]["max_val"] = max(statDict[stat]["max_val"], val)
            statDict[stat]["min_val"] = min(statDict[stat]["min_val"], val)
            cast(List[float], statDict[stat]["vals"]).append(val)
    if location == "disk":
        cast(GzipFile, reader).close()
    for stat in stats:
        resultDict[stat]["min_val"] = cast(float, statDict[stat]["min_val"])
        resultDict[stat]["max_val"] = cast(float, statDict[stat]["max_val"])
        resultDict[stat]["mean"] = cast(float, statDict[stat]["sum_val"]) / cast(
            float, statDict[stat]["count"]
        )
        resultDict[stat]["standard_deviation"] = np.std(statDict[stat]["vals"])
        resultDict[stat]["median"] = np.median(statDict[stat]["vals"])
        resultDict[stat]["sum"] = cast(float, statDict[stat]["sum_val"])
        resultDict[stat]["count"] = cast(float, statDict[stat]["count"])
    return resultDict


def getArrayOfStat(
    location, data: Union[str, List[bytes]], stats: List[str]
) -> Dict[str, List[float]]:
    """
    Collect all the values of a list of stats for a given list of battles.

    :param data: the full path to the data file
    :type data: str
    :param stat: the stats to retrieve
    :type stat: List[str]
    :return: the stats for each battle in the data
    :rtype: Dict[List[float]]


    """
    if location == "disk":
        reader: Union[GzipFile, List[bytes]] = gzip.open(cast(str, data))
    else:
        reader = cast(List[bytes], data)
    results: Dict[str, List[float]] = {}
    for line in reader:
        if location == "disk":
            battle = Battle(**ujson.loads(line))
        else:
            battle = Battle(**ujson.loads(zlib.decompress(line)))
        for stat in stats:
            results[stat].append(
                float(
                    getValMultiDimensional(
                        battle,
                        cast(
                            List[Union[str, int]],
                            list(
                                map(
                                    lambda ele: int(ele) if ele.isdigit() else ele,
                                    stat.split(),
                                )
                            ),
                        ),
                    )
                )
            )
    if location == "disk":
        cast(GzipFile, reader).close()
    return results
