from datetime import datetime

from flask import Flask, Markup, render_template, request, redirect, session

from database import Card, Visit

app = Flask(__name__)

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

@app.route('/')
def home():
    return "Welcome to Twin Lakes"

def validateVisit(cID: int, guest: bool, name: str, ownerName: str, n: int):
    if cID not in Card: return False
    card = Card[cID]
    if ownerName != card.lastName: return False
    Visit.create(
        card = card,
        numberVisitors = n,
        date = datetime.now().date(),
        name=name,
        isGuest = guest
    )
    return True

@app.route('/cardnumber', methods=['GET', 'POST'])
def cardNumber():
    if request.method=='GET':
        return render_template('form.html', formBody=Markup('Please enter your card number: <input type="number" name="cID">'))
    else:
        cID = int(request.form['cID'])
        if cID in Card:
            session['cID'] = int(request.form['cID'])
            return redirect('/name')
        else:
            return "Invalid!"

@app.route('/name', methods=['GET', 'POST'])
def name():
    if request.method=='GET':
        return render_template('form.html', formBody=Markup('''
        Please enter your name: <input type="text" name="name">
        <br>
        Are you an owner or a guest? <input type="radio" name="guest" value="owner"> <input type="radio" name="guest" value="guest">
        '''))
    else:
        session['name'] = request.form['name']
        session['guest'] = request.form['guest']=='guest'
        return redirect('/ownerName')

@app.route('/ownerName', methods=['GET', 'POST'])
def ownerName():
    if request.method=='GET':
        return render_template('form.html', formBody=Markup('Please enter the card owner\'s last name: <input type="text" name="ownerName">'))
    else:
        session['ownerName'] = request.form['ownerName']
        return redirect('/numGuests')

@app.route('/numGuests', methods=['GET', 'POST'])
def numGuests():
    if request.method=='GET':
        return render_template('form.html', formBody=Markup('How many in your party: <input type="number" name="n">'))
    else:
        
        session['n'] = int(request.form['n'])
        res = "done" if validateVisit(**session) else "invalid!"
        session.clear()
        return res