from data_collector import import_process_data

def main():
    path_zip=input('Enter the path to the folder called Zipcodes (it is in files folder)')
    output=input('Enter where you wanna save your file')
    
    final_df=import_process_data(path_zip)
    final_df.to_csv(output + 'final_data.csv')

main()