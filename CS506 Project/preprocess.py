import geopandas as gpd
import json


class PreProcess:
    def __init__(self):
        self.CDBG_file_path = 'resource/Hav_CDBG_Area_WGS84/Hav_CDBG_Area_WGS84.json'
        self.precincts_wards_file_path = 'resource/Hav_Precincts_Wards_WGS84/Hav_Precincts_Wards_WGS84.json'

    def get_CDBG_geometry_data(self) -> dict:
        gdf = gpd.read_file(self.CDBG_file_path)
        gdf = gdf.to_crs(epsg='4326')
        data = json.loads(gdf.to_json())['features'][0]['geometry']

        return data

    def get_precincts_wards_geometry_data(self) -> list:
        gdf = gpd.read_file(self.precincts_wards_file_path)
        gdf = gdf.to_crs(epsg='4326')
        data = json.loads(gdf.to_json())['features']

        return data


# if __name__ == '__main__':
#     preprocess = PreProcess()
#     data1 = preprocess.get_precincts_wards_geometry_data()


