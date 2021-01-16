import requests
import jsonlines
import gzip
import zlib
import os
import shutil
import ujson
from objects import Battle, KeyAndName
from typing import Dict, List, cast, Union, Optional
import json
from gzip import GzipFile


def init(mode, data_path, api_key="") -> str:
    print(mode)
    headers: Dict[str, str] = {}
    if mode == "All":
        fileName: str = data_path + "battleAll.jl.gz"
        url: str = "http://stat.ink/api/v2/battle"
    elif mode == "User":
        fileName = data_path + "battle.jl.gz"
        url = "http://stat.ink/api/v2/user-battle"
        headers = {"Authorization": "Bearer {}".format(api_key)}
    if os.path.exists(fileName):
        recentId = 0
        try:
            with gzip.open(fileName) as reader:
                try:
                    os.remove(fileName[0:-6] + "Temp.jl.gz")
                except FileNotFoundError:
                    pass
                with gzip.open(
                    fileName[0:-6] + "Temp.jl.gz", "at", encoding="utf8"
                ) as writer:
                    for line in jsonlines.Reader(reader, ujson.loads):
                        ujson.dump(line, writer)
                        writer.write("\n")
                        recentId = line["id"]
            os.remove(fileName[0:-6] + "Temp.jl.gz")
        except (jsonlines.jsonlines.InvalidLineError, zlib.error):
            os.replace(fileName[0:-6] + "Temp.jl.gz", fileName)
        prevLastId: int = 0
        params: Dict[str, str] = {
            "order": "asc",
            "newer_than": str(recentId),
            "count": "50",
        }
        temp: List[Battle] = requests.get(url, headers=headers, params=params).json()
        if len(temp) > 0:
            try:
                shutil.rmtree(fileName[0:-6])
            except FileNotFoundError:
                pass
            lastId: int = cast(List[Dict[str, int]], temp)[-1]["id"]
            print(lastId)
            with gzip.open(fileName, "at", encoding="utf8") as writer:
                while lastId != prevLastId:
                    for job in temp:
                        ujson.dump(job, writer)
                        writer.write("\n")
                    writer.flush()
                    os.fsync(writer.fileno())
                    params["newer_than"] = str(lastId)
                    result = requests.get(
                        url,
                        headers=headers,
                        params=params,
                    )
                    print(result.url)
                    print(result)
                    temp = result.json()
                    prevLastId = lastId
                    if len(temp) > 0:
                        lastId = cast(List[Dict[str, int]], temp)[-1]["id"]
                    print(lastId)
    else:
        prevLastId = 0
        params = {"order": "asc", "count": "50"}
        temp = requests.get(url, headers=headers, params=params).json()
        lastId = cast(List[Dict[str, int]], temp)[-1]["id"]
        print(lastId)
        with gzip.open(fileName, "at", encoding="utf8") as writer:
            while lastId != prevLastId:
                for job in temp:
                    ujson.dump(job, writer)
                    writer.write("\n")
                params["newer_than"] = str(lastId)
                result = requests.get(url, headers=headers, params=params)
                print(result.url)
                print(result)
                temp = result.json()
                prevLastId = lastId
                if len(temp) > 0:
                    lastId = cast(List[Dict[str, int]], temp)[-1]["id"]
                print(lastId)
    return fileName


def hasBattles(location, data: Union[str, List[bytes]]) -> bool:
    """
    Check if a given data file has data.

    :param data: the full path of the data file
    :type data: str
    :return: whether the file has jobs or not
    :rtype: bool
    :raises gzip.BadGzipFile: if the file exists but isn't a gzip file
    :raises FileNotFoundError: if the file doesn't exist
    :raises jsonlines.InvalidLineError: if the file is a gzip file of something else

    :Example:

    >>> import core
    >>> core.hasBattles("data/battle.jl.gz")
    True
    >>> import gzip
    >>> with gzip.open("temp.jl.gz", "at", encoding="utf8") as writer:
    ...     writer.write("")
    ...
    >>> core.hasBattles("temp.jl.gz")
    False

    """
    try:
        if location == "disk":
            with gzip.open(cast(str, data)) as reader:
                jsonlines.Reader(reader, ujson.loads).read()
                return True
        else:
            jsonlines.Reader(data, ujson.loads).read()
            return True
    except EOFError:
        return False


def getValMultiDimensional(data, statArr: List[Union[str, int]]):
    """
    Retrieve the chosen stat from the provided data structure, using recursion.

    :param data: the data structure to retrieve data from
    :type data: Union[list, Dict[str, Any]]
    :param statArr: the list of dimensions of the data structure needed to retrieve the stat
    :type statArr: statArr: List[Union[str, int]
    :return: the value retrieved
    :rtype: str

    """
    if data is None:
        return 0
    if len(statArr) > 1:
        if isinstance(statArr[0], int):
            if len(data) > statArr[0]:
                return getValMultiDimensional(data[statArr[0]], statArr[1:])
            return 0
        return getValMultiDimensional(getattr(data, statArr[0]), statArr[1:])
    if isinstance(statArr[0], int):
        if len(data) > statArr[0]:
            return data[statArr[0]]
        return 0
    return getattr(data, statArr[0])


