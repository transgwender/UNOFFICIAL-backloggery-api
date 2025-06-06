import backloggery

def main() -> None:
    client = backloggery.BacklogClient()
    client.get_library("Drumble")
    client.get_library("transgwender")
    result = client.search_library("Drumble", "(?i)mario")
    pass

if __name__ == '__main__':
    main()