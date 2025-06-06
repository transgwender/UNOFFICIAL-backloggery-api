import json

import backloggery

def main() -> None:
    client = backloggery.BacklogClient()
    client.get_library("Drumble")
    client.get_library("transgwender")
    result = client.search_library("Drumble", json.dumps({"abbr": "(?i)gcn", "title": "(?i)mario"}))
    pass

if __name__ == '__main__':
    main()