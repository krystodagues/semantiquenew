import csv
import uuid
from rdflib import Graph, Literal, URIRef
from rdflib.namespace import RDF, RDFS

def generate_unique_id():
    """Generate a unique identifier."""
    return str(uuid.uuid4())

def transform_csv_to_rdf(input_csv, output_ttl):
    """
    Transform CSV to RDF with improved entity representation.
    """
    g = Graph()

    with open(input_csv, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        
        for row in reader:
            subject = row['Subject']
            relation = row['Relation']
            obj = row['Object']

            # Unique identifier
            identifier = generate_unique_id()

            if relation == 'director':
                # Movie
                movie_uri = URIRef(f"http://example.org/movie/{subject.replace(' ', '_')}")
                g.add((movie_uri, RDF.type, URIRef("https://schema.org/Movie")))
                g.add((movie_uri, URIRef("https://schema.org/name"), Literal(subject)))
                
                # Director
                director_uri = URIRef(f"http://example.org/director/{obj.replace(' ', '_')}")
                g.add((director_uri, RDF.type, URIRef("https://schema.org/Person")))
                g.add((director_uri, URIRef("https://schema.org/name"), Literal(obj)))

                # Linking
                g.add((movie_uri, URIRef("https://schema.org/identifier"), Literal(identifier)))
                g.add((movie_uri, URIRef("https://schema.org/director"), director_uri))
                g.add((director_uri, URIRef("https://schema.org/identifier"), Literal(identifier)))
                
                # Symmetrical properties
                g.add((movie_uri, URIRef("http://example.org/hasDirector"), director_uri))
                g.add((director_uri, URIRef("http://example.org/inMovie"), movie_uri))

            elif relation == 'characters':
                # Movie (ensure it exists)
                movie_uri = URIRef(f"http://example.org/movie/{subject.replace(' ', '_')}")
                g.add((movie_uri, RDF.type, URIRef("https://schema.org/Movie")))
                g.add((movie_uri, URIRef("https://schema.org/name"), Literal(subject)))
                g.add((movie_uri, URIRef("https://schema.org/identifier"), Literal(identifier)))

                # Character
                character_uri = URIRef(f"http://example.org/character/{obj.replace(' ', '_')}")
                g.add((character_uri, RDF.type, URIRef("https://schema.org/Character")))
                g.add((character_uri, URIRef("https://schema.org/name"), Literal(obj)))
                g.add((character_uri, URIRef("https://schema.org/identifier"), Literal(identifier)))

                # Linking
                g.add((movie_uri, URIRef("https://schema.org/character"), character_uri))
                
                # Symmetrical properties
                g.add((movie_uri, URIRef("http://example.org/hasCharacter"), character_uri))
                g.add((character_uri, URIRef("http://example.org/inFilm"), movie_uri))

    # Serialize the graph to Turtle
    g.serialize(destination=output_ttl, format='turtle')
    print(f"RDF graph saved to {output_ttl}")

# Execute the transformation
transform_csv_to_rdf('movie_triples.csv', 'film_ia4.ttl')