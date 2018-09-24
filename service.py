import json
import logging
import time
import requests
import requests_cache

# global dictionary filled up at a start of an application
currencies_symbols = {}

requests_cache.install_cache('currency_cache', backend='sqlite', expire_after=21600)    #expires after 6 hours

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)


# creates an output in JSON format
def create_json(input_currency, output_currency, amount):
    logging.info(" FUNC: create_json parameters: inp:%s out:%s am=%s", input_currency, output_currency, amount)
    if input_currency == None:
        return "Input currency not recognized \n"
    if output_currency == None:
        return "Output currency not recognized \n"

    # if input_currency contains ",", it means a currency sign has different currency representations
    # f.e.: symbol £ can be used for GIP,SYP,SHP,LBP,EGP,GBP,FKP
    if "," in input_currency:
        return "Input currency not clearly defined. Possible currencies with such symbol: " + input_currency

    dict = {}
    dict["input"] = {"amount": float(amount), "currency": input_currency}

    # in case no output currencies, prepare to convert to all known currencies
    if output_currency == "None":
        output_currency = ",".join(list(currencies_symbols.values()))

    output_currencies = output_currency.split(",")
    for curr in output_currencies:
        if curr != input_currency:
            if "output" not in dict:
                dict["output"] = {}
            dict["output"].update({curr: convert(input_currency, curr, amount)})

    return json.dumps(dict, indent=4, separators=(',', ': '), sort_keys=True)


# input/output can be in a currency symbol format, but we will need a three-letter currency name
def sign_to_abbreviation(curr):
    logging.info(" FUNC: sign_to_abbreviation parameters: curr:%s", curr)
    if len(curr) == 3:
        return curr
    if curr != "None":
        for key, value in currencies_symbols.items():
            if curr == key:
                return value
        return None
    return curr


# function run at the start of the program to get the known currencies and their symbols
def create_currencies_dict():
    if not currencies_symbols:
        logging.info(" FUNC: create_currencies_dict")
        api_url = "https://free.currencyconverterapi.com/api/v6/currencies"

        try:
            response = requests.get(api_url)
        except requests.exceptions.ConnectionError as e:
            logging.error(" FUNC: create_currencies_dict CONNECTION ERROR: ", e)
            return None

        # if response.status_code != 200:
        #     return None

        currencies = json.loads(response.content.decode('utf-8'))
        for key, value in currencies['results'].items():
            if 'currencySymbol' in value.keys():
                # because some currencies have the same symbol --> we append values to the same key
                if value['currencySymbol'] in currencies_symbols.keys():
                    new_currency = currencies_symbols.get(value['currencySymbol'])
                    currencies_symbols[value['currencySymbol']] = value['id'] + "," + new_currency
                else:
                    currencies_symbols[value['currencySymbol']] = value['id']
        return currencies_symbols


def convert(input_currency, output_currency, amount):
    logging.info(" FUNC: convert parameters: inp:%s out:%s am=%s", input_currency, output_currency, amount)
    if len(input_currency) and len(output_currency) == 3:

        # try:
            # returns dictionary with exactly 1 key-value pair
        rate = contact_api(input_currency, output_currency)
        # except ConnectionError as e:
        #     logging.error(" FUNC: convert ERROR Exception:", e)
        #     return "Service unavailable"
        logging.info(" FUNC: convert rate: %s", rate)
        if rate:
            return round(float(amount) * float(rate.get(input_currency+"_"+output_currency)), 2)
    else:
        return "Currency not recognized"


# external converter service
def contact_api(inp, out):
    logging.info(" FUNC: contact_api parameters: inp:%s out:%s", inp, out)
    api_url_base = 'http://free.currencyconverterapi.com/api/v5/convert'
    conversion = inp + "_" + out
    payload = {"q": conversion, "compact": "ultra"}
    try:
        start_time = time.time()
        response = requests.get(api_url_base, params=payload, timeout=1)  # we have 1 sec to get a response
        logging.info(" FUNC: contact_api request elapsed time: %s", time.time() - start_time)
    except requests.exceptions.ConnectionError as e:
        logging.error(" FUNC: contact_api CONNECTION ERROR: ", e)
        return None

    logging.info(" FUNC: contact_api Loading from CACHE: %s", response.from_cache)
    if response.status_code == 200:
        return json.loads(response.content.decode('utf-8'))
    return None
