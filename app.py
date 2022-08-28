from http.client import responses
from flask import Flask, render_template, request, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey

app = Flask(__name__)

app.debug = True
app.config['SECRET_KEY'] = 'FISH'

toolbar = DebugToolbarExtension(app)

# ----------


@app.route("/")
def home_page():
    return render_template("home.html", survey=satisfaction_survey)


@app.route("/start")
def start_survey():
    # create a session with "responses" as
    # the key and an empty string as its value
    session["responses"] = []
    return redirect("/questions/1")


@app.route("/questions/<int:number>")
def questions_page(number):

    # The page number will always be 1 higher
    # because I wanted the questions to start
    # at 1 instead of 0, so subtract 1 from
    # 'number' for list index purposes
    number -= 1

    # responses = the value of "responses" in our session cookie
    responses = session.get("responses")

    if len(responses) == len(satisfaction_survey.questions):
        return redirect("/complete")

    if (number != len(responses)):
        flash("Nice try!")
        # The '+1' at the end is to make it so
        # questions start at 1 instead of 0
        return redirect(f"/questions/{len(responses) + 1}")

    question = satisfaction_survey.questions[number].question
    choices = satisfaction_survey.questions[number].choices

    return render_template("questions.html", question=question, choices=choices)


@app.route("/answer", methods=["POST"])
def answer_page():

    # to add latest response to our session list
    responses = session["responses"]
    responses.append(request.form["choice"])
    session["responses"] = responses

    return redirect(f"/questions/{len(responses) + 1}")


@app.route("/complete")
def complete_page():
    return render_template("complete.html")
