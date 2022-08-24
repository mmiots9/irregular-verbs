#!/usr/bin/env python

# IMPORT
from flask import Flask, redirect, render_template, request, url_for
from classes import session as se
import pandas as pd
import random

# READ VERBS FILE
verbs = pd.read_csv("verb-list.csv")

# CREATE FLASK APP OBJECT
app = Flask(__name__)

# CREATE SESSION OBJECT
session = se.Session()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/study", methods=["POST"])
def study_session():
    return render_template("study.html", verbs_df=verbs)


@app.route("/test", methods=["GET"])
def start_test_session():
    global session

    # update existing object with a new one
    session = se.Session()

    # update session obj with verbs to be tested
    index_random = random.sample(range(0, len(verbs)),
                                 k=session.n_verbs)
    sub_verb_df = verbs.copy()
    sub_verb_df = sub_verb_df.iloc[index_random]
    session.original_verbs_df = sub_verb_df
    session.asked_verbs_df = session.original_verbs_df.copy()

    return render_template("test.html",
                           question_verb=session.next_question(),
                           q_number=(session.n_guesses + 1),
                           remaining_questions=(
                               session.n_verbs - session.n_guesses - 1))


@app.route("/test", methods=["POST"])
def test_session():
    global session
    current_answers = pd.Series(request.form.to_dict())

    # update session obj
    session.n_guesses += 1
    session.answers_df = session.answers_df.append(
        current_answers, ignore_index=True)

    if session.still_has_question():
        return render_template("test.html",
                               question_verb=session.next_question(),
                               q_number=(session.n_guesses + 1),
                               remaining_questions=(
                                   session.n_verbs - session.n_guesses - 1))
    else:
        return redirect(url_for("show_results"))


@app.route("/results")
def show_results():
    global session
    session.fix_all_df()
    checked_answers = session.check_answers()
    print(session.answers_df)
    return render_template("results.html", checked_answers=checked_answers,
                           original_verbs=session.original_verbs_df,
                           asked_verbs=session.asked_verbs_df,
                           answers=session.answers_df)


    # RUN APP
if __name__ == "__main__":
    app.run(debug=True)
