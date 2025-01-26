import csv
import uuid
from rdflib import Graph, Literal, URIRef
from rdflib.namespace import RDF, RDFS

def generate_unique_id():
    """Generate a unique identifier."""
    return str(uuid.uuid4())

def transform_csv_to_rdf(input_csv, output_ttl):
    """
    Transform CSV to RDF with unique identifiers.
    """
    g = Graph()

    with open(input_csv, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        
        for row in reader:
            subject = row['Subject']
            relation = row['Relation']
            obj = row['Object']

            # Unique identifiers
            movie_id = generate_unique_id()
            movie_uri = URIRef(f"http://example.org/movie/{subject.replace(' ', '_')}")
            movie_identifier_uri = URIRef(f"https://schema.org/identifier/{movie_id}")
            
            # Add movie with identifier
            g.add((movie_uri, RDF.type, URIRef("https://schema.org/Movie")))
            g.add((movie_uri, URIRef("https://schema.org/identifier"), movie_identifier_uri))
            g.add((movie_identifier_uri, RDFS.label, Literal(movie_id)))

            if relation == 'director':
                # Director with unique identifier
                director_id = generate_unique_id()
                director_uri = URIRef(f"https://schema.org/director/{obj.replace(' ', '_')}")
                director_identifier_uri = URIRef(f"https://schema.org/identifier/{director_id}")
                
                g.add((movie_uri, URIRef("https://schema.org/director"), director_uri))
                g.add((director_uri, RDFS.label, Literal(obj)))
                g.add((director_uri, URIRef("https://schema.org/name"), Literal(obj)))
                g.add((director_uri, URIRef("https://schema.org/identifier"), director_identifier_uri))
                g.add((director_identifier_uri, RDFS.label, Literal(director_id)))

            elif relation == 'characters':
                # Character with unique identifier
                character_id = generate_unique_id()
                character_uri = URIRef(f"https://schema.org/character/{obj.replace(' ', '_')}")
                character_identifier_uri = URIRef(f"https://schema.org/identifier/{character_id}")
                
                g.add((movie_uri, URIRef("https://schema.org/character"), character_uri))
                g.add((character_uri, RDFS.label, Literal(obj)))
                g.add((character_uri, URIRef("https://schema.org/name"), Literal(obj)))
                g.add((character_uri, URIRef("https://schema.org/identifier"), character_identifier_uri))
                g.add((character_identifier_uri, RDFS.label, Literal(character_id)))

    # Serialize the graph to Turtle
    g.serialize(destination=output_ttl, format='turtle')
    print(f"RDF graph saved to {output_ttl}")

# Execute the transformation
transform_csv_to_rdf('movie_triples.csv', 'film_ia2.ttl')