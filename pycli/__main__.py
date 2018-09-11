import service
import argparse


if __name__ == "__main__":
    service.create_currencies_dict()
    parser = argparse.ArgumentParser()
    # print(service.currencies_symbols)
    parser.add_argument('--amount', action="store", type=float, dest="amount", required=True)
    parser.add_argument('--input_currency', action="store", dest="input_currency", required=True)
    parser.add_argument('--output_currency', action="store", dest="output_currency")

    args = parser.parse_args()

    print(service.create_json(service.sign_to_abbreviation(format(args.input_currency)),
                              service.sign_to_abbreviation(format(args.output_currency)),
                              format(args.amount)))

