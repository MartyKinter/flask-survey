from flask import Flask, request, render_template, redirect, flash, session
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "secret"

RESPONSES_LIST = "responses"

@app.route("/")
def show_survey_start():
    """Display survey start page"""
    return render_template("survey_start.html", survey = survey)

@app.route("/begin", methods=["POST"])
def start_survey():
    """Clear the session of responses"""
    session[RESPONSES_LIST] = []

    return redirect("/questions/0")

@app.route("/answer", methods=["POST"])
def handle_question():
    """Save responses and redirect to next page"""

    choice = request.form['answer']
    responses = session[RESPONSES_LIST]
    responses.append(choice)
    session[RESPONSES_LIST] = responses

    if(len(responses) == len(survey.questions)):
        #all questions answered
        return redirect("/complete")
    else:
        return redirect(f"/questions/{len(responses)}")

@app.route("/questions/<int:qid>")
def show_question(qid):
    """Display current question"""
    responses = session.get(RESPONSES_LIST)

    if(responses is None):
        return redirect("/")
    if(len(responses) == len(survey.questions)):
        #all questions answered
        return redirect("/complete")
    if(len(responses) != qid):
        flash(f"Invalid question id: {qid}.")
        return redirect(f"/questions/{len(responses)}")

    question = survey.questions[qid]
    return render_template("question.html", question_num=qid, 
        question=question)

@app.route("/complete")
def complete():
    """Display completed page when survey is complete"""
    return render_template("completion.html")

    