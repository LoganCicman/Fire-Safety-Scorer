from arcgis.geocoding import geocode
from arcgis.gis import GIS

gis = GIS(profile='LogajoQRX')

"""
    Helper function to combine adress data into a dict that can be fed into geocode().
    OUTPUT: dict(str:str)
"""
def create_address_dict(street: str, city: str, state: str, zip_code: str):
    addr = dict()
    addr['Street'] = street
    addr['City'] = city
    addr['State'] = state
    addr['Postal'] = zip_code
    return addr
    
"""
    Runs geocode and returns the address' spacial coordinates as a tuple containing x,y values.
    OUTPUT: tuple(double)
"""
def get_coords(addr: dict):
    #data = geocode(addr, search_extent={'ymin': 40.49, 'ymax': 45.025, 'xmin': -79.78, 'xmax': -71.86})
    data = geocode(addr)
    return data[0]['location']['x'], data[0]['location']['y']

if __name__ == "__main__":
    address = create_address_dict('1039 West Park Avenue', 'Long Beach', 'NY', '11561')
