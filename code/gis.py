import folium

from preprocess import PreProcess

from folium import FeatureGroup, LayerControl, Map, GeoJson, GeoJsonTooltip

from folium.plugins import FeatureGroupSubGroup


class GIS:
    def __init__(self):
        self.preprocess = PreProcess()

    def draw_CDBG(self):
        geo_map = Map(location=[42.795390191429625, -71.07516023514027], zoom_start=12)
        data = self.preprocess.get_CDBG_geometry_data()
        geo_json = GeoJson(
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
        geo_map = Map(location=[42.795390191429625, -71.07516023514027], zoom_start=12)
        data = self.preprocess.get_precincts_wards_geometry_data()
        for i in range(len(data)):
            ward_info = data[i]
            ward_number = ward_info['ward']
            feature_group = FeatureGroup(name='Ward ' + ward_number, control=True, show=True)
            feature_group.add_to(geo_map)
            precincts = ward_info['data']
            for j in range(len(precincts)):
                precinct = precincts[j]
                sub_feature_group = FeatureGroupSubGroup(name='Precinct '+precinct['properties']['Precinct'], group=feature_group, control=True, show=True)
                geo_json = GeoJson(
                    data=precinct,
                    style_function=lambda feature: {
                        'fillColor': '#00BFFF',
                        'color': 'black',
                        'weight': 1,
                    },
                    highlight_function=lambda feature: {
                        'fillColor': '#FFBFFF',
                        'color': 'yellow',
                        'weight': 2,
                    },
                    tooltip=GeoJsonTooltip(fields=['Precinct']),
                    overlay=True
                )
                geo_json.add_to(sub_feature_group)
                sub_feature_group.add_to(geo_map)
        LayerControl().add_to(geo_map)
        geo_map.save('release/precincts_wards.html')

    def draw_division(self):
        self.draw_CDBG()
        self.draw_precincts_wards()


if __name__ == '__main__':
    gis = GIS()
    gis.draw_division()