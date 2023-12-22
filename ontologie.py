import rdflib
from rdflib.namespace import RDF

# Charger le fichier RDF
g = rdflib.Graph()
g.parse("output_rdf/birds_united_states.rdf", format="xml") # Remplacez par le chemin de votre fichier RDF



# Définir l'ontologie (ajouter des triplets d'ontologie)
ontology = """
@prefix ns1: <localhost:3030/> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

ns1:Bird a rdfs:Class .

# Propriétés de base
ns1:hasGenus a rdf:Property .
ns1:hasSpecies a rdf:Property .
ns1:hasLocation a rdf:Property .
ns1:recordedBy a rdf:Property .
ns1:hasLatitude a rdf:Property ; rdfs:range xsd:decimal .
ns1:hasLongitude a rdf:Property ; rdfs:range xsd:decimal .
ns1:hasAltitude a rdf:Property ; rdfs:range xsd:decimal .
ns1:hasRecordingURL a rdf:Property ; rdfs:range xsd:anyURI .
ns1:hasSoundType a rdf:Property .
ns1:hasQuality a rdf:Property .
ns1:hasLength a rdf:Property .
ns1:hasDate a rdf:Property ; rdfs:range xsd:date .
ns1:hasTime a rdf:Property ; rdfs:range xsd:time .
ns1:hasFileName a rdf:Property .

# Équivalences avec les propriétés RDF
ns1:gen owl:equivalentProperty ns1:hasGenus .
ns1:sp owl:equivalentProperty ns1:hasSpecies .
ns1:loc owl:equivalentProperty ns1:hasLocation .
ns1:rec owl:equivalentProperty ns1:recordedBy .
ns1:lat owl:equivalentProperty ns1:hasLatitude .
ns1:lng owl:equivalentProperty ns1:hasLongitude .
ns1:alt owl:equivalentProperty ns1:hasAltitude .
ns1:url owl:equivalentProperty ns1:hasRecordingURL .
ns1:type owl:equivalentProperty ns1:hasSoundType .
ns1:q owl:equivalentProperty ns1:hasQuality .
ns1:length owl:equivalentProperty ns1:hasLength .
ns1:date owl:equivalentProperty ns1:hasDate .
ns1:time owl:equivalentProperty ns1:hasTime .
ns1:file-name owl:equivalentProperty ns1:hasFileName .
ns1:SnowGoose a rdfs:Class ; rdfs:subClassOf ns1:Bird .
ns1:Nene a rdfs:Class ; rdfs:subClassOf ns1:Bird .
ns1:Bird rdfs:subClassOf [
    a owl:Restriction ;
    owl:onProperty ns1:hasGenus ;
    owl:someValuesFrom xsd:string
] .
ns1:Bird rdfs:subClassOf [
    a owl:Restriction ;
    owl:onProperty ns1:hasSpecies ;
    owl:someValuesFrom xsd:string
] .
ns1:Bird rdfs:subClassOf [
    a owl:Restriction ;
    owl:onProperty ns1:hasGenus ;
    owl:maxCardinality "1"^^xsd:nonNegativeInteger
] .
ns1:hasLocation rdfs:domain ns1:Bird ; rdfs:range xsd:string .
ns1:recordedBy rdfs:domain ns1:Bird ; rdfs:range xsd:string .
ns1:records owl:inverseOf ns1:recordedBy .
ns1:relatedSpecies a owl:SymmetricProperty .
ns1:partOf a owl:TransitiveProperty .
"""
g.parse(data=ontology, format="turtle")

# Définir les espaces de noms
ns1 = rdflib.Namespace("localhost:3030/")

# Parcourir toutes les entités ayant une propriété ns1:en et leur attribuer le type Bird
for s, p, o in g.triples((None, ns1.en, None)):
    g.add((s, RDF.type, ns1.Bird))


g.serialize(destination="output_rdf/birds_united_states_ontologie.rdf", format="xml")
