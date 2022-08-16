import requests
from time import time, sleep
from get_url import get_urls
from make_request import make_request

apihost = 'localhost'
username= 'admin@nexa.com'
password= '423fc72293d620bd3145'
valve_number = range(1,7)
model_version = (
    "15--2022-08-08T13.53.49.281Z",
    "30--2022-08-02T19.25.42.813Z",
    "45--2022-08-08T18.54.40.649Z",
    "60--2022-08-12T16.13.39.035Z"
    )
n_requests = 1
interval = 0

# get access tokem
request = requests.post(  # get access token
    f"http://{apihost}/api/v1/login/access-token",
    data={"username": username, "password": password},
)
response = request.json()
access_token = response["access_token"]
# print(request.text)

# makes a request to the database

# url = 'http://localhost/api/v1/kedro/valve_recommendation/?valve_selection=7210-N297VRH006&min_tal_level=8&max_tal_level=10'
# url = 'http://localhost/api/v1/kedro/rh_level_predictor/power_valuation?prediction_window=60&min_rh_level=4&max_rh_level=10'
url_valve, url_rh = get_urls(valve_number, model_version)

headers = {'accept': 'application/json', "Authorization": f"Bearer {access_token}"}

it_out = 0
it_in = 0
total_time = 0
print(f"interval between requests: {interval}s")


while True:

    it_out += 1
    print(f'\n--- Request Group no. {it_out} ---')
    for ircount, url in enumerate(url_rh):
        it_in +=1
        request_type_str = f'request {it_in}: rh_predictor w={model_version[ircount]} - '
        total_time, it_time, r = make_request(url, headers, total_time)
        print(request_type_str + f"code {r.status_code} - time = {it_time}")
        if r.status_code != 200:
            print(r.text)

    for ircount, url in enumerate(url_valve):
        it_in +=1
        request_type_str = f'request {it_in}: valve_rec. 00{valve_number[ircount]} - '
        total_time, it_time, r = make_request(url, headers, total_time)
        print(request_type_str + f"code {r.status_code} - time = {it_time}")
        if r.status_code != 200:
            print(r.text)
    
    if it_out >= n_requests:
        break
    sleep(interval)

# data = r.json()
# print(data)
print("\n average time for a request group: "+ str(total_time/it_out)+'s')