from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)

@app.route('/')
def welcome(name=None):

    return render_template('welcome.html', name=name)



    

    



