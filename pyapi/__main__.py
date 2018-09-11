import json
from flask import Flask
from flask_restful import request
import service
import requests_cache

app = Flask(__name__)

requests_cache.install_cache('currency_cache', backend='sqlite', expire_after=36000)

@app.route("/currency_converter")
def get():
    if 'output_currency' in request.args:
        return service.create_json(service.sign_to_abbreviation(request.args['input_currency']),
                                   service.sign_to_abbreviation(request.args['output_currency']),
                                   request.args['amount'])
    else:
        return service.create_json(request.args['input_currency'],
                                   "None",
                                   request.args['amount'])


if __name__ == "__main__":
    service.create_currencies_dict()
    app.run(debug=True)
