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

class RawGame:
    def __init__(self, **options: Any):
        for key, value in options.items():
            setattr(self, key, value)
        # self.abbr: str = options.get('abbr')
        # self.achieve_score: int = options.get('achieve_score')
        # self.achieve_total: int = options.get('achieve_total')
        # self.game_inst_id: int = options.get('game_inst_id')
        # self.has_review: bool = options.get('has_review')
        # self.is_parent: bool = options.get('is_parent')
        # self.last_update: str = options.get('last_update')
        # self.notes: str = options.get('notes')
        # self.own: bool = options.get('own')
        # self.parent_inst_id: Optional[int] = options.get('parent_inst_id')
        # self.phys_digi: int = options.get('phys_digi')
        # self.platform_id: int = options.get('platform_id')
        # self.platform_title: str = options.get('platform_title')
        # self.priority: int = options.get('priority')
        # self.rating: Optional[int] = options.get('rating')
        # self.region: int = options.get('region')
        # self.status: int = options.get('status')
        # self.sub_abbr: Optional[str] = options.get('sub_abbr')
        # self.sub_platform_id: int = options.get('sub_platform_id')
        # self.sub_platform_title: Optional[str] = options.get('sub_platform_title')
        # self.title: str = options.get('title')

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
            match getattr(self, 'status'):
                case 10:
                    setattr(self, 'status', "Unplayed")
                case 20:
                    setattr(self, 'status', "Unfinished")
                case 30:
                    setattr(self, 'status', "Beaten")
                case 40:
                    setattr(self, 'status', "Completed")
                case 60:
                    setattr(self, 'status', "Endless")
                case 80:
                    setattr(self, 'status', "None")
                case _:
                    setattr(self, 'status', "")
        if hasattr(self, 'priority'):
            match getattr(self, 'priority'):
                case 10:
                    setattr(self, 'priority', "Shelved")
                case 20:
                    setattr(self, 'priority', "Replay")
                case 30:
                    setattr(self, 'priority', "Low")
                case 40:
                    setattr(self, 'priority', "Normal")
                case 50:
                    setattr(self, 'priority', "High")
                case 60:
                    setattr(self, 'priority', "Paused")
                case 70:
                    setattr(self, 'priority', "Ongoing")
                case 80:
                    setattr(self, 'priority', "Now Playing")
                case _:
                    setattr(self, 'priority', "")
        if hasattr(self, 'own'):
            match getattr(self, 'own'):
                case 1:
                    setattr(self, 'own', "Own")
                case 2:
                    setattr(self, 'own', "Formerly Owned")
                case 3:
                    setattr(self, 'own', "Played It")
                case 4:
                    setattr(self, 'own', "Other")
                case 5:
                    setattr(self, 'own', "Household")
                case 6:
                    setattr(self, 'own', "Subscription")
                case 7:
                    setattr(self, 'own', "Wishlist")
                case _:
                    setattr(self, 'own', "")
        if hasattr(self, 'phys_digi'):
            match getattr(self, 'phys_digi'):
                case 0:
                    setattr(self, 'phys_digi', "")
                case 1:
                    setattr(self, 'phys_digi', "Digital")
                case 20:
                    setattr(self, 'phys_digi', "Physical")
                case 21:
                    setattr(self, 'phys_digi', "Physical (Game Only)")
                case 22:
                    setattr(self, 'phys_digi', "Physical (Incomplete)")
                case 28:
                    setattr(self, 'phys_digi', "Physical (Complete In Box)")
                case 29:
                    setattr(self, 'phys_digi', "Physical (Sealed)")
                case 30:
                    setattr(self, 'phys_digi', "Physical (Licensed Repro)")
                case 31:
                    setattr(self, 'phys_digi', "Physical (Unlicensed Repro)")
                case _:
                    setattr(self, 'phys_digi', "")
        if hasattr(self, 'region'):
            match getattr(self, 'region'):
                case 1:
                    setattr(self, 'region', "Free")
                case 2:
                    setattr(self, 'region', "North America")
                case 3:
                    setattr(self, 'region', "Japan")
                case 4:
                    setattr(self, 'region', "PAL")
                case 5:
                    setattr(self, 'region', "China")
                case 6:
                    setattr(self, 'region', "Korea")
                case 7:
                    setattr(self, 'region', "Brazil")
                case 8:
                    setattr(self, 'region', "Asia")
                case _:
                    setattr(self, 'region', "")
        if hasattr(self, 'rating'):
            match getattr(self, 'rating'):
                case 1:
                    setattr(self, 'rating', "0.5 Stars")
                case 2:
                    setattr(self, 'rating', "1.0 Star")
                case 3:
                    setattr(self, 'rating', "1.5 Stars")
                case 4:
                    setattr(self, 'rating', "2.0 Stars")
                case 5:
                    setattr(self, 'rating', "2.5 Stars")
                case 6:
                    setattr(self, 'rating', "3.0 Stars")
                case 7:
                    setattr(self, 'rating', "3.5 Stars")
                case 8:
                    setattr(self, 'rating', "4.0 Stars")
                case 9:
                    setattr(self, 'rating', "4.5 Stars")
                case 10:
                    setattr(self, 'rating', "5.0 Stars")
                case _:
                    setattr(self, 'rating', "")
        if hasattr(self, 'difficulty'):
            match getattr(self, 'difficulty'):
                case 10:
                    setattr(self, 'difficulty', "Too Easy")
                case 20:
                    setattr(self, 'difficulty', "Relaxing")
                case 30:
                    setattr(self, 'difficulty', "Moderate")
                case 40:
                    setattr(self, 'difficulty', "Hurts So Good")
                case 50:
                    setattr(self, 'difficulty', "Too Hard")
                case 60:
                    setattr(self, 'difficulty', "Unfair")
                case _:
                    setattr(self, 'difficulty', "")

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