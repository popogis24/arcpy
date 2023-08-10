import arcpy

try:
    workspace = arcpy.GetParameterAsText(0)
    arcpy.env.workspace = workspace
    feature_classes = arcpy.ListFeatureClasses()
    
    if not feature_classes:
        arcpy.AddWarning("Nenhuma feature class encontrada na pasta de trabalho.")
    else:
        for fc in feature_classes:
            nome_fc = fc
            output_fc_name = f"{fc}_NoZM"
            
            with arcpy.EnvManager(outputZFlag="Disabled", MDomain=None, outputMFlag="Disabled"):
                fc_new = arcpy.conversion.FeatureClassToFeatureClass(
                    in_features=fc,
                    out_path=workspace,
                    out_name=output_fc_name,
                    where_clause="",
                    field_mapping="",
                    config_keyword=""
                )
                
                arcpy.management.Delete(in_data=fc)
                arcpy.management.Rename(fc_new, nome_fc)
            
except arcpy.ExecuteError:
    arcpy.AddError(arcpy.GetMessages())
except Exception as e:
    arcpy.AddError(str(e))
