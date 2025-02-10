import numpy as np
import pandas as pd
from location_finder import create_address, get_coords


if __name__ == "__main__":
    #Download station data to pandas dataframe.
    locs = pd.read_csv("data/Station_Coordinates.csv")

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
        addr = create_address(house_num+" "+street, city, state, zip_code)
        addr_xy = get_coords(addr)

        """
        Find 5 closest fire stations to the address.
        Use Law of Haversines to find distance from each fire station.
        """
        r = 3963
        long = np.deg2rad(addr_xy[0])
        lat = np.deg2rad(addr_xy[1])
        nearby = list()
        for num in range(5):
            nearby.append((-1,np.inf))
        for idx, station in locs.iterrows():
            f_long = np.deg2rad(station["x"])
            f_lat = np.deg2rad(station["y"])
            d = np.sin((lat-f_lat)/2)**2 + np.cos(lat)*np.cos(f_lat)*(np.sin((long-f_long)/2)**2)
            d = 2*r*np.arcsin(d**0.5)
            if d <= nearby[0][1]:
                nearby.insert(0, (station["ID"], d))
                nearby.pop(5)
            elif d <= nearby[1][1]:
                nearby.insert(1, (station["ID"], d))
                nearby.pop(5)
            elif d <= nearby[2][1]:
                nearby.insert(2, (station["ID"], d))
                nearby.pop(5)
            elif d <= nearby[3][1]:
                nearby.insert(3, (station["ID"], d))
                nearby.pop(5)
            elif d<= nearby[4][1]:
                nearby.insert(4, (station["ID"], d))
                nearby.pop(5)
                
        """
        Calculate final fire safety score from 0-100.
        Based 60% on log function of 2 closest stations.
        Based 35% on log function of 3 closest stations.
        Based 15% on distance of closest station (if <=2.23mi).
        """
        avg5 = 0
        avg2 = 0
        for j in range(len(nearby)):
            if j <= 1:
                avg2 += nearby[j][1]
            avg5 += nearby[j][1]
        avg2 /= 2.0
        avg5 /= 5.0

        log5 = max(143-62*np.log(avg5), 0)
        log5 = min(log5, 100)
        log2 = max(143-62*np.log(avg2), 0)
        log2 = min(log2, 100)

        score = 0.5*log2 + 0.35*log5 + 0.15*min(100, max(0, (2.23 - nearby[0][1])*(100/2.23)))
        print("Your address' fire safety score is ", np.round(score), "/100.")

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
