import os
import arcpy

folder = fr'C:\Users\anderson.souza\Documents\MSP_Data\Vector_Data\SIMMAM_2021\wetransfer_mma_tartarugas_2023-07-10_0307\MMA Corais\coral'
output_path=

def get_shapefiles_recursive(folder_path):
    """Recursively searches for shapefiles in a folder and its subfolders."""
    shapefiles = []
    for dirpath, dirnames, filenames in os.walk(folder_path):
        for filename in filenames:
            if filename.endswith('.shp'):
                shapefiles.append(os.path.join(dirpath, filename))
    return shapefiles
    
shapefiles = get_shapefiles_recursive(folder)

arcpy.management.Merge(inputs=shapefiles, output=output_path)
