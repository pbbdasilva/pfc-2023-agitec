import zipfile
import os

'''
after we unzip the file, they all have the same name (curriculo.xml)
so we need to rename them to our format -> cv_{cnpq_id}.xml
'''
def rename_cv(cnpq_id):
    default_file_name = "curriculo.xml"
    new_file_name = "cv_{}.xml".format(cnpq_id)
    os.rename(default_file_name, new_file_name)

'''
cvs come zipped from lattes
'''
def unzip():
    files = os.listdir(os.getcwd())
    cnpq_zips = [file for file in files if file.endswith('zip')]

    for zipped_cv in cnpq_zips:
        with zipfile.ZipFile(zipped_cv,"r") as zip_ref:
            zip_ref.extractall()
        
        cnpq_id = zipped_cv.replace(".zip", "")
        rename_cv(cnpq_id)
    
    # after we rename it, we can delete de zipped file
    for zipped_cv in cnpq_zips:
        os.remove(zipped_cv)

def main():
    unzip()

if __name__ == '__main__':
    main()