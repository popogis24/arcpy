
""""
1.	Tenha esses parametros (api_name: str, insert_table_name: str, schema_integration: str, schema_backup: str):
	2.	Le um shapefile/geojson (usando o "api_name")
	3.	Aplica possiveis correções de geometria/blah (isso se precisar)
	4.	Faz o backup da tabela no "schema_backup"
	5.	Deleta o conteudo da tabela(não a tabela) "schema_integration"
	6.	Da integrate

"""

import os
import arcpy
import arcpy.conversion as cs
import arcpy.management as mn
import arcpy.analysis as an

class Layer():
    def __init__(self, api_name: str, insert_table_name: str, schema_backup: str, schema_integration: str):
        self.api_name = api_name
        self.schema_backup = schema_backup
        self.schema_integration = schema_integration
        self.data_type = self.get_data_type()


    def get_data_type(self):
        if self.api_name.endswith('.shp'):
            return 'shapefile'
        elif self.api_name.endswith('.geojson'):
            return 'geojson'
        else:
            raise Exception('Formato de arquivo não suportado')

    def repair_geometry(self):
        mn.RepairGeometry(in_features=self.api_name)

    def make_backup_table(self):
        endereco_tabela_backup = os.path.join(self.schema_backup, self.insert_table_name)
        mn.CopyFeatures(in_features=self.api_name, out_feature_class=endereco_tabela_backup)

    def delete_content(self):
        endereco_tabela = os.path.join(self.schema_integration, self.insert_table_name)
        mn.DeleteFeatures(in_features=endereco_tabela)
    
    def integrate_content(self):
        endereco_tabela = os.path.join(self.schema_integration, self.insert_table_name)
        tabela_atualizada = mn.Append(inputs=self.api_name, target=endereco_tabela, schema_type='TEST')
        mn.AddGlobalIDs(in_datasets=tabela_atualizada)

if __name__ == "__main__":
    api_name = "caminho/para/seu/arquivo.shapefile"
    insert_table_name = "nome_da_tabela"
    schema_backup = "caminho/para/backup"
    schema_integration = "caminho/para/integracao"

    minha_camada = Layer(api_name, insert_table_name, schema_backup, schema_integration)

    minha_camada.repair_geometry()
    minha_camada.make_backup_table()
    minha_camada.delete_content()
    minha_camada.integrate_content()


    
	