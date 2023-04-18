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

data_bob = {
    "username": "bob",
    "password": "ordinateur",
    "grant_type": "password",
    "scope": "",
    "client_id": "",
    "client_secret": "",
}


imageUrl = "https://thumbs.dreamstime.com/b/feuille-de-tomate-59429924.jpg"

class TestAPIAuthorization(unittest.TestCase):

    def test_data_johndoe(self):
        response = requests.post(link, data=data_johndoe)
        self.assertEqual(response.status_code, 200)

        json_response = response.json()
        #print("Réponse  :", json_response)

        access_token = json_response["access_token"]

        # Utilisation du token pour accéder à un autre endpoint
        headers = {"Authorization": f"Bearer {access_token}"}
        healthcheck_url = "http://107.152.44.75:8000/Healthcheck"

        healthcheck_response = requests.get(healthcheck_url, headers=headers)
        self.assertEqual(healthcheck_response.status_code, 200)

        PredictCategorie_url = "http://107.152.44.75:8000/prediction_plante_url" 

        res_1 = requests.get(PredictCategorie_url, headers=headers, params={"url": imageUrl})
        self.assertEqual(res_1.status_code, 200)

        PredictSante_url = "http://107.152.44.75:8000/prediction_sante_url" 

        res_2 = requests.get(PredictSante_url, headers=headers, params={"url": imageUrl})
        self.assertEqual(res_2.status_code, 200)

        PredictMaladie_url = "http://107.152.44.75:8000//prediction_maladie_url" 

        res_3 = requests.get(PredictSante_url, headers=headers, params={"url": imageUrl})
        self.assertEqual(res_3.status_code, 200)



    def test_data_alice(self):
        response = requests.post(link, data=data_alice)
        self.assertEqual(response.status_code, 200)

        json_response = response.json()
        print("Réponse JSON :", json_response)

        access_token = json_response["access_token"]

        # Utilisation du token pour accéder à un autre endpoint
        headers = {"Authorization": f"Bearer {access_token}"}
        healthcheck_url = "http://107.152.44.75:8000/Healthcheck"

        healthcheck_response = requests.get(healthcheck_url, headers=headers)
        self.assertEqual(healthcheck_response.status_code, 200)

        PredictCategorie_url = "http://107.152.44.75:8000/prediction_plante_url" 

        res_1 = requests.get(PredictCategorie_url, headers=headers, params={"url": imageUrl})
        self.assertEqual(res_1.status_code, 200)

        PredictSante_url = "http://107.152.44.75:8000/prediction_sante_url" 

        res_2 = requests.get(PredictSante_url, headers=headers, params={"url": imageUrl})
        self.assertEqual(res_2.status_code, 200)

        PredictMaladie_url = "http://107.152.44.75:8000//prediction_maladie_url" 

        res_3 = requests.get(PredictSante_url, headers=headers, params={"url": imageUrl})
        self.assertEqual(res_3.status_code, 200)


    def test_data_bob(self):
        response = requests.post(link, data=data_bob)
        self.assertEqual(response.status_code, 200)

        json_response = response.json()
        #print("Réponse :", json_response)

        access_token = json_response["access_token"]

        # Utilisation du token pour accéder à un autre endpoint
        headers = {"Authorization": f"Bearer {access_token}"}
        healthcheck_url = "http://107.152.44.75:8000/Healthcheck"

        healthcheck_response = requests.get(healthcheck_url, headers=headers)
        self.assertEqual(healthcheck_response.status_code, 200)

        PredictCategorie_url = "http://107.152.44.75:8000/prediction_plante_url" 

        res_1 = requests.get(PredictCategorie_url, headers=headers, params={"url": imageUrl})
        self.assertEqual(res_1.status_code, 200)

        PredictSante_url = "http://107.152.44.75:8000/prediction_sante_url" 

        res_2 = requests.get(PredictSante_url, headers=headers, params={"url": imageUrl})
        self.assertEqual(res_2.status_code, 403)

        PredictMaladie_url = "http://107.152.44.75:8000//prediction_maladie_url" 

        res_3 = requests.get(PredictSante_url, headers=headers, params={"url": imageUrl})
        self.assertEqual(res_3.status_code, 403)


if __name__ == '__main__':
    unittest.main()