import pandas as pd

class FBAPI:

    def __init__(self):
        self.df = None

    def load_df(self, filename, table='A1'):
        self.df = pd.read_excel(filename, table)
    
    def make_fb_df(self):
        column_dct = {}

        column_dct['Country'] = self.df['A1 Size and composition, 2020/21 and 2011'].iloc[5:50]
        column_dct['Percentage of Population Foreign Born'] = pd.to_numeric(self.df['Unnamed: 2'].iloc[4:50], errors='coerce').round(2)
        column_dct['Foreign Born Population Aged 0-14'] = pd.to_numeric(self.df['Unnamed: 3'].iloc[5:50], errors='coerce').round(2)
        column_dct['Foreign Born Population Aged 65+'] = pd.to_numeric(self.df['Unnamed: 4'].iloc[5:50], errors='coerce').round(2)
        column_dct['Foreign Born Female Population'] = pd.to_numeric(self.df['Unnamed: 5'].iloc[5:50], errors='coerce').round(2)
        column_dct['Mean Foreign Born Household Size'] = pd.to_numeric(self.df['Unnamed: 6'].iloc[4:50], errors='coerce').round(2)

        # Creating the DataFrame
        fb_df = pd.DataFrame(column_dct).reset_index().drop(0).drop('index', axis=1)

        return fb_df


    def make_employment_df(self):


        column_dct = {}

        column_dct['Country'] = self.df['Table B8. Unemployment rates, 2021'].iloc[4:50]
        column_dct['Foreign Born Unemployment Percentage'] = pd.to_numeric(self.df['Unnamed: 1'].iloc[3:50], errors='coerce').round(2)
        column_dct['Native Born Unemployment Percentage'] = pd.to_numeric(self.df['Unnamed: 10'].iloc[3:50], errors='coerce').round(2)

        employment_df = pd.DataFrame(column_dct).reset_index().drop(0).drop('index', axis=1)

        return employment_df
    
    def make_education_df(self):


        column_dct = {}

        column_dct['Country'] = self.df['Table B2. Distribution by level of education and gender, 2020'].iloc[4:50]

        column_dct['Foreign Born ISCED (0-2)'] = pd.to_numeric(self.df['Unnamed: 1'].iloc[3:49] + self.df['Unnamed: 4'].iloc[3:49], errors='coerce').round(2)
        column_dct['Foreign Born ISCED (3-4)'] = pd.to_numeric(self.df['Unnamed: 2'].iloc[3:49] + self.df['Unnamed: 5'].iloc[3:49], errors='coerce').round(2)
        column_dct['Foreign Born ISCED (5+)'] = pd.to_numeric(self.df['Unnamed: 3'].iloc[3:49] + self.df['Unnamed: 6'].iloc[3:49], errors='coerce').round(2)

        column_dct['Native Born Total ISCED (0-2)'] = pd.to_numeric(self.df['Unnamed: 7'].iloc[3:49] + self.df['Unnamed: 10'].iloc[3:49], errors='coerce').round(2)
        column_dct['Native Born ISCED (3-4)'] = pd.to_numeric(self.df['Unnamed: 8'].iloc[3:49] + self.df['Unnamed: 11'].iloc[3:49], errors='coerce').round(2)
        column_dct['Native Born ISCED (5+)'] = pd.to_numeric(self.df['Unnamed: 9'].iloc[3:49] + self.df['Unnamed: 12'].iloc[3:49], errors='coerce').round(2)

        education_df = pd.DataFrame(column_dct).reset_index().drop(0).drop('index', axis=1)

        return education_df
    
    def make_poverty_df(self):

        column_dct = {}

        column_dct['Country'] = self.df['C1 Relative poverty rates, 2020'].iloc[4:49]
        column_dct['Percentage of Foreign Born in Poverty'] = pd.to_numeric(self.df['Unnamed: 1'].iloc[3:49], errors='coerce').round(2)
        column_dct['Percentage of Native Born in Poverty'] = pd.to_numeric(self.df['Unnamed: 8'].iloc[3:49], errors='coerce').round(2)

        poverty_df = pd.DataFrame(column_dct).reset_index().drop(0).drop('index', axis=1)

        return poverty_df
    
    def make_literacy_df(self):
        
        column_dct = {}

        column_dct['Country'] = self.df['Table E2. Reading literacy, 2018'].iloc[4:49]
        column_dct['Foreign Born Average PISA Score'] = pd.to_numeric(self.df['Unnamed: 1'].iloc[3:49], errors='coerce').round(2)
        column_dct['Native Born Average PISA Score'] = pd.to_numeric(self.df['Unnamed: 11'].iloc[3:49], errors='coerce').round(2)

        literacy_df = pd.DataFrame(column_dct).reset_index().drop(0).drop('index', axis=1)
        
        return literacy_df
    
    