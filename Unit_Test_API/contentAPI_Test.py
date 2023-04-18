import unittest
import requests
#from api_utils import checkStatusCodeAndPrintLog

link="http://107.152.44.75:5555/token"    #"http://plantspy.dev-boris.fr/login"


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

class TestAPIContent(unittest.TestCase):

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
        print("res_1 = ", res_1)


        PredictSante_url = "http://107.152.44.75:8000/prediction_sante_url" 

        res_2 = requests.get(PredictSante_url, headers=headers, params={"url": imageUrl})
        self.assertEqual(res_2.status_code, 200)
        print("res_2 = ", res_2)


        PredictMaladie_url = "http://107.152.44.75:8000//prediction_maladie_url" 

        res_3 = requests.get(PredictSante_url, headers=headers, params={"url": imageUrl})
        self.assertEqual(res_3.status_code, 200)
        print("res_3 = ", res_3)

        # Récupération de la prédiction
        prediction = res_3.json()
        print("Prédiction :", prediction)
        #print("Prédiction :", prediction.maladie_pred[0])
    #<p>Prediction Results: {predictions.maladie_pred[0]} avec un niveau de confiance {predictions.confiance_categorie[0].toFixed(2)} et etat de santé {predictions.maladie_pred[0]} avec seuil de confiance {predictions.confiance[0].toFixed(2)}</p>


        # Accéder aux informations de la prédiction
        maladie_pred = prediction["maladie_pred"]
        confiance = prediction["confiance"]

        print("Maladie prédite:", maladie_pred)
        print("Confiance:", confiance)

        # Vous pouvez également accéder aux valeurs spécifiques si nécessaire
        maladie_pred_0 = maladie_pred["0"]
        confiance_0 = confiance["0"]

        print("Maladie prédite pour la clé 0:", maladie_pred_0)
        print("Confiance pour la clé 0:", confiance_0)

        # Vous pouvez ensuite utiliser des assertions pour vérifier si les valeurs sont correctes
        self.assertEqual(maladie_pred_0, "Healthy")  # Remplacez "Healthy" par la valeur attendue
        self.assertGreater(confiance_0, 0.9)  # Vérifiez si la confiance est supérieure à 0.9



if __name__ == '__main__':
    unittest.main()