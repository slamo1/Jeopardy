from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

"""
We will define the paths here. Link Different HTML Pages,

CSS under static

<------------HOME------------->
            |    |
        HOST      PLAYER
"""
@app.route("/host_setup", methods=['GET', 'POST'])
def host_setup():
    return render_template("host_setup.html")

if __name__ == "__main__":
    app.run(debug=True)
