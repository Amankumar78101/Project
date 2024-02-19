from flask import Flask, render_template, redirect, url_for, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return redirect(url_for('index'))  
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        return redirect(url_for('index'))  
    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)
