from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent="Fire Danger Estimator")

"""
    Helper function to combine adress data into a dict that can be fed into geocode().
    OUTPUT: dict(str:str)
"""
def create_address(street: str, city: str, state: str, zip_code: str):
    addr = ""
    addr += street
    addr += ", " + city
    addr += ", " + state
    addr += " " + zip_code
    return addr
    
"""
    Runs geocode and returns the address' spacial coordinates as a tuple containing x,y values.
    OUTPUT: tuple(double)
"""
def get_coords(addr: str):
    data = geolocator.geocode(addr)
    if data == None:
        return None
    return data.longitude, data.latitude
