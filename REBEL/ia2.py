import torch
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
import csv

def extract_rebel_triplets(text):
    """
    Extrait des triplets avec REBEL
    """
    # Charger le modèle et le tokenizer
    model = AutoModelForSeq2SeqLM.from_pretrained("Babelscape/rebel-large")
    tokenizer = AutoTokenizer.from_pretrained("Babelscape/rebel-large")

    # Tokeniser l'entrée
    inputs = tokenizer(text, max_length=512, return_tensors="pt", truncation=True)

    # Générer les triplets
    outputs = model.generate(
        inputs.input_ids, 
        max_length=512, 
        num_return_sequences=1, 
        num_beams=4
    )

    # Décoder la sortie
    decoded_output = tokenizer.decode(outputs[0], skip_special_tokens=True)
    
    # Analyser manuellement les triplets
    triplets = _parse_output(decoded_output)
    
    return triplets

def _parse_output(output):
    """
    Analyse le texte de sortie pour extraire les triplets
    """
    triplets = []
    
    # Exemple de parsing basique
    try:
        # Diviser la sortie en lignes ou en sections
        for line in output.split('\n'):
            # Vérifier si la ligne contient un triplet
            if '(' in line and ')' in line:
                # Extraire les parties du triplet
                parts = line.strip('()').split(',')
                if len(parts) == 3:
                    triplets.append({
                        'sujet': parts[0].strip(),
                        'prédicat': parts[1].strip(),
                        'objet': parts[2].strip()
                    })
    except Exception as e:
        print(f"Erreur d'extraction : {e}")
    
    return triplets

def save_to_csv(triplets, filename='rebel_triplets.csv'):
    """
    Enregistre les triplets dans un fichier CSV
    """
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['sujet', 'prédicat', 'objet']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for triplet in triplets:
            writer.writerow(triplet)
    
    print(f"Triplets enregistrés dans {filename}")

def main():
    # Texte d'exemple plus long
    texte = """James Cameron a réalisé le film Avatar en 2009. 
    Le film se déroule sur la planète Pandora et raconte l'histoire de Jake Sully, 
    un marine paraplégique qui devient un avatar des Na'vi. 
    Le film a révolutionné les effets visuels et la technologie 3D."""
    
    # Extraire les triplets
    triplets = extract_rebel_triplets(texte)
    
    # Afficher les triplets
    print("Triplets extraits :")
    for triplet in triplets:
        print(triplet)
    
    # Enregistrer dans un CSV
    save_to_csv(triplets)

if __name__ == "__main__":
    main()