"""
The MIT License (MIT)

Copyright (c) 2025-present transgwender

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
"""

import json
import re
from datetime import datetime, UTC
from typing import Dict, Any, List
from urllib import request

import backloggery
from backloggery.enums import *


class NoDataFoundError(LookupError):
    """ No data found during lookup. """
    def __init__(self, *args, **kwargs): # real signature unknown
        pass

    @staticmethod # known case of __new__
    def __new__(*args, **kwargs): # real signature unknown
        """ Create and return a new object.  See help(type) for accurate signature. """
        pass

class RawGame:
    """
    The raw game data
    """
    def __init__(self, **options: Any):
        for key, value in options.items():
            setattr(self, key, value)

    def __str__(self) -> str:
        return str(self.__dict__)

    def compare_any(self, **options: Any) -> bool:
        l = [hasattr(self, c) and re.match(options.get(c), getattr(self, c)) for c in options]
        r = any(l)
        return r

    def compare_all(self, **options: Any) -> bool:
        l = [hasattr(self, c) and re.match(options.get(c), getattr(self, c)) for c in options]
        r = all(l)
        return r

class Game(RawGame):
    """
    The processed game data
    """

    def __init__(self, **options: Any):
        super().__init__(**options)
        if hasattr(self, 'status'):
            setattr(self, 'status', cast(Status, getattr(self, 'status')))
        if hasattr(self, 'priority'):
            setattr(self, 'priority', cast(Priority, getattr(self, 'priority')))
        if hasattr(self, 'own'):
            setattr(self, 'own', cast(Own, getattr(self, 'own')))
        if hasattr(self, 'phys_digi'):
            setattr(self, 'phys_digi', cast(PhysDigi, getattr(self, 'phys_digi')))
        if hasattr(self, 'region'):
            setattr(self, 'region', cast(Region, getattr(self, 'region')))
        if hasattr(self, 'rating'):
            setattr(self, 'rating', cast(Rating, getattr(self, 'rating')))
        if hasattr(self, 'difficulty'):
            setattr(self, 'difficulty', cast(Difficulty, getattr(self, 'difficulty')))

class LibraryCache:
    """
    The cache of game library data

    :var time: datetime - The timestamp of the cache
    :var data: List[Game] - The game library data
    """
    def __init__(self, time: datetime, data: List[Game]):
        self.time = time
        self.data = data

def fetch_gameinfo(game_inst_id: int) -> Game:
    """
    Preforms a fetch game info call to Backloggery.

    :param game_inst_id: The id of the game instance to fetch.
    :raises NoDataFoundError: If no data was found for the given id.
    :return: The game data received for the given id.
    """

    data = {'game_inst_id': game_inst_id}
    data = json.dumps(data).encode('utf-8')
    req = request.Request("https://backloggery.com/api/fetch_gameinfo.php", data=data)
    req.add_header('Content-Type', 'application/json')
    req.add_header('Accept', 'application/json')
    req.add_header('User-Agent', f'Backloggery Unofficial API Client/{backloggery.__version__} (dev[at]gwenkornak.ca)')
    # req.add_header('If-Modified-Since', 'Thu, 05 Jun 2025 04:14:34 GMT')
    resp = request.urlopen(req)
    decoded = json.loads(resp.read().decode('utf-8'))
    if not decoded:
        raise NoDataFoundError(f'No Data Found for {game_inst_id}')
    result = decoded['payload']
    game = Game(**result)
    return game

def fetch_library(username: str) -> LibraryCache:
    """
    Preforms a fetch library call to Backloggery.

    :param username: The username of the user to fetch.
    :raises NoDataFoundError: If no results were found for the given username.
    :return: The library data received for the given username.
    """

    data = {'type': "load_user_library", 'username': username}
    data = json.dumps(data).encode('utf-8')
    req = request.Request("https://backloggery.com/api/fetch_library.php", data=data)
    req.add_header('Content-Type', 'application/json')
    req.add_header('Accept', 'application/json')
    req.add_header('User-Agent', f'Backloggery Unofficial API Client/{backloggery.__version__} (dev[at]gwenkornak.ca)')
    # req.add_header('If-Modified-Since', 'Thu, 05 Jun 2025 04:14:34 GMT')
    resp = request.urlopen(req)
    decoded = json.loads(resp.read().decode('utf-8'))
    if not decoded:
        raise NoDataFoundError(f'No Data Found for {username}')
    result = decoded['payload']
    gc = LibraryCache(datetime.now(UTC), [Game(**dct) for dct in result])
    return gc


class BacklogClient:
    """
    Client to interact with Backloggery API.
    """
    def __init__(self) -> None:
        self.cache: Dict[str, LibraryCache] = {}

    def refresh_cache(self, username: str) -> None:
        """
        Refreshes the cache for the given username.

        :raises NoDataFoundError: If no data was found for the specified username.
        :param username: The username to refresh.
        """
        fet = fetch_library(username)
        self.cache[username] = fet

    def get_game(self, game_inst_id: int) -> Game:
        """
        Gets the details of the specified game instance.

        :param game_inst_id: The game instance ID
        :raises NoDataFoundError: If no data was found for the specified game instance.
        :return: The game data corresponding to the game instance ID
        """

        fet = fetch_gameinfo(game_inst_id)
        return fet

    def get_library(self, username: str) -> LibraryCache:
        """
        Gets the library of the specified user. Prioritizes the cached data if exists.

        :param username: The username to look for
        :raises NoDataFoundError: If no data was found for the specified username.
        :return: The cache of the username's library games.
        """
        if username not in self.cache:
            self.refresh_cache(username)
        return self.cache[username]


    def search_library(self, username: str, search_regex: str, partial_match: bool = False) -> tuple[datetime, list[Game]]:
        """
        Searches the specified library for games that match the given regex.

        :param username: The username to search the library of.
        :param search_regex: A json containing parameters and the regular expression to compare against.
        :param partial_match: If True, return games that match any one of the regular expression. If False, return games that match every regular expression.
        :raises NoDataFoundError: If no data was found for the specified username.
        :return: A tuple containing both the time the library was fetched, and a list of the games found, if any.
        """
        regex = json.loads(search_regex)
        lib = self.get_library(username)
        if partial_match:
            return lib.time, [g for g in lib.data if g.compare_any(**regex)]
        else:
            return lib.time, [g for g in lib.data if g.compare_all(**regex)]