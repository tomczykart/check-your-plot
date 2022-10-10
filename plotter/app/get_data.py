import requests
import shapely.wkt
import shapely.geometry
import xmltodict

#plot_id=141201_1.0001.1867/2
#srid 2180 for area
#srid 4326 for coordinates
def get_wkt(plot_id, srid):
        url = f'https://uldk.gugik.gov.pl/?request=GetParcelById&id={plot_id}&result=geom_wkt&srid={srid}'
        response = requests.get(url)
        return response

#create shapely object - polygon
def build_polygon(response):
    #seperate srid and wkt from response
    wkt = response.text.split(';')[1]
    polygon = shapely.wkt.loads(wkt)
    return polygon

#create coordinates list
def get_coordinates(plot_id, srid):
    #format response to be a list of tuples
    wkt = get_wkt(plot_id, srid).text.split(';')[1]
    list = wkt[9:-3].split(',')
    coordinates = [tuple(reversed(a.split(' '))) for a in list]
    return coordinates

#get xml with plot information
def plot_data_xml(plot_id, srid):
    #calculate data from coordinates
    response = get_wkt(plot_id, srid)
    polygon = build_polygon(response)
    #area = polygon.area
    point = polygon.representative_point()#point within the shape
    point_x = point.x
    point_y = point.y
    map_bounds = (point_x, point_y, point_x, point_y) #map bounds eqals one pixel

    #ask api for additional data
    #map parameters for request:
    layers = 'dzialki'
    srs = srid
    bbox = str(map_bounds)[1:-1]
    width = 1
    height = 1
    x = 0
    y = 0

    request_url = f'''https://integracja.gugik.gov.pl/cgi-bin/KrajowaIntegracjaEwidencjiGruntow?
                    VERSION=1.1.1&
                    SERVICE=WMS&
                    REQUEST=GetFeatureInfo&
                    FORMAT=image/png&
                    WIDTH={width}&
                    HEIGHT={height}&
                    LAYERS={layers}&
                    SRS=EPSG:{srs}&
                    BBOX={bbox}&
                    QUERY_LAYERS={layers}&
                    X={x}&
                    Y={y}
                    '''
    request_url = request_url.replace('\n','')
    request_url = request_url.replace(' ','') #request link is ready
    #print(request_url)
    response = requests.get(request_url)
    return response #xml file

def plot_area(plot_id, srid):
    #calculate data from coordinates
    response = get_wkt(plot_id, srid)
    polygon = build_polygon(response)
    area = polygon.area
    area = round(area, 2)
    return area

def parse_xml(plot_id, srid):
    xml = plot_data_xml(plot_id, srid).content
    #print(xml)
    data = xmltodict.parse(xml)
    #print(data.keys())
    a = data['FeatureCollection']['gml:featureMember']['Layer']['Attribute']#list of dictionaries
    #create a dict parameter:value from dict list
    plot_parameters = {}
    for dict in a:
        try:
            key = dict['@Name']
            value = dict['#text']
            plot_parameters[key] = value
        except KeyError:
            plot_parameters[key] = 'brak danych'
            continue
    return plot_parameters


def generate_map(plot_id, srid):
    response = get_wkt(plot_id, srid)
    polygon = build_polygon(response)
    minx, miny, maxx, maxy = polygon.bounds #tuple of floats(minx, miny, maxx, maxy)
    map_bounds = (minx-15, miny-15, maxx+15, maxy+15) #add margin around the plot

    #map parameters for request:
    layers = 'dzialki,numery_dzialek,budynki'
    srs = srid
    bbox = str(map_bounds)[1:-1]
    ratio = (map_bounds[2]-map_bounds[0])/(map_bounds[3]-map_bounds[1])#ratio for propper image height
    width = 800
    height = width*1/ratio
    request_url = f'''https://integracja02.gugik.gov.pl/cgi-bin/KrajowaIntegracjaEwidencjiGruntow?
                    VERSION=1.1.1&
                    SERVICE=WMS&
                    REQUEST=GetMap&
                    FORMAT=image/png&
                    WIDTH={width}&
                    HEIGHT={height}&
                    LAYERS={layers}&
                    SRS=EPSG:{srs}&
                    BBOX={bbox}
                    '''
    request_url = request_url.replace('\n','')
    request_url = request_url.replace(' ','')

    return request_url
