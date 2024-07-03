from flask import Flask
from flask import render_template
from flask import make_response
from flask import request
from flask import redirect

app = Flask(__name__)

@app.route("/")
def hello_world():
    # check cookie if logged in
    # if not logged in, redirect to login page
    # if logged in, render index page
    if request.cookies.get('name'):
        return render_template('index.html', name=request.cookies.get('name'))
    else:
        return redirect('/login')

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if not request.form['name']:
            return render_template('login.html', error='Name is required')
        if not request.form['password']:
            return  render_template('login.html', error='Password is required')
        
        if request.form['name'] != 'admin' or request.form['password'] != 'admin':
            return render_template('login.html', error='Invalid credentials')
        
        response = make_response(redirect('/'))
        response.set_cookie('name', request.form['name'])
        return response
    else:
        if request.cookies.get('name'):
            return redirect('/')
        return render_template('login.html')

@app.route("/logout", methods=['POST'])
def logout():
    response = make_response(redirect('/login'))
    response.set_cookie('name', '', expires=0)
    return response

    

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)