import unittest
from PIL import Image
import os
import cv2

import numpy as np
from PlantSpyModels import predict

test_images = [
    './Models/NewPlantDiseasesDataset/test/test/AppleCedarRust1.JPG',
    './Models/NewPlantDiseasesDataset/test/test/AppleCedarRust4.JPG',
    './Models/NewPlantDiseasesDataset/test/test/AppleScab1.JPG',
    './Models/NewPlantDiseasesDataset/test/test/AppleScab3.JPG',
    './Models/NewPlantDiseasesDataset/test/test/CornCommonRust1.JPG',
    './Models/NewPlantDiseasesDataset/test/test/CornCommonRust2.JPG',
    './Models/NewPlantDiseasesDataset/test/test/CornCommonRust3.JPG',
    './Models/NewPlantDiseasesDataset/test/test/PotatoEarlyBlight1.JPG',
    './Models/NewPlantDiseasesDataset/test/test/PotatoEarlyBlight4.JPG',
    './Models/NewPlantDiseasesDataset/test/test/PotatoHealthy1.JPG',
    './Models/NewPlantDiseasesDataset/test/test/PotatoHealthy2.JPG',
    './Models/NewPlantDiseasesDataset/test/test/TomatoEarlyBlight1.JPG',
    './Models/NewPlantDiseasesDataset/test/test/TomatoHealthy1.JPG',
    './Models/NewPlantDiseasesDataset/test/test/TomatoYellowCurlVirus1.JPG',
    './Models/NewPlantDiseasesDataset/test/test/TomatoHealthy4.JPG'
]


class TestImage(unittest.TestCase):
    def test_is_good_extension(self):
        # Charger l'image de test
        image_test = test_images[0]
        #print("iel  image = " + image_test)
        name, extension = os.path.splitext(image_test)
        #print(extension)
        self.assertIn(extension, ['.JPEG', '.PNG', '.JPG'], f'Invalid image format: {extension}')

    def test_is_good_format(self):
        with open(test_images[0], 'rb') as file:
            img = Image.open(file)
            #print("img.format", img.format)  # 'JPEG'
            self.assertIn(img.format, ['JPEG', 'PNG', 'JPG'], f'Invalid image format: {img.format}')

    def test_size_limit(self):
        """
        check if the image size doesn't exceed 5 Mo
        :return:
        """
        image_test = test_images[0]

        # Taille maximale autorisée (en octets)
        size_limit =  5 * 1024 * 1024

        # Vérifier la taille de l'image (en octets)
        img_size = os.path.getsize(image_test)
        self.assertLessEqual(img_size, size_limit, f'Image size is too big. {img_size} bytes > {size_limit} bytes')


    def test_image_resolution(self):
        # Charger l'image de test
        
        with open(test_images[0], 'rb') as file:
            img = cv2.imread(test_images[0])

            # Vérifier que les dimensions de l'image sont cohérentes avec les attentes du système
            expected_height, expected_width = 256, 256 # min /max +++
            self.assertEqual(img.shape[:2], (expected_height, expected_width),
                             f"Inconsistent image dimensions. Expected {expected_height}x{expected_width} but got {img.shape[:2]}")


    def test_image_quality(self):
        
        with open(test_images[0], 'rb') as file:
            img = Image.open(file)

            # Convertir l'image en niveaux de gris
            img = img.convert('L')

            # Calculer le coefficient de variation de l'image
            pixels = np.array(img).flatten()
            cv = np.std(pixels) / np.mean(pixels)

            # Définir la limite de qualité d'image
            quality_limit = 0.20

            # Vérifier la qualité de l'image
            self.assertLess(cv, quality_limit, f'Image quality is too low. CV={cv}')

##########
# test d'une prédiction du modèle

    def test_image_prediction(self):
        # for i in range(0, level):
        with open(test_images[0], 'rb') as file:
            img = cv2.imread(test_images[0], cv2.IMREAD_COLOR)
            img_resized = cv2.resize(img, (100, 100))

            X_test = []
            X_test.append(img_resized)
            X_test = np.array(X_test) / 255
            prediction_0 = predict(X_test)

            print("list keys of dictionary : ",list(prediction_0.keys()))
            #list keys of dictionary :  ['categorie', 'confiance_categorie', 'maladie_pred', 'confiance']

            self.assertEqual(str(prediction_0["categorie"][0]), "Apple",
                 f"Category prediction is wrong. Expected Apple but got {str(prediction_0['categorie'][0])}")

            
            self.assertEqual(str(prediction_0["maladie_pred"][0]), "Cedar_apple_rust",
                          f"Category prediction is wrong. Expected Cedar_apple_rust but got {str(prediction_0['maladie_pred'][0])}")

    def test_image_prediction_2(self):
        expected_categories = ["Apple", "Apple", "Apple", "Apple", "Corn", "Corn", "Corn", "Potato", "Potato", "Potato", "Potato", "Tomato", "Tomato", "Tomato", "Tomato"]
        expected_diseases = ["Cedar_apple_rust", "Cedar_apple_rust", "Apple_scab", "Apple_scab", "Common_rust", "Common_rust", "Common_rust", "Early_blight", "Early_blight", "Healthy", "Healthy", "Early_blight", "Healthy", "Yellow_curl_virus", "Healthy"]

        correct_category_predictions = 0
        correct_disease_predictions = 0

        for i, image_path in enumerate(test_images):
            with open(image_path, 'rb') as file:
                img = cv2.imread(image_path, cv2.IMREAD_COLOR)
                img_resized = cv2.resize(img, (100, 100))

                X_test = []
                X_test.append(img_resized)
                X_test = np.array(X_test) / 255
                prediction = predict(X_test)
                print(" index ", i , " predicted categorie ", str(prediction["categorie"][0]) , " expected = ", expected_categories[i])
                if str(prediction["categorie"][0]) == expected_categories[i]:
                    correct_category_predictions += 1

                if str(prediction["maladie_pred"][0]) == expected_diseases[i]:
                    correct_disease_predictions += 1

        total_predictions = len(test_images)
        correct_category_percentage = (correct_category_predictions / total_predictions) * 100
        correct_disease_percentage = (correct_disease_predictions / total_predictions) * 100

        print(f"Correct category predictions: {correct_category_percentage}%")
        print(f"Correct disease predictions: {correct_disease_percentage}%")
        
        target_value = 85
        self.assertGreater(correct_category_percentage, target_value, "correct_category_percentage should be >= 85%")
        self.assertGreater(correct_disease_percentage, target_value, "correct_disease_percentage should be >= 85%")



##########
if __name__ == '__main__':
        unittest.main()
