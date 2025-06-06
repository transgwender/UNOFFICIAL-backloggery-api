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

import backloggery

class Game:
    def __init__(self, **options: Any):
        self.abbr: str = options.get('abbr')
        self.achieve_score: int = options.get('achieve_score')
        self.achieve_total: int = options.get('achieve_total')
        self.game_inst_id: int = options.get('game_inst_id')
        self.has_review: bool = options.get('has_review')
        self.is_parent: bool = options.get('is_parent')
        self.last_update: str = options.get('last_update')
        self.notes: str = options.get('notes')
        self.own: bool = options.get('own')
        self.parent_inst_id: Optional[int] = options.get('parent_inst_id')
        self.phys_digi: int = options.get('phys_digi')
        self.platform_id: int = options.get('platform_id')
        self.platform_title: str = options.get('platform_title')
        self.priority: int = options.get('priority')
        self.rating: Optional[int] = options.get('rating')
        self.region: int = options.get('region')
        self.status: int = options.get('status')
        self.sub_abbr: Optional[str] = options.get('sub_abbr')
        self.sub_platform_id: int = options.get('sub_platform_id')
        self.sub_platform_title: Optional[str] = options.get('sub_platform_title')
        self.title: str = options.get('title')

    def compare_any(self, **options: Any) -> bool:
        l = [hasattr(self, c) and re.match(options.get(c), getattr(self, c)) for c in options]
        r = any(l)
        return r

    def compare_all(self, **options: Any) -> bool:
        l = [hasattr(self, c) and re.match(options.get(c), getattr(self, c)) for c in options]
        r = all(l)
        return r

class GameCache:
    def __init__(self, time: datetime.datetime, data: List[Game]):
        self.time = time
        self.data = data

def fetch(username: str) -> GameCache:
    data = {'type': "load_user_library", 'username': username}
    data = json.dumps(data).encode('utf-8')
    req = request.Request("https://backloggery.com/api/fetch_library.php", data=data)
    req.add_header('Content-Type', 'application/json')
    req.add_header('Accept', 'application/json')
    req.add_header('User-Agent', f'Backloggery Unofficial API Client/{backloggery.__version__} (dev[at]gwenkornak.ca)')
    # req.add_header('If-Modified-Since', 'Thu, 05 Jun 2025 04:14:34 GMT')
    resp = request.urlopen(req)
    result = json.loads(resp.read().decode('utf-8'))['payload']
    gc = GameCache(datetime.datetime.now(), [Game(**dct) for dct in result])
    return gc


class BacklogClient:
    def __init__(self) -> None:
        self.cache: Dict[str, GameCache] = {}

    def get_library(self, username: str) -> GameCache:
        if username not in self.cache:
            self.cache[username] = fetch(username)
        return self.cache[username]

    def search_library(self, username: str, search_regex: str, partial_match: bool = False) -> List[Game]:
        regex = json.loads(search_regex)
        lib = self.get_library(username)
        if partial_match:
            return [g for g in lib.data if g.compare_any(**regex)]
        else:
            return [g for g in lib.data if g.compare_all(**regex)]