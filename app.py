import flask
import pickle
import pandas as pd
from flask import Flask, render_template, redirect
from flask import Flask, jsonify, render_template
from sklearn.externals import joblib

# Use pickle to load in the pre-trained model
# with open(f'model/earninings_cost_debt_type.pkl',"rb") as f:
#     model = pickle.load(f)
model = joblib.load("earninings_cost_debt_type.pkl")
modelSAT = joblib.load("SAT.pkl")
modelten = joblib.load("tenyears.pkl")
# Initialise the Flask app
app = flask.Flask(__name__, template_folder='templates')
import sys
# Set up the main route
@app.route('/', methods=['GET', 'POST'])
def main():
    if flask.request.method == 'GET':
        # Just render the initial form, to get input
        return(flask.render_template('index.html'))
    
    if flask.request.method == 'POST':
        # Extract the input
        cost = flask.request.form['cost']
        earnings = flask.request.form['earnings']
        debt = flask.request.form['debt']
        print(cost,earnings,debt, file=sys.stderr)
        math = flask.request.form['math']
        reading = flask.request.form['reading']
        print(math, reading, file=sys.stderr)
        six = flask.request.form['six']
        seven = flask.request.form['seven']
        eight = flask.request.form['eight']
        print(six, seven,eight, file=sys.stderr)
        # Make DataFrame for model
        try:
            input_variables = pd.DataFrame([[cost, earnings, debt]],
                columns=['1', '2', '3'],
                dtype=float,
                index=['input'])
        except:
            e = sys.exc_info()[0]
            print(e, file=sys.stderr)                                       
        print(input_variables, file=sys.stderr)
        input_var2 = pd.DataFrame([[reading, math]],
                                       columns=['Sat_Mp_Critical_Reading', 'Sat_Mp_Math'],
                                       dtype=float,
                                       index=['input'])
        input_var3 = pd.DataFrame([[six, seven, eight]],
                columns=['Mean_earn_6yr_postgrad', 'Mean_earn_7yr_postgrad', 'Mean_earn_8yr_postgrad'],
                dtype=float,
                index=['input'])
        # Get the model's prediction
        prediction = model.predict(input_variables)[0]
        print(prediction, file=sys.stderr)
        prediction_sat = modelSAT.predict(input_var2)[0]
        print(prediction_sat, file=sys.stderr)
        prediction_ten = modelten.predict(input_var3)[0][0]
        print(prediction_ten, file=sys.stderr)
        # jdata={'result1':int(prediction),'result2':int(prediction_sat)}
        # Render the form again, but add in the prediction and remind user
        # of the values they input before
        return flask.render_template('index.html',
                                     # original_input={'cost':cost,
                                                     # 'earnings':earnings,
                                                     # 'debt':debt},
                                     result1=prediction,
                                     # original_input2={'math':math,
                                       #                'reading':reading},
                                     result2=f'${prediction_sat[1:6]} to ${prediction_sat[8:13]}',
                                     result3='{:00.0f}'.format(prediction_ten)
                                     )
        # return jsonify(jdata)

if __name__ == '__main__':
    app.run()