from arcgis.geocoding import geocode
from arcgis.gis import GIS

gis = GIS(profile='LogajoQRX')

"""
    Helper function to combine adress data into a dict that can be fed into geocode().
    OUTPUT: dict(str:str)
"""
def create_address_dict(street: str, house_num: str, city: str, state: str, zip_code: str):
    addr = dict()
    addr['Street'] = house_num + " " + street
    addr['City'] = city
    addr['State'] = state
    addr['Zone'] = zip_code
    return addr
    
"""
    Runs geocode and returns the address' spacial coordinates as a tuple containing x,y values.
    OUTPUT: tuple(double)
"""
def get_coords(addr: dict):
    data = geocode(addr)
    for i in range(len(data)):
        print(data[0]['location']['x'])
    return data[0]['location']['x'], data[0]['location']['y']

if __name__ == "__main__":
    address = create_address_dict('Morningside Drive', '70', 'New York', 'NY', '10027')
    print(address)
    print(get_coords(address))
    exit
