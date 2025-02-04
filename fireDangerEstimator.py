import numpy as np
import pandas as pd
from location_finder import create_address_dict, get_coords
from arcgis.gis import GIS

gis = GIS(profile="LogajoQRX")

if __name__ == "__main__":
    print("Welcome to the Fire Safety Scorer.")
    while True:
        #Prompt user for address input and format properly.
        street = ''
        house_num = ''
        city = ''
        state = ''
        zip_code = ''
        cont = True
        while cont:
            cont = False
            print()
            print("Enter your address to compute your house/property's fire danger score.")
            print("Press enter after each line to submit your data.")
            print("House Number: ", end="")
            house_num = input()
            print("Street Name: ", end="")
            street = input()
            print("City: ", end="")
            city = input()
            print("State: ", end="")
            state = input()
            print("5-Digit Zip Code: ", end="")
            zip_code = input()

            print()

            #Test validity of entered data.
            if not (state.lower().strip() == "ny" or state.lower().strip() == "new york"):
                cont = True
                print("Currently this tool only works for addresses in the state of New York. Please enter state as either \"New York\" or \"NY\".")
            if not house_num.isdigit():
                cont = True
                print("Error: House Number musst be a positive integer.")
            if not (zip_code.isdigit() and len(zip_code) == 5) :
                cont = True
                print("Error: Zip Code must be a 5-digit positive value.")
        
        state = "NY" #As this will always be the case for addresses using this tool.

        #Find the coordinates of the provided address.
        addr = create_address_dict(house_num+" "+street, city, state, zip_code)
        print(addr)
        addr_xy = get_coords(addr)
        print(addr_xy)

        #Ask user if they would like to test another address.
        print("Thank you for using the Fire Safety Scorer. Enter 1 to test another address or 0 to exit.")
        while True:
            choice = input()
            if choice.strip() == "0":
                exit()
            elif choice.strip() == "1":
                break
            else:
                print("Invalid option. Please enter 1 to test another address or 0 to exit.")
