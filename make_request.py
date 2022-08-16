from time import time
import requests


def make_request(url, headers, total_time):
    start = time()
    r = requests.get( url, headers=headers )
    it_time = time() - start
    total_time += it_time
    # print(
    #     request_type +
    #     f" - code {r.status_code} - time = {it_time}"
    #     )
    return total_time, it_time, r