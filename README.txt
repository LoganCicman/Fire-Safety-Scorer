Fire Safety Scorer
by Logan Cicman


Purpose:

The Fire Safety Scorer is meant as a way of providing an estimate of a property's fire safety based on its proximity to fire stations. Firefighter response time is important in saving a structure, as a residential structure can become engulfed in flames in five minutes (https://www.ready.gov/home-fires). Thus, residences in close proximity to fire stations (especially if they are near multiple) are much safer in the event of a structural fire. This project aims to allow homeowners/buyers to see how well protected their home is in the event of a random structural fire. It provides a score in an easy to understand grade-like range of 0-100, with 0 being completely unprotected and 100 being well-protected by multiple close-by fire stations. More on how the score is claculated in the About section below.


Usage:

The Fire Safety Scorer can be run in the command line or any other code editor that runs python scripts. The file containing the scoring script is titled fireDangerEstimator.py and can be run with no arguments in this manner:
~/scorer_location$ python3 fireDangerEstimator.py

Two additional python files are also included in the package, as well as a data subfolder.

The file find_firestation_coords.py can be used to recompute the locations of the fire stations, taken as addresses from data/NYS_Firestations.csv (downloaded from https://data.gis.ny.gov/datasets/sharegisny::firestations/about), and store them in the file data/Station_Coordinates.csv. These coordinates are used in the scoring formula to compute distances to the nearest stations, so recomputing them to keep them up to date when new fire station data is made available is necessary to maintain accuracy. (Note: find_firestation_coords.py takes a while (~1 hour) to run, as HTTP requests for the coordinates have built in delays due to request limits by Nominatim.)

The file location_finder.py contains support methods that allow for the proper operation of the scorer, such as compiling addresses into singular strings and gathering coordinates via geocoding. This file is necessary for fireDangerEstimator.py to run properly, but does nothing when run on its own.


About:

-The Score: The fire safety score takes into account 3 factors, each weighted differently. The first is the average distance of the 5 nearest fire stations to the address (weighted 35%). The second is the average distance of the 2 closest fire stations (weighted 50%). The last is the distance of the nearest station (weighted 15%). The closest stations are found using a simple 5 Nearest Neighbors search by calculating the distance to each station in miles using the Haversine Formula to compute distance between geographic coordinates. Each factor is put on a 0-100 scale prior to weighting, resulting in a result that is also in the range [0-100]. The averages of the closest 2 and 5 stations are placed on a 100 point scale logarithmically, so as the distance increases linearly, the score decreases at a greater rate. The formula for both is given by f(x)=143-62ln(x), where x is the average distance of either 2 or 5 stations. If f(x)>100, it is capped at 100, and if f(x)<0, it is raised to 0. The distance of the closest station's score is used as a sort of bonus, given by g(x)=max(0, (100/2.23)(2.23-x)), where x is the distance of the closest station. This rewards locations with a station within 2.23 miles with a greater overall score. Why 2.23 miles? The time it takes for a fire station to arrive on scene is given by T=0.65+1.7D (https://www.mtas.tennessee.edu/reference/estimating-travel-time-fire-apparatus), where T is the time in 0.1min and D is the driving distance in 0.1mi. If a house becomes engulfed in 5min (https://www.ready.gov/home-fires), then the station needs to be within 2.9mi to arrive before that point. Assuming that driving distance is ~30% greater than straight line distance between two points (https://hcup-us.ahrq.gov/reports/methods/MS2021-02-Distance-to-Hospital.jsp), this means that the fire station must be within 2.23mi to arrive in <=5min, with even smaller distances being even better. The weighted average of the 3 scores is then computed using the above weights to produce the final fire safety score.

-Acknowledgements/References:
	-Geocoding of addresses to coordinate points was performed via the Nominatim Geocoder, made available at https://nominatim.org, and the results were obtained using the GeoPy API (https://geopy.readthedocs.io/en/stable/).
	-Fire station address data was public data made available by the State of New York GIS Database (https://data.gis.ny.gov/datasets/sharegisny::firestations/about).
	-Information used in computation of a meaningful score was obtained from:
		https://www.ready.gov/home-fires
		https://www.mtas.tennessee.edu/reference/estimating-travel-time-fire-apparatus
		https://hcup-us.ahrq.gov/reports/methods/MS2021-02-Distance-to-Hospital.jsp
