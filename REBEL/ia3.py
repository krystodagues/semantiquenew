from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import networkx as nx
import matplotlib.pyplot as plt
import csv

# Load the REBEL model
model_name = "Babelscape/rebel-large"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

# The text to process
text = """
The movie Avatar is a science fiction work directed by James Cameron and produced by 20th Century Fox. Released in 2009, it is widely known for its groundbreaking visual effects and use of 3D technology. The film is set on the planet Pandora, where humans exploit a rare resource called unobtanium, threatening the habitat of the Na'vi, a humanoid indigenous species.

The first movie was followed by several sequels. The first sequel is Avatar: The Way of Water wich was released in 2022 and explores Pandora's oceans. It focuses on the family of Jake Sully and Neytiri, as well as the conflicts with humans. A third sequel, tentatively titled Avatar 3, is scheduled for release in 2025, and its plot is expected to introduce a new Na'vi clan called the Ash People, representing a darker side of the Na'vi. Avatar 4 and Avatar 5 are also planned, with respective release dates in 2029 and 2031, promising to further expand Pandora's universe.
Avatar's sequels are Avatar: The Way of Water, Avatar 3, Avatar 4, and Avatar 5.

The movie Ghostbusters is a supernatural comedy directed by Ivan Reitman and written by Dan Aykroyd and Harold Ramis. Released in 1984, the story follows a team of scientists who start a ghost-catching business in New York City. The team consists of Peter Venkman, Ray Stantz, Egon Spengler, and later Winston Zeddemore.

A sequel titled Ghostbusters II was released in 1989, continuing the adventures of the original team. In 2016, a reboot titled Ghostbusters: Answer the Call was directed by Paul Feig, featuring an all-female main cast. Another sequel, Ghostbusters: Afterlife, was released in 2021, directed by Jason Reitman, and focused on a new generation discovering the Ghostbusters' legacy.
Ghostbusters'sequels are Ghostbusters II, Ghostbusters: Answer the Call, and Ghostbusters: Afterlife.


The movie Wreck-It Ralph is a computer-animated comedy film produced by Walt Disney Animation Studios and directed by Rich Moore. Released in 2012, the story follows Ralph, a video game villain who wants to become a hero, and Vanellope von Schweetz, a glitchy racer from another game.

A sequel, Ralph Breaks the Internet, was released in 2018. In this installment, Ralph and Vanellope venture into the internet to save Vanellope's game, Sugar Rush, and meet new characters like Yesss, the head algorithm of a video-sharing website, and Shank, a racer from an online game.

The movie Die Hard is an action thriller directed by John McTiernan and released in 1988. It stars Bruce Willis as John McClane, a New York police officer who becomes trapped in a Los Angeles skyscraper during a Christmas Eve hostage situation orchestrated by Hans Gruber, portrayed by Alan Rickman.

The film spawned several sequels, including Die Hard 2 (1990), Die Hard with a Vengeance (1995), Live Free or Die Hard (2007), and A Good Day to Die Hard (2013). Each sequel follows John McClane in new high-stakes scenarios, often involving family members and international threats.
Wreck-It Ralph's sequel is Ralph Breaks the Internet.


The movie The Chronicles of Narnia: The Lion, the Witch, and the Wardrobe is a fantasy film directed by Andrew Adamson and produced by Walt Disney Pictures. Released in 2005, it is based on the novel by C.S. Lewis and tells the story of the Pevensie siblings—Peter, Susan, Edmund, and Lucy—who discover the magical land of Narnia and help Aslan, a noble lion, defeat the evil White Witch.

The sequel, Prince Caspian, was released in 2008 and continues the Pevensies' adventures in Narnia. A third film, The Voyage of the Dawn Treader, was released in 2010, focusing on Edmund and Lucy's journey with Prince Caspian to find seven lost lords of Narnia.
The Chronicles of Narnia: The Lion, the Witch, and the Wardrobe's sequels are Prince Caspian and The Voyage of the Dawn Treader."""

def split_text(text, max_length=512):
    """Split text into blocks of manageable length"""
    sentences = text.split(". ")
    blocks = []
    current_block = ""
    for sentence in sentences:
        if len(current_block) + len(sentence) <= max_length:
            current_block += sentence + ". "
        else:
            blocks.append(current_block.strip())
            current_block = sentence + ". "
    if current_block:
        blocks.append(current_block.strip())
    return blocks

def extract_entities_and_relations(block):
    """Extract entities and relations from a text block"""
    inputs = tokenizer(block, return_tensors="pt", truncation=True, max_length=512)
    outputs = model.generate(**inputs)
    decoded_output = tokenizer.batch_decode(outputs, skip_special_tokens=True)
    return decoded_output[0]

def parse_rebel_output(output):
    """Parse the REBEL model output into triples"""
    triples = []
    statements = output.split('\n')
    for statement in statements:
        parts = statement.split('  ')
        if len(parts) >= 3:
            subject = parts[0].strip()
            obj = parts[1].strip()
            relation = parts[2].strip()
            if subject and obj and relation:
                triples.append((subject, relation, obj))
    return triples

def create_graph(triples):
    """Create a NetworkX graph from triples"""
    graph = nx.DiGraph()
    for triple in triples:
        if len(triple) == 3 and all(triple):
            subject, relation, obj = triple
            graph.add_node(subject)
            graph.add_node(obj)
            graph.add_edge(subject, obj, label=relation)
    return graph

def plot_graph(graph):
    """Visualize the knowledge graph"""
    plt.figure(figsize=(12,8))
    if len(graph) == 0:
        print("Warning: Graph is empty!")
        return
    pos = nx.kamada_kawai_layout(graph)
    nx.draw_networkx_nodes(graph, pos, node_color="lightblue", node_size=3000)
    nx.draw_networkx_labels(graph, pos, font_size=10, font_weight="bold")
    nx.draw_networkx_edges(graph, pos)
    edge_labels = nx.get_edge_attributes(graph, 'label')
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels)

    plt.title("Knowledge Graph")
    plt.axis('off')
    plt.tight_layout()
    plt.show()

def filter_and_export_triples(triples, output_file='movie_triples.csv'):
    """
    Filter triples containing 'characters' or 'director' and export to CSV
    
    Args:
        triples (list): List of triples (subject, relation, object)
        output_file (str): Path to output CSV file
    """
    # Filter triples
    filtered_triples = [
        triple for triple in triples 
        if 'characters' in triple[1].lower() or 'director' in triple[1].lower()
    ]
    
    # Write to CSV
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['Subject', 'Relation', 'Object'])
        csv_writer.writerows(filtered_triples)
    
    print(f"Exported {len(filtered_triples)} triples to {output_file}")
    return filtered_triples

# Main execution
text_blocks = split_text(text)

triples = []
for block in text_blocks:
    result = extract_entities_and_relations(block)
    block_triples = parse_rebel_output(result)
    triples.extend(block_triples)

print("\nExtracted Triples:")
for triple in triples:
    print(triple)

# Create and plot knowledge graph
knowledge_graph = create_graph(triples)
plot_graph(knowledge_graph)

# Export specific triples to CSV
filtered_triples = filter_and_export_triples(triples)
print("\nFiltered Triples:")
for triple in filtered_triples:
    print(triple)