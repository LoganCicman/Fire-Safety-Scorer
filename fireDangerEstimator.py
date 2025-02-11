import numpy as np
import pandas as pd
from re import match
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
            if not match("(\d+-\d+|\d+)[A-Za-z]?", house_num):
                cont = True
                print("Error: House Number must be in one of the following formats:")
                print("\t-Only numbers (such as 123).")
                print("\t-Numbers followed by a letter (such as 123A).")
                print("\t-Two groupings of numbers separated by a hyphen (such as 12-34).")
                print("\t-Two groupings of numbers separated by a hyphen followed by a letter (such as 12-34A).")
            if not (zip_code.isdigit() and len(zip_code) == 5) :
                cont = True
                print("Error: Zip Code must be a 5-digit positive value.")
        
        state = "NY" #As this will always be the case for addresses using this tool.

        #Find the coordinates of the provided address.
        addr = create_address(house_num+" "+street, city, state, zip_code)
        addr_xy = get_coords(addr)

        #Re-prompt the user for a different address if it cannot find their address.
        if addr_xy == None:
            print("\nThe address you provided could not be located. Please enter 0 to quit, 1 to try again, or h for address entry troubleshooting tips.")
            while True:
                c = input().lower()
                if c.strip() == '0':
                    exit
                elif c.strip() == 'h':
                    print("\n__________Address Entry Help__________")
                    print("Common Errors:")
                    print("-Make sure to include street suffixes such as \"St\", \"Ave\", etc. or the full word (\"Street\", \"Avenue\", etc.) in the street name.\n For example, if you live at 123 Oak Street, enter \"Oak St.\" or \"Oak Street\" as the street, rather than just \"Oak\".")
                    print("-Make sure everything is accurate. A small difference in house number should make little difference (unless the entered house number does not exist)")
                    print("However, entering a zip code or city that doesn't match the address will make it difficult to locate the correct location.")
                    print("\nPlease enter 0 to quit or 1 to try again.")
                elif c.strip() == '1':
                    break
                else:
                    print("Invalid option. Please enter 0 to quit, 1 to try again, or h to get help.")
            continue


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
        print("Your address' fire safety score is ", int(np.round(score)), "\b/100.")
        print(score)

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
