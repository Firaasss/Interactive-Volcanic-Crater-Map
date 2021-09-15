import folium, pandas

html = """<h4>Volcano Information:</h4>
Volcano Name: <a href="https://www.google.com/search?q=%%22%s%%22" target="_blank">%s</a><br>
Height: %s m<br>
Type: %s<br>
Status: %s
"""

# function that will be passed with an elevation value to classify a marker's color
def color_maker(elevation):
    if(elevation >= 0 and elevation < 2000):
        return 'green'
    elif(elevation >= 2000 and elevation < 3000):
        return 'orange'
    else:
        return 'red'

map = folium.Map(location = [38.9700012,-112.5009995], zoom_start=3, tiles='OpenStreetMap')
fg = folium.FeatureGroup(name="Volcano & Population RT Map")

#pulling columns from csv using pandas and storing lists locally
data = pandas.read_csv("Webmap_datasources/Volcanoes.txt")
lat = data["LAT"].to_list()
lon = data["LON"].to_list()
elev = data["ELEV"].to_list()
stat = data["STATUS"].to_list()
type = data["TYPE"].to_list()
name = data["NAME"].to_list()

fgm = folium.FeatureGroup(name="Volcanoes")

# looping through both lists simultaneously using zip f'n
for lat, lon, elev, name, stat, type in zip(lat, lon, elev, name, stat, type):
    iframe = folium.IFrame(html=html % (name, name, elev, type, stat), width=300, height=150)
    fgm.add_child(folium.CircleMarker(
        location = [lat, lon],
        popup = folium.Popup(iframe),
        fill_color=color_maker(elev),
        radius = 6,
        color = 'grey',
        fill_opacity = 0.7
    ))

fgp = folium.FeatureGroup(name="Population")

#adding Geo layer to map for population levels
fgp.add_child(folium.GeoJson(
    data = open("Webmap_datasources/world.json", "r", encoding="utf-8-sig").read(),
    style_function = lambda x: {'fillColor':'green' if x['properties']['POP2005'] < 10000000
        else 'orange' if 10000000 <= x['properties']['POP2005'] < 20000000 else 'red'}
))

map.add_child(fgm)
map.add_child(fgp)
map.add_child(folium.LayerControl())

map.save("Map1.html")
