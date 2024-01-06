# main.py

from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Set up SQLite3 database
conn = sqlite3.connect('feedback.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS feedback (id INTEGER PRIMARY KEY AUTOINCREMENT, liked TEXT)''')
conn.commit()
conn.close()

# Survey page route
@app.route('/', methods=['GET', 'POST'])
def survey():
    if request.method == 'POST':
        liked = request.form['liked']
        conn = sqlite3.connect('feedback.db')
        c = conn.cursor()
        c.execute('INSERT INTO feedback (liked) VALUES (?)', (liked,))
        conn.commit()
        conn.close()
        return redirect(url_for('thank_you'))
    return render_template('survey.html')

# Thank you page route
@app.route('/thankyou')
def thank_you():
    return render_template('thankyou.html')

# Admin page route
@app.route('/admin')
def admin():
    conn = sqlite3.connect('feedback.db')
    c = conn.cursor()
    c.execute('SELECT * FROM feedback')
    feedback_records = c.fetchall()
    conn.close()
    return render_template('admin.html', feedback_records=feedback_records)

if __name__ == '__main__':
    app.run(debug=True)