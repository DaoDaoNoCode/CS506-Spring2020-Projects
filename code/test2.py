import folium
import folium.plugins as plugins


if __name__ == '__main__':

    m = folium.Map(location=[0, 0], zoom_start=6)

    fg = folium.FeatureGroup(name='group1')
    m.add_child(fg)

    g11 = plugins.FeatureGroupSubGroup(fg, 'group1_part1')
    m.add_child(g11)

    g12 = plugins.FeatureGroupSubGroup(fg, 'group1_part2')
    m.add_child(g12)

    folium.Marker([-1, -1]).add_to(g11)
    folium.Marker([1, 1]).add_to(g11)

    folium.Marker([-1, 1]).add_to(g12)
    folium.Marker([1, -1]).add_to(g12)

    fg2 = folium.FeatureGroup(name='group2')
    m.add_child(fg2)

    g21 = plugins.FeatureGroupSubGroup(fg2, 'group2_part1')
    m.add_child(g21)

    g22 = plugins.FeatureGroupSubGroup(fg2, 'group2_part2')
    m.add_child(g22)

    folium.Marker([-2, -2]).add_to(g21)
    folium.Marker([2, 2]).add_to(g21)

    folium.Marker([-2, 2]).add_to(g22)
    folium.Marker([2, -2]).add_to(g22)


    folium.LayerControl(collapsed=False).add_to(m)
    m.save('release/Plugins_8.html')