import os
import pandas as pd

from flask import Flask, render_template, request, session, redirect, url_for, flash
from werkzeug.utils import secure_filename


app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'questions')
ALLOWED_EXTENSIONS = set(['csv'])

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.mkdir(UPLOAD_FOLDER)

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
    increments = list(range(start_amount, stop_amount, increment))

    if request.method == 'GET':
        return render_template("host_setup.html", categories=categories, \
            jeopardy=jeopardy, double_jeopardy=double_jeopardy)

    if request.method == "POST":
        category_strings = []

        master = []
        for i in categories:
            cat_str ="c"+ str(i)
            category_strings.append(request.form.get(cat_str))

            jeop_board = {}
            for n in range(6):
                val = (n+1)*100
                que_str = "c"+ str(i+1) + "-" + str(val)
                ans_str = "nm" + str(i+1) + "-" + str(val)
                jeop_board[val] = [request.form.get(que_str), request.form.get(ans_str), 1]
            master.append(jeop_board)
                #questions.append(request.form.get(que_str))
                #answers.append(request.form.get(ans_str))

        session['jeopardy'] = master
        session['categories'] = category_strings
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

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            
            # Process the file - this need additional check and to be moved into its own function.
            ## MESSY
            questions = pd.read_csv(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            increments = list(set(questions['Value'].values.astype(str)))
            increments.sort()
            print("HELLO")
            print(increments)

            category_groups = questions.groupby(by='Category Name')
            categories = list(category_groups.groups)

            board = []
            for category, data in category_groups:
                category_dict = {}
                for index, question in data.iterrows():
                    category_dict[str(question['Value'])] = [question['Question'], question['Answer'], 1]
                
                board.append(category_dict)
            
            session['jeopardy'] = board
            session['categories'] = categories
            session['increments'] = increments

            return redirect(url_for('jeopardy_form_post'))
    return render_template("upload.html")

if __name__ == "__main__":
    app.run(debug=True)
