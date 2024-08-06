import json
import random
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
import joblib

# JSON dosyasını yükle
with open('augmented_questions.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# Verileri hazırla
questions = []
labels = []

for key, value in data.items():
    for entry in value:
        questions.append(entry['question'])
        labels.append(key)

# TF-IDF vektörleme
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(questions)

# Lineer SVM modeli oluştur
model = LinearSVC()
model.fit(X, labels)

# Modeli kaydet
joblib.dump(model, 'svm_model.pkl')

# Test verisi için fonksiyon tanımla
def predict_answer(question):
    question_vec = vectorizer.transform([question])
    prediction = model.predict(question_vec)[0]
    
    for entry in data[prediction]:
        if entry['question'].lower() == question.lower():
            return entry['answer']

    return "Üzgünüm, bu soruya yanıt bulunamadı."

# # Örnek kullanım
# if __name__ == "__main__":
#     test_question = "İş yeri açacağım bu krediden faydalanabilir miyim?"
#     answer = predict_answer(test_question)
#     print(f"Soru: {test_question}")
#     print(f"Cevap: {answer}")

