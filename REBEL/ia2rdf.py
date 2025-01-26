import csv
import uuid
from rdflib import Graph, Literal, Namespace, URIRef
from rdflib.namespace import RDF, RDFS

def generate_unique_id():
    """Generate a unique identifier."""
    return str(uuid.uuid4())

def transform_csv_to_rdf(input_csv, output_ttl):
    """
    Transform CSV to RDF with specific schema definitions.
    
    Args:
        input_csv (str): Path to input CSV file
        output_ttl (str): Path to output Turtle file
    """
    # Create a new graph
    g = Graph()

    # Read the CSV
    with open(input_csv, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        
        for row in reader:
            subject = row['Subject']
            relation = row['Relation']
            obj = row['Object']

            # Movie URI
            movie_uri = URIRef(f"http://example.org/movie/{subject.replace(' ', '_')}")
            
            # Add movie type
            g.add((movie_uri, RDF.type, URIRef("https://schema.org/Movie")))

            if relation == 'director':
                # Director URI with unique identifier
                director_uri = URIRef(f"https://schema.org/director/{obj.replace(' ', '_')}_{generate_unique_id()}")
                
                # Add director information
                g.add((movie_uri, URIRef("https://schema.org/director"), director_uri))
                g.add((director_uri, RDFS.label, Literal(obj)))
                g.add((director_uri, URIRef("https://schema.org/name"), Literal(obj)))

            elif relation == 'characters':
                # Character URI with unique identifier
                character_uri = URIRef(f"https://schema.org/character/{obj.replace(' ', '_')}_{generate_unique_id()}")
                
                # Add character information
                g.add((movie_uri, URIRef("https://schema.org/character"), character_uri))
                g.add((character_uri, RDFS.label, Literal(obj)))
                g.add((character_uri, URIRef("https://schema.org/name"), Literal(obj)))

    # Serialize the graph to Turtle
    g.serialize(destination=output_ttl, format='turtle')
    print(f"RDF graph saved to {output_ttl}")

# Execute the transformation
transform_csv_to_rdf('movie_triples.csv', 'film_ia.ttl')