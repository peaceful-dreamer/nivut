import csv
from pyproj import Transformer


def lat_lon_to_israel_transverse_mercator(lat, lon):
    source_crs = 'epsg:4326' # Global lat-lon coordinate system
    target_crs = 'epsg:2039' # Israel Transverse Mercator

    x, y = Transformer.from_crs(source_crs, target_crs).transform(lat, lon)
    return x, y

def google_maps_to_lat_lon(url):
    lat_pos_indicator = "?q="
    lon_pos_indicator = "%2C" 
    lon_stop_indicator = "&z" 

    lat_pos = url.find(lat_pos_indicator)
    lon_pos = url.find(lon_pos_indicator)
    lon_stop = url.find(lon_stop_indicator)

    lat = url[lat_pos+len(lat_pos_indicator):lon_pos]
    lon = url[lon_pos+len(lon_pos_indicator):lon_stop]

    return lat, lon


lines = []
fieldnames = None

with open('_collections/points.csv', newline='') as csvfile:
    pointsreader = csv.DictReader(csvfile)
    fieldnames = pointsreader.fieldnames
    for row in pointsreader:
        lat, lon = google_maps_to_lat_lon(row['url'])
        x, y = lat_lon_to_israel_transverse_mercator(lat, lon)
        row.update({"lat": lat, "lon": lon, "x": x, "y": y})
        lines.append(row)
        
fieldnames.extend(["lat", "lon", "x", "y"])

with open('_collections/points.csv', 'w', newline='') as csvfile:
    pointswriter = csv.DictWriter(csvfile, fieldnames=fieldnames)
    pointswriter.writeheader()
    pointswriter.writerows(lines)

