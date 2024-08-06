from flask import Flask, request, jsonify, render_template
import joblib
import json
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

with open('augmented_questions.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

rows = []
for answers in data.values():
    for item in answers:
        rows.append({"question": item["question"], "answer": item["answer"]})

df = pd.DataFrame(rows)

model = joblib.load('chatbot_model.pkl')

# TfidfVectorizer'ı modelden al
vectorizer = model.named_steps['tfidfvectorizer']

# Tüm soruları ve cevapları içeren bir liste oluştur
questions = df['question'].tolist()
answers = df['answer'].tolist()

# Soruları TF-IDF vektörlerine dönüştür
tfidf_matrix = vectorizer.transform(questions)

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chatbot', methods=['POST'])
def chatbot():
    user_input = request.form['user_input']

    # Eğer kullanıcı bir ID girdiyse
    if user_input.isdigit():
        if user_input in data:
            return jsonify({'response': data[user_input][0]['answer']})
        else:
            return jsonify({'response': 'Geçersiz ID girdiniz.'})

    # Eğer kullanıcı manuel olarak bir soru girdiyse
    else:
        # Kullanıcıdan gelen soruyu TF-IDF vektörüne dönüştür
        user_question_vector = vectorizer.transform([user_input])
        
        # Kullanıcı sorusu ile tüm sorular arasındaki cosine similarity hesapla
        cosine_similarities = cosine_similarity(user_question_vector, tfidf_matrix).flatten()
        
        # En yüksek benzerlik skoruna sahip sorunun indeksini bul
        highest_similarity_index = np.argmax(cosine_similarities)
        highest_similarity_score = cosine_similarities[highest_similarity_index]
        
        similarity_threshold = 0.5
        
        if highest_similarity_score >= similarity_threshold:
            return jsonify({'response': answers[highest_similarity_index]})
        else:
            return jsonify({'response': 'Böyle bir soru yok.'})

if __name__ == '__main__':
    app.run(debug=True)
