from flask import Flask, render_template, redirect, url_for, request,Response

app = Flask(__name__)
app = app()

@app.route('/')
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)