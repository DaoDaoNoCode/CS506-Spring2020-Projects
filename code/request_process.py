import pandas as pd
import numpy as np
import folium
from folium import plugins
from folium import FeatureGroup, LayerControl, Map, Marker
from folium.plugins import MarkerCluster


# read request from csv file and remove invalid entries
def read_request(path):
    # 0 = Request ID
    # 1 = Create Date
    # 5 = Status Code
    # 10 = Request Type ID
    # 11 = Request Type
    # 19 = Address
    # 28 = Priority
    # 29 = Longitude
    # 30 = Latitude
    requests = pd.read_csv(path, usecols=[
        0, 1, 5, 10, 11, 19, 28, 29, 30])
    request_valid = remove_invalid_entries(requests)

    return request_valid


# find out all kinds of requests
# save request type in a dictionary: {Request Type ID: Request Type}
def filter_request_type(requests):
    requests_type = np.array(requests[["Request Type ID", "Request Type"]])
    requests_dict = {}
    for request in requests_type:
        request_id = request[0]
        if request_id not in requests_dict:
            requests_dict[request_id] = request[1]

    return requests_dict


# remove all entries that do not have longitude or latitude
def remove_invalid_entries(requests):
    requests_position = np.array(requests[["Address", "Longitude", "Latitude"]])
    requests_drop = []
    for i in range(len(requests_position)):
        if requests_position[i][0] is np.nan or requests_position[i][1] == 0 or requests_position[i][2] == 0:
            requests_drop.append(i)
    requests_remain = requests.drop(requests_drop)

    return requests_remain


# classify requests by type
# put same type of requests coordinates in a list
# requests_final = {Request Type: [[Latitude, Longitude, Address]]}
def classify_requests_coordinate(requests):
    requests_type_dict = filter_request_type(requests)
    requests_final = {}
    for type_id in requests_type_dict:
        requests_final[requests_type_dict[type_id]] = []
    requests_type_coordinate = np.array(
        requests[["Request Type", "Latitude", "Longitude", "Address"]])
    for request in requests_type_coordinate:
        requests_final[request[0]].append([request[1], request[2], request[3]])

    return requests_final


# find center of a cluster of coordinates
# coordinates: numpy array
def find_center(coordinates):
    center = np.mean(coordinates, axis=0)

    return center


# draw heatmap
# requests: dict
def draw_heatmap(requests):
    a_map = Map(location=[42.76, -71.08], zoom_start=10)
    show = True
    for request_type in requests:
        if show:
            feature_group = FeatureGroup(name=request_type, show=True)
            show = False
        else:
            feature_group = FeatureGroup(name=request_type, show=False)
        mc = MarkerCluster()
        for request in requests[request_type]:
            print(request[2])
            popup_info = "Request Type: \n" + request_type + "\nAddress: " + request[2]
            mc.add_child(Marker(location=[request[0], request[1]], popup=popup_info))
        mc.add_to(feature_group)
        feature_group.add_to(a_map)

    LayerControl().add_to(a_map)
    a_map.save("map.html")


if __name__ == '__main__':
    requests = read_request("resource/haverhill-request_updated.csv")
    # print(requests)
    # filter_request_type(requests)
    # remove_invalid_entries(requests)
    requests_final = classify_requests_coordinate(requests)
    draw_heatmap(requests_final)
