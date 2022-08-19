from unittest import TestCase
from unittest.mock import patch

from main import generate_id_from_url, shorten_url


class UrlShortenerTestCase(TestCase):
    def setUp(self):
        self.testfunc = generate_id_from_url
        
    def test_01_hashing_function(self):
        # test for generating md5 hash with base64 encoding for a long url
        answer = self.testfunc("https://www.yahoo.com/")
        #print(answer)
        self.assertEqual(answer, "Y9H6PWS")

    def test_02_hashing_function(self):
        # test for generating md5 hash with base64 encoding for a long url
        answer = self.testfunc("https://www.w3schools.com/python/python_mysql_create_table.asp")
        self.assertEqual(answer, "ZN/imJD")

    def test_03_hashing_function(self):
        # test for generating md5 hash with base64 encoding for a long url
        answer = self.testfunc("https://www.delftstack.com/howto/python/split-integer-into-digits-python/")
        self.assertEqual(answer, "R1KYEAf")

    @patch('main.exists_id', return_value=True)
    def test_04_mock_exists_id(self, exists_id):
        # test for the return value of exists_id function
        self.assertEqual(exists_id("R1KYEAf"), True)

    @patch('main.store_id_url', return_value="Y9H6PWS")
    def test_05_mock_store_id_url(self, store_id_url):
        # test for the return value of store_id_url function
        self.assertEqual(store_id_url("Y9H6PWS","https://www.yahoo.com/"), "Y9H6PWS")

    @patch('main.shorten_url', return_value="http://127.0.0.1:5000/?id=Y9H6PWS")
    def test_06_mock_shorten_url(self, shorten_url):
        # test for the return value of shorten_url function
        self.assertEqual(shorten_url("https://www.yahoo.com/"), "http://127.0.0.1:5000/?id=Y9H6PWS")

    @patch('main.get_url', return_value="https://www.yahoo.com/")
    def test_07_mock_get_url(self, get_url):
        # test for the return value of get_url function
        self.assertEqual(get_url("Y9H6PWS"),"https://www.yahoo.com/")

    def test_08_hashing_function(self):
        # test for generating md5 hash with base64 encoding for a long url
        answer = self.testfunc("https://csatlas.com/python-import-file-module/")
        self.assertEqual(answer, "OFDQHCn")

    def test_09_hashing_function(self):
        # test for generating md5 hash with base64 encoding for a long url
        answer = self.testfunc("https://meet.google.com/rfn-obfh-crg?pli=1&authuser=0")
        self.assertEqual(answer, "UoSTnFy")

    def test_10_hashing_function(self):
        # test for generating md5 hash with base64 encoding for a long url
        answer = self.testfunc("https://dev.mysql.com/doc/connector-python/en/connector-python-introduction.html")
        self.assertEqual(answer, "FzGH6O9")






