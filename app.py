from flask import Flask, render_template, request, redirect, url_for, session
import time

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Make sure to change this to a secure secret key for session management

# Login route - user must login before accessing any other pages
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Validate login credentials
        if username == 'admin' and password == 'Dinuth':
            session['logged_in'] = True  # Store login status in session
            return redirect(url_for('start'))  # Redirect to start page after successful login
        else:
            return render_template('login.html', error="Invalid credentials")  # Show error if invalid credentials

    return render_template('login.html')  # Show login page initially

# Start page - available only after successful login
@app.route('/start')
def start():
    if 'logged_in' not in session:
        return redirect(url_for('login'))  # Redirect to login page if not logged in

    return render_template('start.html')  # Display start page

# Questions page - where users can fill in answers
@app.route('/questions', methods=['GET', 'POST'])
def questions():
    if 'logged_in' not in session:
        return redirect(url_for('login'))  # Redirect to login page if not logged in

    if request.method == 'POST':
        # Store answers in the session after form submission
        answers = {key: request.form[key] for key in request.form}
        session['answers'] = answers  # Save answers to session
        return redirect(url_for('complete'))  # Redirect to the completion page after submitting answers

    # Retrieve answers from the session if any
    answers = session.get('answers', {})
    remaining_time = 120  # Timer value, can be updated dynamically if needed

    return render_template('questions.html', answers=answers, remaining_time=remaining_time)  # Display question form

# Complete page - shows submitted answers and any unanswered questions
@app.route('/complete')
def complete():
    if 'logged_in' not in session:
        return redirect(url_for('login'))  # Redirect to login if not logged in

    # Retrieve the answers and identify unanswered questions
    answers = session.get('answers', {})
    unanswered_questions = {key: value for key, value in answers.items() if not value}
    completed_answers = {key: value for key, value in answers.items() if value}

    return render_template('complete.html', answers=completed_answers, unanswered_questions=unanswered_questions)

# Restart route - clears answers and redirects to the start page
@app.route('/restart')
def restart():
    session.pop('answers', None)  # Remove answers from session
    return redirect(url_for('start'))  # Redirect to start page after restart

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
