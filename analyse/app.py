from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def dashboard():
    return render_template("index.html")  # Le fichier dans templates/

if __name__ == "__main__":
    app.run(debug=True)
