import requests
import shapely.wkt
import shapely.geometry
import json

#API ULKD
url = 'https://uldk.gugik.gov.pl/?request=GetParcelById&id=141201_1.0001.1867/2&result=geom_wkt&srid=4326' #srid 4326 for coordinates
url2 = 'https://uldk.gugik.gov.pl/?request=GetParcelById&id=141201_1.0001.1867/2&result=geom_wkt' #srid 2180 for area


#get data from ulkd
def get_data(api_url):
    response = requests.get(api_url)
    return response

#create shapely object - polygon
def build_polygon(api_url):
    #seperate srid and wkt from response
    srid, wkt = get_data(api_url).text.split(';')
    polygon = shapely.wkt.loads(wkt)
    return polygon

#use shapely poligon method
def calculate_area(polygon):
    return polygon.area

#generate geojson
def generate_geojson(polygon):
    polygon_json = shapely.geometry.mapping(polygon)
    return json.dumps(polygon_json)
