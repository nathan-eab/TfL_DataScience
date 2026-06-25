import requests

def fetch_arrivals(line_ids):
    """
    Fetch live arrival predictions for one or more bus lines.
    line_ids: a list of line id strings, e.g. ["24", "134"]
    """
    ids_joined = ",".join(line_ids)
    url = f"https://api.tfl.gov.uk/Line/{ids_joined}/Arrivals"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


if __name__ == "__main__":
    arrivals = fetch_arrivals(["15", "115"])
    print(f"Got {len(arrivals)} predictions")
    for entry in arrivals[:5]:
        print(entry["lineId"], "-", entry["stationName"], "-", entry["expectedArrival"])