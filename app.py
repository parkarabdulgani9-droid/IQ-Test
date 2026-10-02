import random
import sqlite3
import os
from flask import (
    Flask,
    render_template,
    request,
    jsonify,
    redirect,
    url_for,
    session
)
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# The Question Bank is now stored on the server
question_bank = [
    { "q": "If a doctor gives you 3 pills and tells you to take one every half hour, how long will they last?", "a": ["30 minutes", "60 minutes", "90 minutes", "120 minutes"], "correct": 1 },
    { "q": "A father and son get in a car crash. The father dies. The son is rushed to the hospital. The surgeon says, 'I can't operate on him, he's my son!' Who is the surgeon?", "a": ["Grandfather", "Mother", "Uncle", "Stepfather"], "correct": 1 },
    { "q": "How many months have 28 days?", "a": ["1", "2", "6", "12"], "correct": 3 },
    { "q": "If you are running in a race and you pass the person in 2nd place, what place are you in?", "a": ["1st", "2nd", "3rd", "Last"], "correct": 1 },
    { "q": "A farmer has 17 sheep, and all but 9 die. How many sheep are left alive?", "a": ["8", "9", "0", "17"], "correct": 1 },
    { "q": "Divide 30 by 1/2 and add 10. What is the answer?", "a": ["25", "40", "70", "20"], "correct": 2 },
    { "q": "If 5 cats can catch 5 mice in 5 minutes, how many minutes does it take 100 cats to catch 100 mice?", "a": ["100 minutes", "5 minutes", "1 minute", "50 minutes"], "correct": 1 },
    { "q": "Some months have 31 days, others have 30. How many have 31?", "a": ["5", "6", "7", "12"], "correct": 2 },
    { "q": "Mary's father has 5 daughters: Nana, Nene, Nini, Nono. What is the 5th daughter's name?", "a": ["Nunu", "Mary", "Nina", "Nono"], "correct": 1 },
    { "q": "How many 0.5cm x 0.5cm square tiles do you need to cover a 1cm x 1cm square?", "a": ["2", "4", "8", "16"], "correct": 1 },
    { "q": "If you have 6 apples and you take away 4, how many do you have?", "a": ["2", "4", "6", "0"], "correct": 1 },
    { "q": "Before Mount Everest was discovered, what was the highest mountain in the world?", "a": ["K2", "Mount Kilimanjaro", "Mount Everest", "Kangchenjunga"], "correct": 2 },
    { "q": "A plane crashes on the border of the US and Canada. Where do they bury the survivors?", "a": ["US", "Canada", "In the border zone", "You don't bury survivors"], "correct": 3 },
    { "q": "If a rooster lays an egg on the top of a slanted roof, which way will it roll?", "a": ["Left", "Right", "Roosters don't lay eggs", "Downwards"], "correct": 2 },
    { "q": "What is heavy forward, but backward is NOT?", "a": ["Ton", "Star", "Weight", "Shadow"], "correct": 0 },
    { "q": "What comes next in the pattern: 1, 4, 9, 16, 25, ...?", "a": ["30", "35", "36", "49"], "correct": 2 },
    { "q": "If A = 1, B = 2, C = 3, what is the value of FACE?", "a": ["15", "18", "12", "14"], "correct": 0 },
    { "q": "Which shape has 8 sides?", "a": ["Hexagon", "Octagon", "Pentagon", "Heptagon"], "correct": 1 },
    { "q": "If 3 cats catch 3 mice in 3 minutes, how many cats are needed to catch 100 mice in 100 minutes?", "a": ["3", "100", "30", "1"], "correct": 0 },
    { "q": "Which number is the prime number?", "a": ["9", "15", "21", "17"], "correct": 3 }
]

app.secret_key = os.environ.get("SECRET_KEY", "change-this-secrect-key")
DATABASE = "database.db"

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():

    conn = get_db()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            average_iq REAL DEFAULT 0,
            highest_iq REAL DEFAULT 0
        )
    """)

    conn.commit()
    conn.close()

@app.route("/")
def home():
    return redirect(url_for("login"))

@app.route("/register", methods=["GET", "POST"])
def register():
    error = None

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        if not username or not password:
            error = "Username and password are required."
        elif len(password) < 6:
            error = "Password must be at least 6 characters long."
        else:
            conn = get_db()
            existing = conn.execute("SELECT id FROM users WHERE username = ?", (username,)
            ).fetchone()
            if existing:
                error = "Username already exists."
            else:
                password_hash = generate_password_hash(password)
                conn.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", (username, password_hash))

                conn.commit()
                conn.close()

                return redirect(url_for("login"))

            conn.close()

    return render_template("register.html", error=error)

@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        conn = get_db()
        user = conn.execute(
            "SELECT * FROM users WHERE username = ?", (username,)
        ).fetchone()
        conn.close()
        if user and check_password_hash(user["password_hash"], password):
            session["user_id"] = user["id"]
            return redirect(url_for("dashboard"))
        else:
            error = "Invalid username or password."
    return render_template("login.html", error=error)

@app.route("/get_questions")
def get_questions():
    if "user_id" not in session:
        return jsonify({
            "error" : "Unauthorized"
        }), 401
    questions = question_bank.copy()
    random.shuffle(questions)
    return jsonify(questions)

@app.route("/quiz")
def quiz():
    if "user_id" not in session:
        return redirect(url_for("login"))
    questions = random.sample(question_bank, 10)
    return render_template("quiz.html", questions=questions)

@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("login"))
    user_id = session["user_id"]
    conn = get_db()
    user = conn.execute(
        "SELECT * FROM users WHERE id = ?", (user_id,)
    ).fetchone()
    conn.close()
    return render_template("dashboard.html", user=user)

@app.route("/change-username", methods=["GET", "POST"])
def change_username():
    if "user_id" not in session:
        return redirect(url_for("login"))
    error = None
    if request.method == "POST":
        new_username = request.form.get("username", "").strip()
        if not new_username:
            error = "New username is required."
        else:
            conn = get_db()
            existing = conn.execute(
                "SELECT id FROM users WHERE username = ? AND id != ?",
                (new_username, session["user_id"])
            ).fetchone()
            if existing:
                error = "Username already exists."
            else:
                conn.execute(
                    "UPDATE users SET username = ? WHERE id = ?",
                    (new_username, session["user_id"])
                )
                conn.commit()
                conn.close()
                return redirect(url_for("dashboard"))
            conn.close()
    return render_template("change_username.html", error=error)

@app.route("/change-password", methods=["GET", "POST"])
def change_password():
    if "user_id" not in session:
        return redirect(url_for("login"))
    error = None
    if request.method == "POST":
        current_password = request.form.get("current_password")
        new_password = request.form.get("new_password")
        confirm_password = request.form.get("confirm_password")

        conn = get_db()
        user = conn.execute(
            "SELECT * FROM users WHERE id = ?", (session["user_id"],)
        ).fetchone()
        if not check_password_hash(user["password_hash"], current_password):
            error = "current password is incorrect."
        elif not new_password:
            error = "new password cannot be empty."
        elif new_password != confirm_password:
            error = "new passwords do not match."
        else:
            password_hash = generate_password_hash(new_password)
            conn.execute("UPDATE users SET password_hash = ? WHERE id = ?",
                         (password_hash, session["user_id"]))
            conn.commit()
            conn.close()
            return redirect(url_for("dashboard"))
        conn.close()
    return render_template("change_password.html", error = error)
        

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)