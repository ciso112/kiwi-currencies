import service
import unittest
import logging
import mock


logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

class TestConverter(unittest.TestCase):

    def setUp(self):
        service.create_currencies_dict()

    def test_sign_to_abbreviation(self):
        logging.info(" TEST: test_sign_to_abbreviation")
        assert service.sign_to_abbreviation("€") == "EUR"
        # test case for multiple-currencies sign, order of output is not guaranteed; TODO:could get sorted
        # 'GIP,SYP,SHP,LBP,EGP,GBP,FKP': 7 * 3-letter symbol + 6 commas = 27
        assert len(service.sign_to_abbreviation("£")) == 27

    def simple_contact_api(self, inp, out):
        logging.info(" TEST: simple_contact_api")
        if inp == "USD" and out == "EUR":
            return 0.863
        if inp == "USD" and out == "JPY":
            return 111.509
        if inp == "EUR" and out == "USD":
            return 1.159
        if inp == "EUR" and out == "JPY":
            return 129.223
        if inp == "JPY" and out == "EUR":
            return 0.008
        if inp == "JPY" and out == "USD":
            return 0.009
        return None

    @mock.patch('service.contact_api', side_effect=simple_contact_api)
    def test_contact_api(self, contact_api_function):
        logging.info(" TEST: test_contact_api %s", contact_api_function)
        assert not contact_api_function.called

        assert service.contact_api(None, "EUR", "USD") == 1.159

    # unfinished - service calls contact_api to ger conversion rate - this needs to be mocked (TODO)

    # @mock.patch('service.contact_api', side_effect=simple_contact_api)
    # def test_convert(self, contact_api):
    #     logging.info(" TEST: test_convert %s", contact_api)
    #     assert service.convert("EUR", "USD", 1) == 1.159

    def test_unknown_input(self):
        logging.info(" TEST: test_unknown_input")
        self.assertEquals(service.convert(output_currency="EgUR", input_currency="USD", amount=45.2),
                          "Currency not recognized")


if __name__ == '__main__':
    unittest.main()
