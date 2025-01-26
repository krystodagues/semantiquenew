from transformers import pipeline
import pandas as pd



text = """The movie Avatar is a science fiction work directed by James Cameron and produced by 20th Century Fox. Released in 2009, it is widely known for its groundbreaking visual effects and use of 3D technology. The film is set on the planet Pandora, where humans exploit a rare resource called unobtanium, threatening the habitat of the Na'vi, a humanoid indigenous species.

The first movie was followed by several sequels. The first sequel, Avatar: The Way of Water, was released in 2022 and explores Pandora’s oceans. It focuses on the family of Jake Sully and Neytiri, as well as the conflicts with humans. A third sequel, tentatively titled Avatar 3, is scheduled for release in 2025, and its plot is expected to introduce a new Na'vi clan called the Ash People, representing a darker side of the Na'vi. Avatar 4 and Avatar 5 are also planned, with respective release dates in 2029 and 2031, promising to further expand Pandora's universe."""

# Charger le modèle REBEL
print("Loading REBEL model...")
triplet_extraction = pipeline("text2text-generation", model="Babelscape/rebel-large")

# Extraction des triplets
print("Extracting triplets...")
results = triplet_extraction(text, return_text=True, max_length=512)
triplets_raw = results[0]['generated_text']

# Traitement des triplets pour extraction
print("Processing triplets...")
triplets = []
for line in triplets_raw.split("\n"):
    if line.strip() and " -> " in line:
        subject, relation, obj = line.split(" -> ")
        triplets.append((subject.strip(), relation.strip(), obj.strip()))

# Enregistrer les triplets dans un fichier CSV
csv_filename = "triplets.csv"
print(f"Saving triplets to {csv_filename}...")
df = pd.DataFrame(triplets, columns=["Subject", "Relation", "Object"])
df.to_csv(csv_filename, index=False)

print("Triplets saved successfully!")