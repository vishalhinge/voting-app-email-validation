from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

CANDIDATES = [
    "Alice", "Bob", "Charlie", "Diana", "Eve",
    "Frank", "Grace", "Heidi", "Ivan", "Judy"
]

def init_db():
    conn = sqlite3.connect("data/votes.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS votes (
                    email TEXT PRIMARY KEY,
                    choices TEXT
                )''')
    conn.commit()
    conn.close()

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        email = request.form.get("email").strip().lower()
        selections = request.form.getlist("captains")
        if len(selections) != 6:
            return "Please select exactly 6 captains.", 400

        conn = sqlite3.connect("data/votes.db")
        c = conn.cursor()
        c.execute("SELECT * FROM votes WHERE email = ?", (email,))
        if c.fetchone():
            conn.close()
            return "You have already voted.", 403
        c.execute("INSERT INTO votes (email, choices) VALUES (?, ?)",
                  (email, ",".join(selections)))
        conn.commit()
        conn.close()
        return render_template("thankyou.html", email=email)
    return render_template("index.html", candidates=CANDIDATES)

if __name__ == "__main__":
    os.makedirs("data", exist_ok=True)
    init_db()
    app.run(host="0.0.0.0", port=5000)