def getPlayerIdByName(location, data: Union[str, List[bytes]], name) -> List[str]:
    ids: List[str] = []
    if location == "disk":
        reader: Union[GzipFile, List[bytes]] = gzip.open(cast(str, data))
    else:
        reader = cast(List[bytes], data)
    for line in reader:
        if location == "disk":
            battle: Battle = Battle(**ujson.loads(line))
        else:
            battle = Battle(**ujson.loads(zlib.decompress(line)))
        if battle.players is not None:
            for player in battle.players:
                if (
                    player.name is not None
                    and player.splatnet_id is not None
                    and player.name == name
                    and player.splatnet_id not in ids
                ):
                    ids.append(player.splatnet_id)
    if location == "disk":
        cast(GzipFile, reader).close()
    return ids


def getNamesOfPlayer(location, data: Union[str, List[bytes]], player) -> List[str]:
    names: List[str] = []
    if location == "disk":
        with gzip.open(cast(str, data)) as reader:
            for line in reader:
                battle: Battle = Battle(**ujson.loads(line))
                if battle.players is not None:
                    for player in battle.players:
                        if (
                            player.splatnet_id is not None
                            and player.name is not None
                            and player.splatnet_id == player
                            and player.name not in names
                        ):
                            names.append(player.name)
    else:
        for battleLine in cast(List[bytes], data):
            battle = Battle(**ujson.loads(zlib.decompress(battleLine)))
            if battle.players is not None:
                for player in battle.players:
                    if (
                        player.splatnet_id is not None
                        and player.name is not None
                        and player.splatnet_id == player
                        and player.name not in names
                    ):
                        names.append(player.name)
    return names


def prettyPrintJsonLines(inPath, outPath):
    with gzip.open(inPath) as reader:
        with open(outPath, "w") as writer:
            writer.write("[")
            for line in reader:
                json.dump(json.loads(line), writer, indent=4)
                writer.write(",\n")
            writer.write("]")


def loadBattlesFromFile(data) -> List[bytes]:
    battles: List[bytes] = []
    with gzip.open(data) as reader:
        for line in reader:
            battles.append(zlib.compress(line))
    return battles


def findPeriodByMapsAndModes(
    location, data: Union[str, List[bytes]], maps: List[str], mode, rule
) -> List[int]:
    periods: List[int] = []
    if location == "disk":
        reader: Union[GzipFile, List[bytes]] = gzip.open(cast(str, data))
    else:
        reader = cast(List[bytes], data)
    for line in reader:
        if location == "disk":
            battle: Battle = Battle(**ujson.loads(line))
        else:
            battle = Battle(**ujson.loads(zlib.decompress(line)))
        if (
            (
                battle.map is not None
                and (battle.map.key == maps[0] or battle.map.key == maps[1])
            )
            and battle.mode == mode
            and battle.rule == rule
        ) and battle.period not in periods:
            periods.append(battle.period)
    if location == "disk":
        cast(GzipFile, reader).close()
    return periods


def findMapsAndModesByPeriod(
    location, data: Union[str, List[bytes]], period
) -> Dict[str, Dict[str, Dict[str, Union[List[KeyAndName], Optional[KeyAndName]]]]]:
    result: Dict[str, dict] = {
        "fest": {
            "standard": {"stages": [], "rule": None},
            "squad_4": {"stages": [], "rule": None},
            "fest_normal": {"stages": [], "rule": None},
        },
        "gachi": {
            "standard": {"stages": [], "rule": None},
            "squad_2": {"stages": [], "rule": None},
            "squad_4": {"stages": [], "rule": None},
        },
        "regular": {"standard": {"stages": [], "rule": None}},
        "private": {"private": {"stages": [], "rule": None}},
    }
    if location == "disk":
        reader: Union[GzipFile, List[bytes]] = gzip.open(cast(str, data))
    else:
        reader = cast(List[bytes], data)
    for line in reader:
        if location == "disk":
            battle: Battle = Battle(**ujson.loads(line))
        else:
            battle = Battle(**ujson.loads(zlib.decompress(line)))
        if (
            battle.period == period
            and battle.mode is not None
            and battle.lobby is not None
            and battle.map not in result[battle.mode.key][battle.lobby.key]
        ):
            result[battle.mode.key][battle.lobby.key]["stages"].append(battle.map)
            result[battle.mode.key][battle.lobby.key]["rule"] = battle.rule
    if location == "disk":
        cast(GzipFile, reader).close()
    return result
