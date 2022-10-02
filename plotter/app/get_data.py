import requests
import shapely.wkt
import shapely.geometry


#plot_id=141201_1.0001.1867/2
#srid 2180 for area
#srid 4326 for coordinates
def get_wkt(plot_id, srid):
        url = f'https://uldk.gugik.gov.pl/?request=GetParcelById&id={plot_id}&result=geom_wkt&srid={srid}'
        response = requests.get(url)
        return response

#create shapely object - polygon
def build_polygon(plot_id, srid):
    #seperate srid and wkt from response
    wkt = get_wkt(plot_id, srid).text.split(';')[1]
    polygon = shapely.wkt.loads(wkt)
    return polygon

#create coordinates list
def get_coordinates(plot_id, srid):
    #format response to be a list of tuples
    wkt = get_wkt(plot_id, srid).text.split(';')[1]
    list = wkt[9:-3].split(',')
    coordinates = [tuple(reversed(a.split(' '))) for a in list]
    return coordinates

#get data for plot

def plot_data(plot_id, srid):
    #calculate data from coordinates
    polygon = build_polygon(plot_id, srid)
    area = polygon.area
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
    response = requests.get(request_url)
    print(response)

plot_data('141201_1.0001.1867/2', '2180')
#create map view from WMS web map service
def generate_map(plot_id, srid):
    polygon = build_polygon(plot_id, srid)
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
