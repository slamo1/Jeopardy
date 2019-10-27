from flask import Flask, render_template, request, session, redirect, url_for

app = Flask(__name__)

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

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

    if request.method == 'GET':

        jeopardy = range(start_amount, stop_amount, increment)
        double_jeopardy = range(2*start_amount, 2*stop_amount, 2*increment)

        return render_template("host_setup.html", categories=categories, \
            jeopardy=jeopardy, double_jeopardy=double_jeopardy)

    if request.method == "POST":
        categories = []
        increments = []

        master = []
        for i in range(6):
            cat_str ="c"+ str(i+1)
            categories.append(request.form.get(cat_str))

            jeop_board = {}
            for n in range(6):
                val = (n+1)*100
                increments.append(val)
                que_str = "c"+ str(i+1) + "-" + str(val)
                ans_str = "nm" + str(i+1) + "-" + str(val)
                jeop_board[val] = [request.form.get(que_str), request.form.get(ans_str), 1]
            master.append(jeop_board)
                #questions.append(request.form.get(que_str))
                #answers.append(request.form.get(ans_str))
        increments = list(range(start_amount, stop_amount, increment))
        session['jeopardy'] = master
        session['categories'] = categories
        session['increments'] = increments

        return redirect(url_for('jeopardy_form_post'))


@app.route("/jeopardy_board", methods=['GET', 'POST'])
def jeopardy_form_post():
    return render_template("jeo_board.html", categories=session['categories'], \
            increments=session['increments'], board=session['jeopardy'])



@app.route("/answer_page/<category>/<value>")
def answer_page(category, value):
    category = int(category)
    
    # Pop out and update the board
    jeopardy_board = session.pop('jeopardy')
    question = jeopardy_board[category][value][0]
    answer = jeopardy_board[category][value][1]
    jeopardy_board[category][value][2] = 0

    session['jeopardy'] = jeopardy_board

    return render_template("answer_page.html", question=question, answer=answer)



if __name__ == "__main__":
    app.run(debug=True)
