FROM debian:latest

RUN apt-get update && apt-get install python3-pip -y && apt-get install -y python3
#RUN apt-get update && apt-get install -y python3

# Copier le fichier requirements dans le conteneur
COPY requirements.txt /requirements.txt

# Installer les dépendances requises
RUN pip3 install -r /requirements.txt

# Copier les fichiers de test dans le conteneur
COPY authenticateAPI_Test.py  /authenticateAPI_Test.py
COPY authorizationAPI_Test.py /authorizationAPI_Test.py
COPY contentAPI_Test.py       /contentAPI_Test.py

# Volume ou collecter les logs des différents containers de tests unitaires
VOLUME /test_logs

# Set the environment variable for logging
ENV LOG=1

# Run the command to execute the tests
CMD python3 authenticateAPI_Test.py
CMD python3 authorizationAPI_Test.py
CMD python3 contentAPI_Test.py