# PlantSpy
PlantSpy is an AI tool (Deep Learning) allowing to detect the category of a plant, its health and its eventual sickness name.



Pour utiliser les modèles de prediction, il suffit de :

1- Fournir une image au script python  

2- Appliquer la mise en forme nécessaire (resize à 100x100, mise en place en array)

3- Appeler la fonction "Predict()" qui prend en argument l'image

En sortie, le système fournit sa prédiction comme suit : 
nom_de_catégorie_de_plante + intervalle de confiance de prediction en % + [Healthy ou nom_maladie] + intervalle de confiance de prediction en %


**Example** :
1- Image en input : ./Models/NewPlantDiseasesDataset/test/test/AppleCedarRust1.JPG

2- Mise en forme en python :

        image = test_images[0]
        img = cv2.imread(image, cv2.IMREAD_COLOR)
        img_resized = cv2.resize(img, (100, 100))
        X_test = []
        X_test.append(img_resized)
        X_test = np.array(X_test) / 255

3- Appel du modèle: 

        prediction_0 = predict(X_test)
        
        print("==> Prediction : " + str(prediction_0.iloc[0, 0]) +
               " for " + str(round(prediction_0.iloc[0, 1] * 100, 2)) +"% and as " +
               str(prediction_0.iloc[0, 2]) + " for " + str(round(prediction_0.iloc[0, 3] * 100, 2)) + "%")

Résultat :
==> Prediction : Apple for 94.95% and as Cedar_apple_rust for 100.0%
