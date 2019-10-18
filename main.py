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
    categories = range(1,7)
    
    start_amount = 100
    stop_amount = 700
    increment = 100
    jeopardy = range(start_amount, stop_amount, increment)
    double_jeopardy = range(2*start_amount, 2*stop_amount, 2*increment)
    
    return render_template("host_setup.html", categories=categories, \
        jeopardy=jeopardy, double_jeopardy=double_jeopardy)

if __name__ == "__main__":
    app.run(debug=True)
