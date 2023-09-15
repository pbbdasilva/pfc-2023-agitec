import argparse
import zipfile
import os

TMP_DIR = "tmp/"

'''
after we unzip the file, they all have the same name (curriculo.xml)
so we need to rename them to our format -> cv_{rank}_{cnpq_id}.xml
'''
def rename_cv(cnpq_id, rank):
    default_file_name = TMP_DIR + "curriculo.xml"
    new_file_name = "cv_{}_{}.xml".format(rank, cnpq_id)
    os.rename(default_file_name, new_file_name)

'''
cvs come zipped from lattes
'''
def unzip(rank):
    files = os.listdir(os.getcwd())
    # get zip only for the given rank
    cnpq_zips = [file for file in files if file.endswith('zip') and file.startswith(rank)]

    if len(cnpq_zips) == 0:
        print("No files for target rank were found")
        exit(1)

    for zipped_rank in cnpq_zips:
        with zipfile.ZipFile(zipped_rank,"r") as zip_ref:
            zip_ref.extractall(TMP_DIR)
        zipped_cvs = [file for file in os.listdir(os.getcwd() + "/" + TMP_DIR) if file.endswith(".zip")]
        for zipped_cv in zipped_cvs:
            with zipfile.ZipFile(TMP_DIR + zipped_cv, "r") as zip_ref:
                zip_ref.extractall(TMP_DIR)
                rename_cv(zipped_cv.replace(".zip", ""), rank)
    
    # after we rename it, we can delete the zip files
    for zipped_rank in cnpq_zips:
        os.remove(zipped_rank)
    for zipped_cv in os.listdir(TMP_DIR):
        os.remove(TMP_DIR + zipped_cv)
    os.rmdir(TMP_DIR)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Store resumes from current directory to mongodb')
    parser.add_argument('--rank', help='Rank parameter')
    args = parser.parse_args()
    rank = args.rank

    if not rank:
        print("Error: Rank parameter (--rank) is required.")
        exit(1)
    unzip(rank)