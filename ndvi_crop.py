import os

year = 2004

path_1 = "/home/marko/Diplomski/Download_podaci/" + str(year) + "/"  + str(year) +"_MODIS/"
path_2 = "/home/marko/Diplomski/Download_podaci/radno/"
path_3 = "/home/marko/Diplomski/Download_podaci/" + str(year) + "/" +str(year) + "_NDVI/"
path_4 = "/home/marko/Diplomski/Download_podaci/" + str(year) + "/" + str(year) + "_Crop_NDVI/"
dirList_1 = sorted(os.listdir(path_1))
dirList_3 = sorted(os.listdir(path_3))

def izdvajanje(file):
    izdvajanje_b01 = "gdal_translate -ot Float32 -of HDF4Image HDF4_EOS:EOS_GRID:" + '"' + path_1 + file + '"' + ":MOD_Grid_250m_Surface_Reflectance:sur_refl_b01 " + path_2 + "modis_b01_" + file[9:16] +".hdf"
    izdvajanje_b02 = "gdal_translate -ot Float32 -of HDF4Image HDF4_EOS:EOS_GRID:" + '"' + path_1 + file + '"' + ":MOD_Grid_250m_Surface_Reflectance:sur_refl_b02 " + path_2 + "modis_b02_" + file[9:16] +".hdf"
    os.system(izdvajanje_b01)
    os.system(izdvajanje_b02)

def NDVI_Crop(file):
    izdvajanje(file)
    dirList_2 = sorted(os.listdir(path_2))
    modis_b01 = path_2 + dirList_2[0]
    modis_b02 = path_2 + dirList_2[2]
    file_naziv = "NDVI_" + file[9:16]
    os.system( "gdal_calc.py -A " + modis_b01 +' -B ' + modis_b02 + " --format=HDF4Image --outfile=" + path_3 + file_naziv + ".hdf " + '--calc="(B-A)/(A+B)" --overwrite')
    os.system("rm " + path_2 + "*")
    dirList_3 = sorted(os.listdir(path_3))
    os.system("gdalwarp -te 1439512 4986866 1515727 5043853 " + path_3 + file_naziv + ".hdf" + " " + path_4 + "crop_" + file[9:16] + ".tif" + " -overwrite")
    

for moj_file in dirList_1:
    if moj_file.endswith(".hdf"):
        NDVI_Crop(moj_file)
