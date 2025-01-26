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

The first movie was followed by several sequels. The first sequel, Avatar: The Way of Water, was released in 2022 and explores Pandora’s oceans. It focuses on the family of Jake Sully and Neytiri, as well as the conflicts with humans. A third sequel, tentatively titled Avatar 3, is scheduled for release in 2025, and its plot is expected to introduce a new Na'vi clan called the Ash People, representing a darker side of the Na'vi. Avatar 4 and Avatar 5 are also planned, with respective release dates in 2029 and 2031, promising to further expand Pandora's universe.


The movie Ghostbusters is a supernatural comedy directed by Ivan Reitman and written by Dan Aykroyd and Harold Ramis. Released in 1984, the story follows a team of scientists who start a ghost-catching business in New York City. The team consists of Peter Venkman, Ray Stantz, Egon Spengler, and later Winston Zeddemore.

A sequel titled Ghostbusters II was released in 1989, continuing the adventures of the original team. In 2016, a reboot titled Ghostbusters: Answer the Call was directed by Paul Feig, featuring an all-female main cast. Another sequel, Ghostbusters: Afterlife, was released in 2021, directed by Jason Reitman, and focused on a new generation discovering the Ghostbusters' legacy.

The movie Wreck-It Ralph is a computer-animated comedy film produced by Walt Disney Animation Studios and directed by Rich Moore. Released in 2012, the story follows Ralph, a video game villain who wants to become a hero, and Vanellope von Schweetz, a glitchy racer from another game.

A sequel, Ralph Breaks the Internet, was released in 2018. In this installment, Ralph and Vanellope venture into the internet to save Vanellope’s game, Sugar Rush, and meet new characters like Yesss, the head algorithm of a video-sharing website, and Shank, a racer from an online game.

The movie Die Hard is an action thriller directed by John McTiernan and released in 1988. It stars Bruce Willis as John McClane, a New York police officer who becomes trapped in a Los Angeles skyscraper during a Christmas Eve hostage situation orchestrated by Hans Gruber, portrayed by Alan Rickman.

The film spawned several sequels, including Die Hard 2 (1990), Die Hard with a Vengeance (1995), Live Free or Die Hard (2007), and A Good Day to Die Hard (2013). Each sequel follows John McClane in new high-stakes scenarios, often involving family members and international threats.



The movie The Chronicles of Narnia: The Lion, the Witch, and the Wardrobe is a fantasy film directed by Andrew Adamson and produced by Walt Disney Pictures. Released in 2005, it is based on the novel by C.S. Lewis and tells the story of the Pevensie siblings—Peter, Susan, Edmund, and Lucy—who discover the magical land of Narnia and help Aslan, a noble lion, defeat the evil White Witch.

The sequel, Prince Caspian, was released in 2008 and continues the Pevensies’ adventures in Narnia. A third film, The Voyage of the Dawn Treader, was released in 2010, focusing on Edmund and Lucy’s journey with Prince Caspian to find seven lost lords of Narnia.

The movie The Matrix is a science fiction action film directed by Lana Wachowski and Lilly Wachowski. Released in 1999, it follows Neo, played by Keanu Reeves, who discovers that reality is a simulated world controlled by intelligent machines. Guided by Morpheus and Trinity, Neo learns to fight against the machines to free humanity.

The film was followed by three sequels: The Matrix Reloaded and The Matrix Revolutions, both released in 2003, and The Matrix Resurrections, released in 2021. Each installment explores Neo’s role as “The One” and humanity’s ongoing struggle against machine domination.

The movie Toy Story is a computer-animated comedy produced by Pixar Animation Studios and directed by John Lasseter. Released in 1995, it tells the story of Woody, a cowboy doll voiced by Tom Hanks, and Buzz Lightyear, a space ranger action figure voiced by Tim Allen, as they navigate friendship and rivalry in a world where toys come to life.

The franchise expanded with three sequels: Toy Story 2 (1999), Toy Story 3 (2010), and Toy Story 4 (2019), exploring themes of loyalty, change, and belonging.

The movie Jurassic Park is a science fiction adventure film directed by Steven Spielberg and based on the novel by Michael Crichton. Released in 1993, it showcases a theme park where dinosaurs are brought back to life through genetic engineering. When the park’s security systems fail, chaos ensues as dinosaurs escape, threatening the lives of the visitors and staff.

The franchise includes sequels such as The Lost World: Jurassic Park (1997), Jurassic Park III (2001), and a reboot series starting with Jurassic World (2015), continuing with Jurassic World: Fallen Kingdom (2018) and Jurassic World Dominion (2022).

The movie Star Wars: Episode IV - A New Hope is a science fiction space opera directed by George Lucas. Released in 1977, it introduces Luke Skywalker, a young farm boy who joins a rebellion against the evil Galactic Empire. The story features iconic characters such as Princess Leia, Han Solo, Darth Vader, and Obi-Wan Kenobi.

The Star Wars saga expanded with two additional trilogies. The prequel trilogy (1999-2005) explores the rise of Anakin Skywalker, while the sequel trilogy (2015-2019) follows new characters like Rey and Kylo Ren, continuing the battle between the Light and Dark sides of the Force.

The movie The Lion King is an animated musical film produced by Walt Disney Pictures. Released in 1994, it tells the story of Simba, a lion cub who flees his home after the death of his father, Mufasa, caused by his uncle Scar. With the help of his friends Timon and Pumbaa, Simba learns to embrace his destiny and returns to reclaim his place as king of the Pride Lands.

