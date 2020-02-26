import folium

from preprocess import PreProcess

from utils import *


class GIS:
    def __init__(self):
        self.preprocess = PreProcess()

    def draw_CDBG(self):
        geo_map = folium.Map(location=[42.795390191429625, -71.07516023514027], zoom_start=12)
        data = self.preprocess.get_CDBG_geometry_data()
        geo_json = folium.GeoJson(
            data,
            style_function=lambda feature: {
                'fillColor': '#ffff00',
                'color': 'black',
                'weight': 1,
                # 'dashArray': '1, 1'
            }
        )
        geo_json.add_to(geo_map)
        geo_map.save('release/CDBG.html')

    def draw_precincts_wards(self):
        geo_map = folium.Map(location=[42.795390191429625, -71.07516023514027], zoom_start=12)
        data = self.preprocess.get_precincts_wards_geometry_data()
        for i in range(len(data)):
            geo_json = folium.GeoJson(
                data=data[i]['geometry'],
                style_function=lambda feature: {
                    'fillColor': '#00BFFF',
                    'color': 'black',
                    'weight': 2,
                },
                overlay=True
            )
            geo_json.add_to(geo_map)
        geo_map.save('release/precincts_wards.html')

    def draw_division(self):
        self.draw_CDBG()
        self.draw_precincts_wards()


if __name__ == '__main__':
    gis = GIS()
    gis.draw_division()
