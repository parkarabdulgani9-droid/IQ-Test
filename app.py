from flask import Flask, render_template, jsonify

app = Flask(__name__)

# The Question Bank is now stored on the server
question_bank = [
    { "q": "Next in sequence: 2, 6, 12, 20, 30, ...?", "a": ["36", "40", "42", "48"], "correct": 2 },
    { "q": "If CAT = 24, then DOG = ?", "a": ["26", "27", "25", "28"], "correct": 0 },
    { "q": "Rearrange 'CIFAIPIC' to find a(n):", "a": ["Animal", "City", "Ocean", "Country"], "correct": 2 },
    { "q": "Book is to Read as Knife is to:", "a": ["Sharp", "Cut", "Steel", "Kitchen"], "correct": 1 },
    { "q": "What is 15% of 200?", "a": ["25", "30", "35", "40"], "correct": 1 },
    { "q": "Next in sequence: 8, 27, 64, 125, ...?", "a": ["196", "216", "256", "225"], "correct": 1 },
    { "q": "Which does not belong?", "a": ["Apple", "Carrot", "Banana", "Grape"], "correct": 1 },
    { "q": "A train goes 100km in 2 hours. Speed?", "a": ["40 km/h", "50 km/h", "60 km/h", "70 km/h"], "correct": 1 },
    { "q": "Which is the odd one out?", "a": ["Gold", "Silver", "Iron", "Bronze"], "correct": 3 },
    { "q": "If FLOWER = GMRQYG, then FRUIT = ?", "a": ["GSVJT", "GSUJT", "HSVJT", "GSVJU"], "correct": 0 }
]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_questions')
def get_questions():
    # This route allows the JavaScript to fetch the data
    return jsonify(question_bank)

if __name__ == '__main__':
    app.run(debug=True)