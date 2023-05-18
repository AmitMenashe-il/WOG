from flask import Flask, render_template
from Utils import SCORES_FILE_NAME, BAD_RETURN_CODE
import os

app = Flask(__name__)


@app.route('/')
def score_server():
    # checking if score file exists
    if SCORES_FILE_NAME in os.listdir():
        file = open(SCORES_FILE_NAME)
        score = file.read()
        file.close()
        #if score is read properly return score
        if score is not None and score.isdigit():
            return render_template('score.html', SCORE=score)
        #if score file is corrupt return error
        else:
            return render_template('score.html', ERROR=BAD_RETURN_CODE)
    # if no score file  return error
    else:
        return render_template('score.html', ERROR=BAD_RETURN_CODE)


#app.run()
