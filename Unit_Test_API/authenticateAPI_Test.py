import unittest
import requests
#from api_utils import checkStatusCodeAndPrintLog



link="http://107.152.44.75:8000/token"    #"http://plantspy.dev-boris.fr/login"

data_johndoe = {
    "username": "johndoe",
    "password": "secret",
    "grant_type": "password",
    "scope": "",
    "client_id": "",
    "client_secret": "",
}

data_alice = {
    "username": "alice",
    "password": "wonderland",
    "grant_type": "password",
    "scope": "",
    "client_id": "",
    "client_secret": "",
}

data_laboratoire = {
    "username": "laboratoire",
    "password": "analyse",
    "grant_type": "password",
    "scope": "",
    "client_id": "",
    "client_secret": "",
}
data_bob = {
    "username": "bob",
    "password": "ordinateur",
    "grant_type": "password",
    "scope": "",
    "client_id": "",
    "client_secret": "",
}

data_unknown = {
    "username": "unknown",
    "password": "nothing",
    "grant_type": "password",
    "scope": "",
    "client_id": "",
    "client_secret": "",
}

class TestAPIAuthentication(unittest.TestCase):

    def test_authentication_1(self):
        response = requests.post(link, data=data_johndoe)
        self.assertEqual(response.status_code, 200)

    def test_authentication_2(self):
        response = requests.post(link, data=data_alice)
        self.assertEqual(response.status_code, 200)

    def test_authentication_3(self):
        response = requests.post(link, data=data_laboratoire)
        self.assertEqual(response.status_code, 200)

    def test_authentication_4(self):
        response = requests.post(link, data=data_bob)
        self.assertEqual(response.status_code, 200)

    def test_authentication_5(self):
        response = requests.post(link, data=data_unknown)
        self.assertEqual(response.status_code, 500) # not handled 


if __name__ == '__main__':
    unittest.main()

