import csv
from rdflib import Graph, Namespace, Literal, URIRef
from rdflib.namespace import RDF
import urllib.parse
import requests
import librosa
from pydub import AudioSegment
import numpy as np
from pathlib import Path


def extract_average_frequency(audio_file):
    audio = AudioSegment.from_mp3(audio_file)
    samples = np.array(audio.get_array_of_samples())
    freq_moyenne = np.mean(np.abs(samples))
    print("Fréquence moyenne :", round(freq_moyenne, 2))
    return round(freq_moyenne, 2)

def download_mp3(url, file_name):
    response = requests.get(url)
    path_file = "audios/" + file_name + ".mp3"
    path = Path(path_file)
    if not path.is_file():
        with open(path_file, "wb") as f:
            f.write(response.content)

    return path_file


line = 0

# Ligne maximale à atteindre, soit final_line/saut_line lignes au total
final_line = 1000

# On sautera de saut_line à chaque fois
saut_line = 5

# Crée un graphe RDF
g = Graph()

# Crée un espace de noms personnalisé
my_namespace = Namespace("localhost:3030/")

# Ouvrir le fichier CSV
with open('birds_united_states.csv', 'r', encoding="utf-8") as csv_file:
    csv_reader = csv.DictReader(csv_file)

    for row in csv_reader:
        # Crée un URI pour chaque ligne en utilisant l'espace de noms personnalisé
        if line == final_line:
            break
        # On veut sauter des lignes afin d'avoir un échantillon plus varié des espèces
        line += saut_line

        subject = my_namespace[row['id']]

        # Ajoutez des triplets RDF pour chaque colonne dans le CSV
        for column, value in row.items():
            if column == "ID" or 'gen' or 'sp' or 'en' or 'rec' or 'loc' or 'lat' or 'lng' or 'alt' or 'file' or 'date' or 'length':
                predicate = my_namespace[column]

                if column == "file":
                    object = URIRef("localhost:3030/" + value)
                    g.add((subject, predicate, object))
                    path_file = download_mp3("https:" + value, row['id'])
                    average_frequency = extract_average_frequency(path_file)
                    g.add((object, URIRef("localhost:3030/average_frequency"), Literal(int(average_frequency))))

                else:
                    object = Literal(value)
                    g.add((subject, predicate, object))

# Sauvegarde le graphe RDF dans un fichier
g.serialize('output_rdf/birds_united_states.rdf', format='xml')
