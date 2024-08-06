import json
import random
import nltk
from nltk.corpus import wordnet
import time

nltk.download('wordnet')
nltk.download('omw-1.4')

# Mevcut JSON dosyasını yükleme
print("Loading JSON data...")
with open('keskop_answer.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print("JSON data loaded.")

def generate_variations(question, num_variations=10):
    words = question.split()
    variations = set()

    attempts = 0
    max_attempts = num_variations * 10  # Çok fazla deneme yapmayı engellemek için

    while len(variations) < num_variations and attempts < max_attempts:
        new_words = []
        for word in words:
            # Eş anlamlı kelime ile değiştirme
            synonyms = wordnet.synsets(word)
            if synonyms:
                synonym = synonyms[0].lemmas()[0].name()
                if synonym != word:
                    word = synonym

            new_words.append(word)
        
        # Rastgele olarak cümle büyük veya küçük harflerle yazılsın
        if random.choice([True, False]):
            variation = ' '.join(new_words).upper()
        else:
            variation = ' '.join(new_words).lower()

        variations.add(variation)
        attempts += 1

        if attempts % 10 == 0:
            print(f"Attempts: {attempts}, Current variations: {len(variations)}")

    if len(variations) < num_variations:
        print(f"Warning: Only generated {len(variations)} variations for question: {question}")

    return list(variations)

# Soruları çoğaltma
augmented_questions = {}
print("Generating variations for questions...")

start_time = time.time()
total_questions = len(data)
processed_questions = 0

for key, value in data.items():
    question = value['question']
    answer = value['answer']
    print(f"Generating variations for question {key}: {question}")
    variations = generate_variations(question)
    augmented_questions[key] = []
    for variation in variations:
        augmented_questions[key].append({"question": variation, "answer": answer})
    
    processed_questions += 1
    print(f"Processed {processed_questions}/{total_questions} questions...")

print(f"All questions processed in {time.time() - start_time:.2f} seconds.")

# Sonucu yeni bir JSON dosyasına kaydetme
print("Saving augmented questions to JSON file...")
with open('augmented_questions.json', 'w', encoding='utf-8') as f:
    json.dump(augmented_questions, f, ensure_ascii=False, indent=4)

print("Augmented questions saved to 'augmented_questions.json'.")
