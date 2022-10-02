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
    coordinates = [tuple(a.split(' ')) for a in list]
    return coordinates


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
    print(ratio)
    width = 800
    height = width*1/ratio
    styles = ''
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
#BBOX=659944.766407799,486467.44840687,660557.657032805,486824.870281908

    #return 'https://integracja02.gugik.gov.pl/cgi-bin/KrajowaIntegracjaEwidencjiGruntow?VERSION=1.1.1&SERVICE=WMS&REQUEST=GetMap&LAYERS=dzialki,numery_dzialek,budynki&SRS=EPSG:2180&WIDTH=1570&HEIGHT=916&TRANSPARENT=TRUE&FORMAT=image/png&BBOX=659944.766407799,486467.44840687,660557.657032805,486824.870281908'
    return request_url
print(generate_map('141201_1.0001.1867/2','2180'))
