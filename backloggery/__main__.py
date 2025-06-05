import backloggery

def main() -> None:
    client = backloggery.BacklogClient()
    client.get("Drumble")
    client.get("transgwender")
    pass

if __name__ == '__main__':
    main()