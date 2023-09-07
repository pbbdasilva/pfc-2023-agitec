import requests as req
from concurrent.futures import ProcessPoolExecutor
import asyncio
import os
import argparse

base_url = "http://localhost:5037/cv/"

'''
    async calls to lattes-core api
    the base_url should be set to the endpoint where the api is running
    if you receive connection refused when calling this method it is probably
    wrong url or api is not running

    will use cvs in current directory
'''
def store_cv(cnpq_id):
    # print("sending put request for {}".format(cnpq_id))
    url = base_url + cnpq_id
    try:
        r = req.get(url)
    except req.exceptions.ConnectionError as e:
        print("error for {}".format(cnpq_id))
        print(e)
    
    if r.status_code != 200:
        print("error for {}".format(cnpq_id))

async def main():
    files = os.listdir(os.getcwd())
    cnpq_ids = [file.replace("cv_", "").replace(".xml", "") for file in files if file.startswith('cv_') and file.endswith('xml')]

    loop = asyncio.get_event_loop()
    with ProcessPoolExecutor() as executor:
        tasks = [loop.run_in_executor(None, store_cv, cv_id) for cv_id in cnpq_ids]
        await asyncio.gather(*tasks)
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Store resumes from current directory to mongodb')
    parser.add_argument('--url', help='API endpoint')
    args = parser.parse_args()
    url = args.url

    # if no url is defined, we assume the correct one is already in the script
    if url:
        base_url = url

    asyncio.run(main())