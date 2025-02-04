import pandas as pd

if __name__ == "__main__":
    #Import firestation data into a dataframe.
    stations = pd.read_csv('data/NYS_Firestations.csv')

    print(stations.loc[0]['Address'])
