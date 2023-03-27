from flask import Flask,request, url_for, redirect, render_template
import pickle
import numpy as np
import sys
from sys import stderr
import logging
from netflix_recommendation import netflix_recommendations


logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)



@app.route('/')
def hello_world():
    return render_template("home.html")


@app.route('/predict',methods=['POST','GET'])
def predict():
    app.logger.info("what")
    input=[str(x) for x in request.form.values()]
    moviename = np.array(input)[0]
    # app.logger.info(movieename)
    try: 
        movie, score = netflix_recommendations(moviename)
    except:
        pass
    
    
    
    
    try:
        
        return render_template('result.html',pred="Your #1 movie based on your last watch will be {} with {}% match. <br>Your #2 movie based on your last watch will be {} with {}% match.</br>Your #3 movie based on your last watch will be {} with {}% match. <br>Your #4 movie based on your last watch will be {} with {}% match. </br> Your #5 movie based on your last watch will be {} with {}% match.".format(movie[0],score[0],movie[1],score[1],movie[2],score[2],movie[3],score[3],movie[4],score[4]))
    except:
        return render_template('result.html',pred="Aww snap! Couldn't find this particular movie/TV series")

    # if output>str(0.5):
    #     return render_template('forest_fire.html',pred='Your Forest is in Danger.\nProbability of fire occuring is {}'.format(output),bhai="kuch karna hain iska ab?")
    # else:
    #     return render_template('forest_fire.html',pred='Your Forest is safe.\n Probability of fire occuring is {}'.format(output),bhai="Your Forest is Safe for now")


if __name__ == '__main__':
    app.run(debug=True)
