import arcpy
import os
import zipfile

arcpy.env.overwriteOutput = True
input = arcpy.GetParameterAsText(0)
workspace = arcpy.GetParameterAsText(1)
num_lines_per_div = int(arcpy.GetParameterAsText(2))  # Número de linhas por divisão

# Calculate the number of features in the input
result = arcpy.GetCount_management(input)
count = int(result.getOutput(0))

# Divide the number of features by num_lines_per_div
div = count // num_lines_per_div + (1 if count % num_lines_per_div != 0 else 0)

# Transform the input into a layer
arcpy.MakeFeatureLayer_management(input, "try3_SnapOff20")

# Create a loop that will run 'div' times
for i in range(div):
    # Calculate the range for selection
    start_range = i * num_lines_per_div + 1
    end_range = (i + 1) * num_lines_per_div

    # Select features using the appropriate range
    arcpy.management.SelectLayerByAttribute(
        in_layer_or_view='try3_SnapOff20',
        selection_type="NEW_SELECTION",
        where_clause="div >= {} AND div <= {}".format(start_range, end_range),
        invert_where_clause=None
    )
    
    # Export the selected features to a shapefile
    output_shapefile = arcpy.FeatureClassToFeatureClass_conversion(
        in_features='try3_SnapOff20',
        out_path=workspace,
        out_name='SIGAM_Div_{}'.format(i)
    ).getOutput(0)  # Get the actual path of the output shapefile
    
    # Create a zip file for the shapefile
    zip_filename = 'SIGAM_Div_{}.zip'.format(i)
    zip_path = os.path.join(workspace, zip_filename)
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zip:
        for file_suffix in ['.shp', '.dbf', '.shx', '.prj']:
            file_path = output_shapefile.replace('.shp', file_suffix)
            zip.write(file_path, os.path.basename(file_path))
    
    # Clean up - delete the shapefile
    arcpy.Delete_management(output_shapefile)

    # Adiciona mensagem de progresso
    arcpy.AddMessage("Divisão {} de {} concluída".format(i + 1, div))

    # Adiciona um emoji aleatório
    arcpy.AddMessage("🤪")
    

# Clean up - delete the layer
arcpy.Delete_management("try3_SnapOff20")
