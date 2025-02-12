from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def community_garden():
    return render_template('home.html')