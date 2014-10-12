import os
import numpy
import csv
from shapely.wkb import loads
from osgeo import ogr

year = 2004

path_1 = "/home/marko/Diplomski/Download_podaci/" + str(year) + "/" + str(year) + "_Crop_NDVI/"
piezo_path = "/home/marko/Diplomski/Download_podaci/piezometri/spacva_lokacije.shp"
csv_path = "/home/marko/Diplomski/Download_podaci/" + str(year) + "/" + str(year) +"_vrijednosti_NDVI.csv"

dirList_1 = sorted(os.listdir(path_1))

csv_file = open(csv_path, "wb")

shp_file = ogr.Open(piezo_path)
sloj = shp_file.GetLayerByName("spacva_lokacije")

def srednjak_piezo(file, x_koord, y_koord):
    polozajLista = [-231, 0, 231]
    vrijednostiLista = []
    for x in polozajLista:
        for y in polozajLista:        
            locationInfo = os.popen("gdallocationinfo " + path_1 + file + " -geoloc " + str(x_koord + x) + " " + str(y_koord + y)).read()
            locationInfo_float =  float(locationInfo.split(" ")[11])
            vrijednostiLista.append(locationInfo_float)   
    srednja_vrijednost = np.mean(vrijednostiLista)
    return srednja_vrijednost

pisanje_csv = csv.writer(csv_file, delimiter = ";")

lista_1 = []
lista_2 = ['naziv_rastera']

for file in dirList_1:
    lista_2.append(file[5:12])

lista_1.append(lista_2)  

piezometar = sloj.GetNextFeature()

while piezometar is not None:
    geometrijaCestice = loads(piezometar.GetGeometryRef().ExportToWkb())
    lista_3 = []
    x_koord = geometrijaCestice.x
    y_koord = geometrijaCestice.y
    piezo_broj = piezometar.id
    lista_3.append(piezo_broj)
    for file in dirList_1:
        if file.endswith(".tif"):
            sredina = srednjak_piezo(file, x_koord, y_koord)
            if sredina < 0.2:
                lista_3.append("Oblak!")
            else:
                lista_3.append(sredina)
    lista_1.append(lista_3)
    
    piezometar = sloj.GetNextFeature()
    
shp_file.Destroy()

pisanje_liste = zip(*lista_1)
for x in pisanje_liste:
    pisanje_csv.writerow(x)

csv_file.close()




