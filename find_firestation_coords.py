import pandas as pd
from arcgis.gis import GIS
from location_finder import create_address_dict, get_coords

gis = GIS(profile = "LogajoQRX")

if __name__ == "__main__":
    #Import firestation data into a dataframe.
    stations = pd.read_csv('data/NYS_Firestations.csv')

    #For each station, do a geocode query to find the station's coordinates in the cartesian frame.
    coords = pd.DataFrame(columns=['ID', 'x', 'y'])
    for i in range(len(stations)):
        cur = stations.loc[i]
        addr = create_address_dict(cur['Address'], cur['City'], 'NY', cur['Zip'])
        geoData = get_coords(addr)
        coords.loc[len(coords)] = {'ID':i, 'x':float(geoData[0]), 'y':float(geoData[1])}
        
    #Save the coordinates as a csv to be used in fire safety calculations.
    coords.to_csv('data/Station_Coordinates.csv', index=False)
