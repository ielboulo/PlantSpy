import tensorflow as tf

model_categorie = tf.keras.models.load_model('./Models/model_LeNet1_Categorie_AllData_Softmax')
model_healthy = tf.keras.models.load_model("./Models/model_isHealthy_18K")
model_maladieTomato = tf.keras.models.load_model('./Models/model_Tomate_avecHealthy_softmax')
model_maladiePotato = tf.keras.models.load_model('./Models/model_Potato1_avecHealthy')
model_maladieCorn   = tf.keras.models.load_model('./Models/model_Corn_Healthy')
model_maladieApple  = tf.keras.models.load_model('./Models/model_Apple_Healthy')
model_maladieGrape  = tf.keras.models.load_model('./Models/model_Grape1_Healthy')


dict_categorie = {0: 'Apple', 1: 'Blueberry', 2: 'Cherry', 3: 'Corn', 4: 'Grape', 5: 'Orange', 6: 'Peach',
                  7: 'Pepper', 8: 'Potato', 9: 'Raspberry', 10: 'Soybean', 11: 'Squash', 12: 'Strawberry', 13: 'Tomato'}

# Grape
dict_maladie_Grape1 = {0: 'Black_rot',
                       1: 'Esca_(Black_Measles)',
                       2: 'Leaf_blight_(Isariopsis_Leaf_Spot)',
                       3: 'healthy'}

# POTATO

dict_maladie_Potato1 = {0: 'Early_blight',
                        1: 'Late_blight',
                        2: 'healthy'}

# TOMATO

dict_maladie_Tomato1 = {0: 'Bacterial_spot',
                        1: 'Early_blight',
                        2: 'Late_blight',
                        3: 'Leaf_Mold',
                        4: 'Septoria_leaf_spot',
                        5: 'Spider_mites Two-spotted_spider_mite',
                        6: 'Target_Spot',
                        7: 'Tomato_Yellow_Leaf_Curl_Virus',
                        8: 'Tomato_mosaic_virus',
                        9: 'healthy'}

# APPLE

dict_maladie_Apple1 = {0: 'Apple_scab',
                       1: 'Black_rot',
                       2: 'Cedar_apple_rust',
                       3: 'healthy'}

# CORN

dict_maladie_Corn1 = {2: 'Northern_Leaf_Blight',
                      1: 'Common_rust_',
                      0: 'Cercospora_leaf_spot Gray_leaf_spot',
                      3: 'healthy'}
