from flask import Flask, render_template, request

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
@app.route("/host_setup")
def host_setup():
    categories = range(1,7)

    start_amount = 100
    stop_amount = 700
    increment = 100
    jeopardy = range(start_amount, stop_amount, increment)
    double_jeopardy = range(2*start_amount, 2*stop_amount, 2*increment)

    return render_template("host_setup.html", categories=categories, \
        jeopardy=jeopardy, double_jeopardy=double_jeopardy)

@app.route("/host_setup", methods=['POST'])
def jeopardy_form_post():
    if request.method == "POST":
        categories = []
        answers = []
        questions = []

        for i in range(6):
            cat_str ="c"+ str(i+1)
            categories.append(request.form.get(cat_str))
            for n in range(6):
                que_str = "c"+ str(i+1) + "-" + str((n+1)*100)
                ans_str = "nm" + str(i+1) + "-" + str((n+1)*100)
                questions.append(request.form.get(que_str))
                answers.append(request.form.get(ans_str))
        print(categories)
        print(questions)
        print(answers)
        start_amount = 100
        stop_amount = 700
        increment = 100
        increments = range(start_amount, stop_amount, increment)
        return render_template("jeo_board.html", categories=categories, \
            answers=answers, questions=questions, increments=increments)

@app.route("/answer_page")
def answer_page():
    return render_template("answer_page.html")
if __name__ == "__main__":
    app.run(debug=True)