The movie inspired a sequel, The Lion King II: Simba’s Pride (1998), a prequel, The Lion King 1½ (2004), and a live-action adaptation in 2019.

The movie Pirates of the Caribbean: The Curse of the Black Pearl is an adventure fantasy film directed by Gore Verbinski and produced by Jerry Bruckheimer. Released in 2003, it stars Johnny Depp as Captain Jack Sparrow, a witty and eccentric pirate, alongside Orlando Bloom as Will Turner and Keira Knightley as Elizabeth Swann.

The film’s success spawned a franchise, including sequels such as Dead Man’s Chest (2006), At World’s End (2007), On Stranger Tides (2011), and Dead Men Tell No Tales (2017).

The movie Finding Nemo is a computer-animated adventure film produced by Pixar Animation Studios and directed by Andrew Stanton. Released in 2003, it follows Marlin, a clownfish searching for his son Nemo, who has been captured and placed in a fish tank. Along the way, Marlin is joined by Dory, a friendly yet forgetful blue tang fish.

A sequel, Finding Dory, was released in 2016. It focuses on Dory’s journey to find her family, exploring themes of identity and perseverance.

The movie The Dark Knight is a superhero film directed by Christopher Nolan and released in 2008. It stars Christian Bale as Batman, who faces off against The Joker, played by Heath Ledger. The Joker terrorizes Gotham City, forcing Batman to confront moral dilemmas and the consequences of his vigilantism.

The movie is the second installment in the Dark Knight Trilogy, preceded by Batman Begins (2005) and followed by The Dark Knight Rises (2012).

The movie Shrek is an animated comedy film directed by Andrew Adamson and Vicky Jenson, produced by DreamWorks Animation. Released in 2001, it tells the story of Shrek, an ogre who reluctantly teams up with a talking donkey, Donkey, to rescue Princess Fiona from a tower guarded by a dragon.

The franchise expanded with sequels: Shrek 2 (2004), Shrek the Third (2007), and Shrek Forever After (2010). A spin-off, Puss in Boots, focusing on the titular character, was released in 2011 and followed by a sequel in 2022.



The movie Back to the Future is a science fiction adventure film directed by Robert Zemeckis and produced by Steven Spielberg. Released in 1985, it stars Michael J. Fox as Marty McFly, a teenager who accidentally travels back to 1955 using a time-traveling DeLorean invented by Dr. Emmett Brown, played by Christopher Lloyd. Marty must ensure his parents fall in love to avoid erasing his own existence.

The trilogy includes two sequels: Back to the Future Part II (1989) and Back to the Future Part III (1990), exploring different time periods and consequences of time travel.

The movie The Hunger Games is a dystopian science fiction film directed by Gary Ross, based on the novel by Suzanne Collins. Released in 2012, it follows Katniss Everdeen, played by Jennifer Lawrence, who volunteers to participate in the Hunger Games, a deadly televised competition where participants must fight to the death.

The series includes three sequels: Catching Fire (2013), Mockingjay - Part 1 (2014), and Mockingjay - Part 2 (2015). The films explore themes of rebellion, survival, and sacrifice.

The movie Frozen is an animated musical fantasy film produced by Walt Disney Animation Studios and directed by Chris Buck and Jennifer Lee. Released in 2013, it tells the story of Elsa, a princess with magical ice powers, and her sister Anna, who embarks on a journey with Kristoff and his reindeer Sven to save their kingdom from eternal winter.

A sequel, Frozen II, was released in 2019, delving deeper into Elsa's powers and the sisters’ family history.

The movie Iron Man is a superhero film directed by Jon Favreau and produced by Marvel Studios. Released in 2008, it stars Robert Downey Jr. as Tony Stark, a billionaire inventor who creates a high-tech suit of armor to escape captivity and later uses it to fight evil as the superhero Iron Man.

The movie launched the Marvel Cinematic Universe (MCU), leading to sequels Iron Man 2 (2010) and Iron Man 3 (2013), as well as Stark’s appearances in The Avengers series and other MCU films.

The movie The Incredibles is an animated superhero film produced by Pixar Animation Studios and directed by Brad Bird. Released in 2004, it follows the Parr family, a group of superheroes forced to live normal lives after superheroes are banned. The family includes Mr. Incredible, Elastigirl, and their children Violet, Dash, and Jack-Jack.

A sequel, Incredibles 2, was released in 2018, focusing on Elastigirl’s efforts to restore superheroes’ reputation while Mr. Incredible manages the family.

The movie Spider-Man is a superhero film directed by Sam Raimi and released in 2002. It stars Tobey Maguire as Peter Parker, a teenager who gains spider-like abilities after being bitten by a radioactive spider. As Spider-Man, he battles villains like the Green Goblin, played by Willem Dafoe, while navigating his personal life.

The original trilogy includes Spider-Man 2 (2004) and Spider-Man 3 (2007). The character was rebooted in The Amazing Spider-Man series (2012-2014) and later incorporated into the Marvel Cinematic Universe with Tom Holland as Spider-Man.

The movie Titanic is a romantic drama film directed by James Cameron. Released in 1997, it stars Leonardo DiCaprio as Jack Dawson and Kate Winslet as Rose DeWitt Bukater, two passengers from different social classes who fall in love aboard the RMS Titanic, a luxurious ship that tragically sank during its maiden voyage in 1912 after hitting an iceberg.

The film explores themes of love, sacrifice, and class division, set against the backdrop of a historical disaster. It won 11 Academy Awards, including Best Picture and Best Director, and became one of the highest-grossing films of all time.
"""

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

def filter_and_export_triples(triples, output_file='movie_triples2.csv'):
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

    