import arcpy

class LT_X_AreaProcessor:
    def __init__(self, tema, fields_interesse, lt, unidade, output):
        self.tema = tema
        self.fields_interesse = fields_interesse
        self.lt = lt
        self.unidade = unidade
        self.output = output

    def dissolve_tema(self):
        arcpy.Dissolve_management(self.tema, 'tema_dissolve', self.fields_interesse)

    def intersect_tema_lt(self):
        arcpy.Intersect_analysis([self.lt, 'tema_dissolve'], 'lt_x_area')

    def add_extensao_field(self):
        arcpy.AddField_management('lt_x_area', 'extensao', 'FLOAT')

    def calculate_extensao(self):
        if self.unidade == 'metros':
            arcpy.CalculateField_management('lt_x_area', 'extensao', '!shape.length@meters!', 'PYTHON')
        elif self.unidade == 'kilometros':
            arcpy.CalculateField_management('lt_x_area', 'extensao', '!shape.length@kilometers!', 'PYTHON')
        elif self.unidade == 'milhas':
            arcpy.CalculateField_management('lt_x_area', 'extensao', '!shape.length@miles!', 'PYTHON')
        elif self.unidade == 'pes':
            arcpy.CalculateField_management('lt_x_area', 'extensao', '!shape.length@feet!', 'PYTHON')
        elif self.unidade == 'jardas':
            arcpy.CalculateField_management('lt_x_area', 'extensao', '!shape.length@yards!', 'PYTHON')

    def generate_output(self):
        arcpy.CopyFeatures_management('lt_x_area', self.output)

def main():
    arcpy.OverwriteOutput = True
    arcpy.env.workspace = r'C:\Users\anderson.souza\Documents\CHESF\Piloto_quantitativo\workspace'
    
    tema = arcpy.GetParameterAsText(0)
    fields_interesse = arcpy.GetParameterAsText(1)
    lt = arcpy.GetParameterAsText(2)
    unidade = arcpy.GetParameterAsText(3)
    output = arcpy.GetParameterAsText(4)
    
    processor = LT_X_AreaProcessor(tema, fields_interesse, lt, unidade, output)
    processor.dissolve_tema()
    processor.intersect_tema_lt()
    processor.add_extensao_field()
    processor.calculate_extensao()
    processor.generate_output()

if __name__ == "__main__":
    main()
