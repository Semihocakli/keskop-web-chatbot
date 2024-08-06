async function sendQuestion() {
    const question = document.getElementById('question').value;
    const response = await fetch('/sor', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ question: question })
    });
    const data = await response.json();
    
    // Yeni cevap elementi oluşturun
    const newAnswer = document.createElement('p');
    newAnswer.innerText = data.answer;
    
    // Cevaplar div'ine yeni cevabı ekleyin
    document.getElementById('answers').appendChild(newAnswer);
    
    // Input'u temizleyin
    document.getElementById('question').value = '';
}
