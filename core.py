import requests
import jsonlines
import gzip
import os
import shutil
import ujson
from objects import Battle
from typing import Dict, List, cast, Union


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
        except jsonlines.jsonlines.InvalidLineError:
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
        return ""
    if len(statArr) > 1:
        if isinstance(statArr[0], int):
            if len(data) > statArr[0]:
                return getValMultiDimensional(data[statArr[0]], statArr[1:])
            return ""
        return getValMultiDimensional(getattr(data, statArr[0]), statArr[1:])
    if isinstance(statArr[0], int):
        if len(data) > statArr[0]:
            return data[statArr[0]]
        return ""
    return getattr(data, statArr[0])
