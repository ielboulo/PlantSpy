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
    './ModelsNewPlantDiseasesDataset/test/test/PotatoEarlyBlight1.JPG',
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
        image_test = test_images[0]
        img = Image.open(image_test)
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
        image_test = test_images[0]

        img = cv2.imread(image_test)

        # Vérifier que les dimensions de l'image sont cohérentes avec les attentes du système
        expected_height, expected_width = 256, 256 # min /max +++
        self.assertEqual(img.shape[:2], (expected_height, expected_width),
                         f"Inconsistent image dimensions. Expected {expected_height}x{expected_width} but got {img.shape[:2]}")


    def test_image_quality(self): # degré de flou
        img = Image.open(test_images[0])

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
            img = cv2.imread(file, cv2.IMREAD_COLOR)
            img_resized = cv2.resize(img, (100, 100))

            X_test = []
            X_test.append(img_resized)
            X_test = np.array(X_test) / 255
            prediction_0 = predict(X_test)


            #print("==> Prediction : " + str(prediction_0.iloc[0, 0]) +
            #       " for " + str(round(prediction_0.iloc[0, 1] * 100, 2)) +"% and as " +
            #       str(prediction_0.iloc[0, 2]) + " for " + str(round(prediction_0.iloc[0, 3] * 100, 2)) + "%")

            self.assertEqual(str(prediction_0.iloc[0, 0]), "Apple",
                              f"Category prediction is wrong. Expected Apple but got {str(prediction_0.iloc[0, 0])}")
            self.assertEqual(str(prediction_0.iloc[0, 2]), "Cedar_apple_rust",
                              f"Category prediction is wrong. Expected Cedar_apple_rust but got {str(prediction_0.iloc[0, 2])}")


##########
if __name__ == '__main__':
        unittest.main()
