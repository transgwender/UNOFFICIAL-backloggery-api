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

import datetime
import json
import re
from typing import Dict, Any, Optional, List
from urllib import request
from urllib.error import HTTPError

import backloggery
from backloggery.enums import *


class RawGame:
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

class GameCache:
    def __init__(self, time: datetime.datetime, data: List[Game]):
        self.time = time
        self.data = data

def fetch(username: str) -> HTTPError | GameCache:
    data = {'type': "load_user_library", 'username': username}
    data = json.dumps(data).encode('utf-8')
    req = request.Request("https://backloggery.com/api/fetch_library.php", data=data)
    req.add_header('Content-Type', 'application/json')
    req.add_header('Accept', 'application/json')
    req.add_header('User-Agent', f'Backloggery Unofficial API Client/{backloggery.__version__} (dev[at]gwenkornak.ca)')
    # req.add_header('If-Modified-Since', 'Thu, 05 Jun 2025 04:14:34 GMT')
    try:
        resp = request.urlopen(req)
    except HTTPError as err:
        return err
    decoded = json.loads(resp.read().decode('utf-8'))
    if not decoded:
        return HTTPError(resp.url, 404, f'No Data Found for {username}', resp.headers, resp.fp)
    result = decoded['payload']
    gc = GameCache(datetime.datetime.now(), [Game(**dct) for dct in result])
    return gc


class BacklogClient:
    def __init__(self) -> None:
        self.cache: Dict[str, GameCache] = {}

    def refresh_cache(self, username: str) -> None:
        fet = fetch(username)
        if isinstance(fet, HTTPError):
            raise fet
        self.cache[username] = fet

    def get_library(self, username: str) -> GameCache:
        if username not in self.cache:
            self.refresh_cache(username)
        return self.cache[username]

    def search_library(self, username: str, search_regex: str, partial_match: bool = False) -> List[Game]:
        regex = json.loads(search_regex)
        lib = self.get_library(username)
        if partial_match:
            return [g for g in lib.data if g.compare_any(**regex)]
        else:
            return [g for g in lib.data if g.compare_all(**regex)]