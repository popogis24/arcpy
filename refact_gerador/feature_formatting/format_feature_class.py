import os
import arcpy
import arcpy.management as mn
import arcpy.analysis as an
from refact_gerador import settings


class Format_Feature_Class():
    def __init__(self, analyzed_product, feature_class, fields_to_dissolve, workspace, storage_dataset):
        
        self.analyzed_product = analyzed_product
        self.feature_class = feature_class
        self.fields_to_dissolve = fields_to_dissolve
        self.storage_dataset = storage_dataset
        
        self.dissolved_data_folder = os.path.join(os.path.dirname(self.workspace))/"dissolved_data"
        os.makedirs(self.workspace, exist_ok=True)

        self.feature_class_name = os.path.basename(self.feature_class)
    
    def format_fields(self):
        formatted_field = self.fields_to_dissolve.split(";")
        return formatted_field

    def repair_geometry(self):
        mn.RepairGeometry(self.feature_class)
    
    def clip_feature_class(self):
        area_of_interest = an.PairwiseBuffer(
            in_features=self.feature_class,
            out_feature_class=fr"{self.workspace}\buffer",
            buffer_distance_or_field=50000,
            dissolve_option="ALL")

        clipped_feature_class = an.PairwiseClip(
            in_features=self.feature_class,
            clip_features=area_of_interest,
            out_feature_class=fr"{self.workspace}\{self.feature_class_name}_clipped_data")
        return clipped_feature_class

    def dissolve(self):
        dissolved_feature_class = mn.PairwiseDissolve(
            in_features=self.clip_feature_class(),
            out_feature_class=fr"{self.dissolved_data}\{self.feature_class_name}_dissolved",
            dissolve_field=self.format_fields)
        return dissolved_feature_class

    def set_state_boundaries(self):
        uf_address = "BR_UF_2022.shp"
        feature_class_with_state_boundaries = mn.PairwiseIntersect(
            in_features=[self.dissolve(), uf_address],
            out_feature_class=fr"{self.workspace}\{self.feature_class_name}_dissolved_byUF")

        return feature_class_with_state_boundaries
    
    def set_municipal_boundaries(self):
        municipio_address = "BR_Municipios_2022.shp"
        feature_class_with_municipal_boundaries = mn.PairwiseIntersect(
            in_features=[self.dissolve(), municipio_address],
            out_feature_class=fr"{self.workspace}\{self.feature_class_name}_dissolved_byMunicipio")
    
        return feature_class_with_municipal_boundaries
    
    def store_shapefile_in_database(self):
        mn.FeatureClassToFeatureClass(
            in_features=self.set_state_boundaries(),
            out_location=self.storage_dataset,
            out_name=self.feature_class_name)
        
        arcpy.AddMessage(f"Shapefile {self.feature_class_name} stored in {self.storage_dataset}")
