# Currency Converter
A practical task for a position of Junior Python Developer.
Task entry: https://gist.github.com/MichalCab/c1dce3149d5131d89c5bbddbc602777c

## Prerequisites
python 3.4

## Requirements
Required libraries can be found in `requirements.txt` and installed via `pip3 install -r requirements.txt`

## Run application
Run a `__main__.py` file, either in pyapi or pycli folder depending on a desired form of usage.

## Parameters
- `amount` - amount which we want to convert - float
- `input_currency` - input currency - 3 letters name or currency symbol
- `output_currency` - requested/output currency - 3 letters name or currency symbol

Note that a single currency symbol can represent several currencies:
- in case this happens with `output_currency`, convert to all known currencies with such symbol
- in case this happens with `input_currency`, conversion is not performer. Rather, an info message with currencies having such symbol is shown, so a user can specify `input_currency` more precisely

## Output
Possibilities:
- json with a following structure:

Single input and output currency:
```
{
    "input": {
        "amount": <float>,
        "currency": <3 letter currency code>
    }
    "output": {
        <3 letter currency code>: <float>
    }
}
```

Single input and multiple output currencies (in case a currency sign represents more currencies):
```
{
    "input": {
        "amount": <float>,
        "currency": <3 letter currency code>
    }
    "output": {
        <corresponding 3 letter currency code>: <float>
        <corresponding 3 letter currency code>: <float>
        .
        .
    }
}
```

Single input and no output currency - convert to all known currencies:
```
{
    "input": {
        "amount": <float>,
        "currency": <3 letter currency code>
    }
    "output": {
        <3 letter currency code>: <float>
        <3 letter currency code>: <float>
        <3 letter currency code>: <float>
        .
        .
    }
}
```

- Info message:

Multiple input currencies (in case a currency sign represents more currencies):
```
"Input currency not clearly defined. Possible currencies with such symbol: <possible currencies>"
```

Unknown input currency:
```
"Input currency not recognized"
```

Unknown output currency:
```
"Output currency not recognized"
```

## Examples

### CLI
```
./currency_converter.py --amount 100.0 --input_currency EUR --output_currency CZK
{
     "input": {
        "amount": 100.0,
        "currency": "EUR"
    },
    "output": {
        "CZK": 2561.78
    }
}
```

```
./currency_converter.py --amount 0.9 --input_currency € --output_currency AUD
{
    "input": {
        "amount": 0.9,
        "currency": "EUR"
    },
    "output": {
        "AUD": 1.46
    }
}
```

```
./currency_converter.py --amount 10.92 --input_currency zł
{
    "input": {
        "amount": 10.92,
        "currency": "PLN"

    },
    "output": {
        "HRK": 18.84,
        "UZS": 24006.34,
        "RUB": 196.93,
        "BOB": 20.64,
        .
        .
        .
    }
}
```

```
./currency_converter.py --amount 10.92 --input_currency EUR --output_currency £
{
    "input": {
        "amount": 10.92,
        "currency": "EUR"
    },
    "output": {
        "GBP": 9.79,
        "FKP": 9.77,
        "LBP": 19462.11,
        "SHP": 16.97,
        "SYP": 6617.36,
        "EGP": 230.18,
        "GIP": 9.77
    }
}
```

```
./currency_converter.py --amount 10.92 --input_currency Nonsense_curr
Input currency not recognized
```


### API

Note: When using curl, currencies symbols are not decoded properly and therefore not recognised. A recommended tool is Postman.

```
GET /currency_converter?amount=4.5&input_currency=₱&output_currency=VEF HTTP/1.1
{
    "input": {
        "amount": 4.5,
        "currency": "PHP"
    },
    "output": {
        "VEF": 20633.77
    }
}
```

```
GET /currency_converter?amount=10.92&input_currency=£ HTTP/1.1
Input currency not clearly defined. Possible currencies with such symbol: SHP,FKP,EGP,LBP,SYP,GIP,GBP
```

```
GET /currency_converter?amount=10.92&input_currency=₦ HTTP/1.1
{
    "input": {
        "amount": 10.92,
        "currency": "NGN"
    },
    "output": {
        "HRK": 0.19,
        "UZS": 241.47,
        "RUB": 1.98,
        "BOB": 0.21,
        "TZS": 68.63,
        "GBP": 0.02,
        "GIP": 0.02,
        "GTQ": 0.23,
        .
        .
        .
        }
}
```







