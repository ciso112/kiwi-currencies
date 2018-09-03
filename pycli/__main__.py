import json
import argparse
import requests


def create_json(input_currency, output_currency, amount):
    if input_currency == None or output_currency == None:
        return "Currency not recognized"
    # if input_currency contains ",", it means a currency sign has different currency representations
    if "," in input_currency:
        return "Input currency not clearly defined. Possible currencies with such symbol: " + input_currency
    d = {}
    d["input"] = {"amount": float(amount), "currency": input_currency}
    if output_currency == "None":
        output_currency = ",".join(list(currencies_symbols.values()))

    # if len(output_currency) > 1 or output_currency =="None":
    output_currencies = output_currency.split(",")
    for curr in output_currencies:
        if not curr == input_currency:
            # output_line =
            if "output" not in d:
                d["output"] = {}
            d["output"].update({curr: convert(input_currency, curr, amount)})

    return json.dumps(d, indent=4, separators=(',', ': '))

# global dictionary filled up at a start of an application
currencies_symbols = {}


def sign_to_abbreviation(curr):
    if curr != "None":
        for key, value in currencies_symbols.items():
            if curr == key:
                curr = value
                return curr
            else:
                return curr
    else:
        return curr


def create_currencies_dict():
    api_url = "https://free.currencyconverterapi.com/api/v6/currencies"
    response = requests.get(api_url)
    if response.status_code == 200:
        currencies = json.loads(response.content.decode('utf-8'))
        for key, value in currencies['results'].items():
            if 'currencySymbol' in value.keys():
                # because some currencies have the same symbol --> we append values to the same key
                if value['currencySymbol'] in currencies_symbols.keys():
                    new_currency = currencies_symbols.get(value['currencySymbol'])
                    currencies_symbols[value['currencySymbol']] = value['id'] + "," + new_currency
                else:
                    currencies_symbols[value['currencySymbol']] = value['id']
            else:
                pass
        return currencies_symbols
    else:
        return None


def convert(input_currency, output_currency, amount):
    if len(input_currency) and len(output_currency) == 3:
        rate = contact_api(input_currency, output_currency)
        return round(float(amount) * float(rate.get(input_currency+"_"+output_currency)), 2)
    else:
        return "Currency not recognized"


# external converter service
def contact_api(inp, out):
    api_url_base = 'http://free.currencyconverterapi.com/api/v5/convert'
    conversion = inp + "_" + out
    payload = {"q": conversion, "compact": "ultra"}
    response = requests.get(api_url_base, params=payload)

    if response.status_code == 200:
        print(response)
        return json.loads(response.content.decode('utf-8'))
    else:
        return None

if __name__ == "__main__":
    create_currencies_dict()
    parser = argparse.ArgumentParser()

    parser.add_argument('--amount', action="store", type=float, dest="amount", required=True)
    parser.add_argument('--input_currency', action="store", dest="input_currency", required=True)
    parser.add_argument('--output_currency', action="store", dest="output_currency")

    args = parser.parse_args()

    print(create_json(sign_to_abbreviation(format(args.input_currency)),
                      sign_to_abbreviation(format(args.output_currency)),
                      format(args.amount)))
