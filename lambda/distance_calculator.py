from math import cos, asin, sqrt, pi

def get_five_closest_stations(stations, lat, long):
    distances_from_home = {}

    # TODO optimise this algorithm
    for station in stations:
        station_lat = float(station["lat"])
        station_long = float(station["lon"])
        station_distance_from_home = distance(lat, long, station_lat, station_long)
        distances_from_home[station["station_id"]]  = station_distance_from_home

    closest_tuples = sorted(distances_from_home.items(), key=lambda x: x[1])[:5]
    closest_station_ids = []
    for pair in closest_tuples:
        station_id = pair[0]
        closest_station_ids.append(station_id)

    return (closest_station_ids)


def distance(lat1, lon1, lat2, lon2):
    p = pi/180
    a = 0.5 - cos((lat2-lat1)*p)/2 + cos(lat1*p) * cos(lat2*p) * (1-cos((lon2-lon1)*p))/2
    return 12742 * asin(sqrt(a)) 
