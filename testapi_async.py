import aiohttp
import asyncio

import requests
from time import time, sleep
import asyncio
import aiohttp
from get_url import get_urls

apihost = 'localhost'
username= 'admin@nexa.com'
password= '423fc72293d620bd3145'
n_requests = 10
interval = 0
model_version = (
    "60--2022-08-08T17.04.50.444Z",
    )
valve_number = range(1,7)

# url = 'http://localhost/api/v1/kedro/valve_recommendation/?valve_selection=7210-N297VRH006&min_tal_level=8&max_tal_level=10'
# url = 'http://localhost/api/v1/kedro/rh_level_predictor/power_valuation?prediction_window=%s&min_rh_level=4&max_rh_level=10'
url_valve, url_rh = get_urls(valve_number, model_version)

# get access tokem
request = requests.post(  # get access token
    f"http://{apihost}/api/v1/login/access-token",
    data={"username": username, "password": password},
)
response = request.json()
access_token = response["access_token"]
headers = {'accept': 'application/json', "Authorization": f"Bearer {access_token}"}

start_time = time()


async def main():
    it_out = 0
    it_in = 0
    total_time = 0

    async with aiohttp.ClientSession() as session:

        
        for it_out in range(1, n_requests+1):

            print(f'\n--- Request Group no. {it_out} ---')
            for ircount, url in enumerate(url_rh):
                it_in += 1
                start = time()
                async with session.get(url, headers=headers) as resp:
                    result = await resp.text()
                    run_time = time() - start
                    total_time += run_time
                    print(f"request {it_in}: rh_predictor w={model_version[ircount]} - code {resp.status} - time: {run_time}")
                    if resp.status != 200:
                        print(result)

            for ircount, url in enumerate(url_valve):
                it_in += 1
                start = time()
                async with session.get(url, headers=headers) as resp:
                    result = await resp.text()
                    run_time = time() - start
                    total_time += run_time
                    print(f"request {it_in}: valve_rec. 00{valve_number[ircount]} - code {resp.status} - time: {run_time}")
                    if resp.status != 200:
                        print(result)

    return it_in, it_out, total_time

it_in, it_out, total_time = asyncio.run(main())
print("\n--- %s seconds total ---" % (time() - start_time))
print(f"average time per group = {total_time/it_out}\n")