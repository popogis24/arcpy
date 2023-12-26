import json


json_path = r'C:\teste\teste.json'
url_base = r'https://gisepeprd2.epe.gov.br/arcgis/rest/services/Download_Dados_Webmap_EPE/GPServer/Extract%20Data%20Task/execute?f=json&env%3AoutSR=102100&Layers_to_Clip=%5B%22Subesta%C3%A7%C3%B5es%20-%20Expans%C3%A3o%20Planejada%22%2C%22Linhas%20de%20Transmiss%C3%A3o%20-%20Expans%C3%A3o%20Planejada%22%2C%22Subesta%C3%A7%C3%B5es%20-%20Base%20Existente%22%2C%22Linhas%20de%20Transmiss%C3%A3o%20-%20Base%20Existente%22%5D&Area_of_Interest=%7B%22geometryType%22%3A%22esriGeometryPolygon%22%2C%22features%22%3A%5B%7B%22geometry%22%3A%7B%22rings%22%3A%5B%5B%5B-9024700.796477927%2C-4794777.928925178%5D%2C%5B-9024700.796477927%2C1369104.031989796%5D%2C%5B-2449893.3715019543%2C1369104.031989796%5D%2C%5B-2449893.3715019543%2C-4794777.928925178%5D%2C%5B-9024700.796477927%2C-4794777.928925178%5D%5D%5D%2C%22spatialReference%22%3A%7B%22wkid%22%3A102100%7D%7D%7D%5D%2C%22sr%22%3A%7B%22wkid%22%3A102100%7D%7D&Feature_Format=Shapefile%20-%20SHP%20-%20.shp&Raster_Format=Tagged%20Image%20File%20Format%20-%20TIFF%20-%20.tif'


#download this json file and save it on this folder with teste.json as a name
import urllib.request
urllib.request.urlretrieve(url_base, r'C:\teste\teste.json')


with open(json_path, 'r') as json_file:
    data = json.load(json_file)

    url_file = data['results'][0]['value']['url']
    #download file for me
    print(url_file)
