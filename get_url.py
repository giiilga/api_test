

def get_urls(valve_number, prediction_window):
    url_valve_pl = 'http://localhost/api/v1/kedro/valve_recommendation/versioned/7210-N297VRH00%s?min_tal_level=8&max_tal_level=10&model_version=2022-08-08T17.04.50.444Z'
    url_rh_pl = 'http://localhost/api/v1/kedro/rh_level_predictor/versioned/power_valuation?min_rh_level=4&max_rh_level=10&model_version=%s'
    url_valve = [url_valve_pl % x for x in valve_number]
    url_rh = [url_rh_pl % x for x in prediction_window]

    return url_valve, url_rh

# print(get_urls(valve_number, prediction_window))