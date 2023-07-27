
import arcpy

arcpy.env.workspace = r"R:\09-Banco_De_Dados_Geografico\01-Clientes\Neoenergia\LT_CPS_EIA\LT_CPS_SID_EIA.gdb"

rasters = arcpy.ListRasters()
for raster in rasters:
    filename = raster
    arcpy.management.CopyRaster(
        in_raster=raster,
        out_rasterdataset=fr"R:\09-Banco_De_Dados_Geografico\01-Clientes\Neoenergia\LT_CPS_EIA\PROTOCOLO\Dados_Protocolo\Metadado\Raster\{filename}",
        config_keyword="",
        background_value=None,
        nodata_value="",
        onebit_to_eightbit="NONE",
        colormap_to_RGB="NONE",
        pixel_type="",
        scale_pixel_value="NONE",
        RGB_to_Colormap="NONE",
        format="TIFF",
        transform="NONE",
        process_as_multidimensional="CURRENT_SLICE",
        build_multidimensional_transpose="NO_TRANSPOSE"
    )
    
    print(raster, " - Concluído")
