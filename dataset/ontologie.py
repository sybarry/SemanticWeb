from rdflib import Graph, RDF, OWL, Namespace, RDFS, URIRef
# Charger le fichier RDF existant
rdf_file_path = "../output_rdf/birds_united_states.rdf"
g = Graph()
g.parse(rdf_file_path, format="xml")


# Définir la namespace
ns1 = Namespace("localhost:3030/")

# Ajouter des règles OWL/RDFS pour la propriété id
g.add((ns1.id, RDF.type, OWL.FunctionalProperty))
g.add((ns1.id, RDF.type, RDF.Property))
g.add((ns1.id, RDFS.domain, ns1.RDF_Description))
g.add((ns1.id, RDFS.range, RDFS.Literal))

# Sauvegarder le fichier RDF mis à jour
g.serialize(destination="../output_rdf/birds_united_states.rdf", format="xml")
