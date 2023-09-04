import requests as req
from concurrent.futures import ProcessPoolExecutor
import asyncio
import os

base_url = "http://localhost:5037/cv/"


def store_cv(cnpq_id):
    # print("sending put request for {}".format(cnpq_id))
    url = base_url + cnpq_id
    r = req.get(url)
    print(r.status_code)
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
    asyncio.run(main())