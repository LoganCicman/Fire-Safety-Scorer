import pandas as pd
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
from time import sleep
from location_finder import create_address

if __name__ == "__main__":
    #Set geocoding method.
    geolocator = Nominatim(user_agent="find_firestation_coords")
    geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)

    #Import firestation data into a dataframe.
    stations = pd.read_csv('data/NYS_Firestations.csv')

    #For each station, do a geocode query to find the station's coordinates in the cartesian frame.
    coords = pd.DataFrame(columns=['ID', 'x', 'y'])
    addrs = list()
    """
    for i in range(len(stations)):
        cur = stations.loc[i]
        addr = create_address(cur['Address'], cur['City'], 'NY', str(cur['Zip']))
        geoData = get_coords(addr)
        if not geoData == None:
            coords.loc[len(coords)] = {'ID':i, 'x':float(geoData[0]), 'y':float(geoData[1])}
    """
    for i in range(len(stations)):
        cur = stations.loc[i]
        a = create_address(cur['Address'], cur['City'], 'NY', str(cur['Zip']))
        addrs.append(a)

    #Now get the coordinates for the concatenated addresses.
    results = [geocode(ad) for ad in addrs]
    print(results)
    for i in range(len(results)):
        if not results[i] == None:
            coords.loc[len(coords)] = {'ID':i, 'x':results[i].longitude, 'y':results[i].latitude}


    #Save the coordinates as a csv to be used in fire safety calculations.
    coords.to_csv('data/Station_Coordinates.csv', index=False)
