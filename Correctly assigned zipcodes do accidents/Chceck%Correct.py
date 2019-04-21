import pandas as pd

filepath='C://Users//grzechu//Desktop//TTU//ProjectsSpringGIT//BI_Project//BI-project//Correctly assigned zipcodes do accidents//'
x=pd.read_csv(filepath+'Accidents_XY_Zipcodes.csv')
x['diff']=x['wrong_zipcode']-x['correct_zipcode']

check=x[x['diff'] == 0].sum(axis=1)

(check.shape[0]/x.shape[0])*100
