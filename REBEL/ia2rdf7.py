import csv
import uuid
from rdflib import Graph, Literal, URIRef, Namespace
from rdflib.namespace import RDF, RDFS

def generate_unique_id():
    """Generate a unique identifier."""
    return str(uuid.uuid4())

def transform_csv_to_rdf(input_csv, output_ttl):
    """
    Transform CSV to RDF without duplicate properties."""
    g = Graph()
    
    ex = Namespace("http://example.org/")
    g.namespace_manager.bind('ex', ex)

    with open(input_csv, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        
        for row in reader:
            subject = row['Subject']
            relation = row['Relation']
            obj = row['Object']

            identifier = generate_unique_id()

            if relation == 'director':
                # Movie
                movie_uri = ex[f"movie/{subject.replace(' ', '_')}"]
                g.add((movie_uri, RDF.type, URIRef("https://schema.org/Movie")))
                g.add((movie_uri, URIRef("https://schema.org/name"), Literal(subject)))
                g.add((movie_uri, URIRef("https://schema.org/identifier"), Literal(identifier)))
                
                # Director
                director_uri = ex[f"director/{obj.replace(' ', '_')}"]
                g.add((director_uri, RDF.type, URIRef("https://schema.org/Person")))
                g.add((director_uri, URIRef("https://schema.org/name"), Literal(obj)))
                g.add((director_uri, URIRef("https://schema.org/identifier"), Literal(identifier)))
                
                # Use only custom properties
                g.add((movie_uri, ex.hasDirector, director_uri))
                g.add((director_uri, ex.inMovie, movie_uri))

            elif relation == 'characters':
                # Movie
                movie_uri = ex[f"movie/{subject.replace(' ', '_')}"]
                g.add((movie_uri, RDF.type, URIRef("https://schema.org/Movie")))
                g.add((movie_uri, URIRef("https://schema.org/name"), Literal(subject)))
                g.add((movie_uri, URIRef("https://schema.org/identifier"), Literal(identifier)))

                # Character
                character_uri = ex[f"character/{obj.replace(' ', '_')}"]
                g.add((character_uri, RDF.type, URIRef("https://schema.org/Character")))
                g.add((character_uri, URIRef("https://schema.org/name"), Literal(obj)))
                g.add((character_uri, URIRef("https://schema.org/identifier"), Literal(identifier)))
                
                # Use only custom properties
                g.add((movie_uri, ex.hasCharacter, character_uri))
                g.add((character_uri, ex.inFilm, movie_uri))

    # Serialize the graph to Turtle
    g.serialize(destination=output_ttl, format='turtle')
    print(f"RDF graph saved to {output_ttl}")

# Execute the transformation
transform_csv_to_rdf('movie_triples.csv', 'film_ia7.ttl')