# IMPORT
from random import choice
import pandas as pd

# COSTANTS
N_VERBS = 10


# CLASS
class Session:
    def __init__(self):
        self.n_verbs = N_VERBS
        self.n_guesses = 0
        self.original_verbs_df = None
        self.asked_verbs_df = None
        self.answers_df = pd.DataFrame()

    def still_has_question(self):
        return self.n_verbs > self.n_guesses

    def next_question(self):
        to_not_ask = choice(list(self.asked_verbs_df.columns))

        self.asked_verbs_df.iloc[self.n_guesses,
                                 self.asked_verbs_df.columns != to_not_ask] = None

        next_question_df = self.asked_verbs_df.iloc[self.n_guesses].to_frame(
        ).transpose()
        return next_question_df

    def fix_all_df(self):
        self.fix_verbs_df()
        self.fix_answer_df()

    def fix_verbs_df(self):
        self.original_verbs_df.reset_index(inplace=True, drop=True)
        self.asked_verbs_df.reset_index(inplace=True, drop=True)

        self.original_verbs_df = self.original_verbs_df.apply(
            lambda x: x.astype(str).str.lower())
        self.asked_verbs_df = self.asked_verbs_df.apply(
            lambda x: x.astype(str).str.lower())

    def fix_answer_df(self):
        self.answers_df = self.answers_df.apply(
            lambda x: x.astype(str).str.lower())
        try:
            self.answers_df = self.answers_df[self.original_verbs_df.columns.values]
        except KeyError as key:
            to_add = key.args[0].split("'")[1]
            self.answers_df[to_add] = None
        finally:
            self.answers_df = self.answers_df[self.original_verbs_df.columns.values]

        self.answers_df[self.answers_df == ""] = "NV"

    def check_answers(self):
        return self.answers_df == self.original_verbs_df
