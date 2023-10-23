import csv
from rdflib import Graph, Namespace, Literal
from rdflib.namespace import RDF
import urllib.parse

line = 0

nb_line = 200

# Crée un graphe RDF
g = Graph()

# Crée un espace de noms personnalisé
my_namespace = Namespace("localhost:3030/")

# Ouvrir le fichier CSV
with open('birds_united_states.csv', 'r', encoding="utf-8") as csv_file:
    csv_reader = csv.DictReader(csv_file)

    for row in csv_reader:
        # Crée un URI pour chaque ligne en utilisant l'espace de noms personnalisé
        if line == nb_line:
            break
        line += 1
        print(row)
        subject = my_namespace[row['id']]

        # Ajoutez des triplets RDF pour chaque colonne dans le CSV
        for column, value in row.items():
            if column == "ID" or 'gen' or 'sp' or 'en' or 'rec' or 'loc' or 'lat' or 'lng' or 'alt' or 'file' or 'date' or 'length':
                predicate = my_namespace[column]
                object = Literal(value)
                g.add((subject, predicate, object))

# Sauvegarde le graphe RDF dans un fichier
g.serialize('../output_rdf/birds_united_states.rdf', format='xml')
