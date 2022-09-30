import requests

#plot_id=141201_1.0001.1867/2
#srid 2180 for area
#srid 4326 for coordinates
def get_wkt(plot_id, srid):
        url = f'https://uldk.gugik.gov.pl/?request=GetParcelById&id={plot_id}&result=geom_wkt&srid={srid}'
        response = requests.get(url)
        return response

#create coordinates list
def get_coordinates(plot_id, srid):
    #format response to be a list of tuples
    wkt = get_wkt(plot_id, srid).text.split(';')[1]
    list = wkt[9:-3].split(',')
    coordinates = [tuple(a.split(' ')) for a in list]
    return coordinates
