
from flask import Flask, render_template, request
from ffp_feature_transformation import transform_feature
from joblib import load
import numpy as np
from flask_wtf import FlaskForm
from ffp_form import DataEntryForm
import logging
from DatabaseConnection.Database import Connector

app = Flask(__name__)
app.config['SECRET_KEY']='406cdbd39813edf0971d172ecca5a610'


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(name)s:%(message)s')

file_handler = logging.FileHandler('app_log_files.log')
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)

@app.route("/", methods = ['GET','POST'])
def home():

  form = DataEntryForm()
  if request.method == 'POST':

    logger.info('Requested Method : POST')

    if form.is_submitted():

      logger.info('Form Submitted')

      user_input = request.form.to_dict()

      logger.info('User Input Acquired')

      try:

        if user_input['Source'] == user_input['Destination']:

          logger.warning('Source and Destination Should not be the Same')

          return render_template('ffp_index.html',form=form, value_low = '', 
                              value_high = '',rupees='', fallback_text='Source and Destination Should not be the Same')

        else:
          logger.info('Feature Transformation Request is Send')
          y = transform_feature(user_input)
          logger.info('User Input is Transformed into an Array')
          model = load('Flight_Fare_Prediction_Model.pkl')
          logger.info('Model is Loaded')
          predicted_flight_fare = model.predict([y])
          predicted_flight_fare = np.round(predicted_flight_fare)
          low = (predicted_flight_fare / 100) * 5     # 5% decrease in Fare
          high = (predicted_flight_fare / 100) * 15   # 15% increase in Fare 
          value_low = np.round(predicted_flight_fare - low)
          value_high = np.round(predicted_flight_fare + high)
          logger.info('Success! Estimated Fare is Displayed  ')
          
          return render_template('ffp_index.html',form=form, value_low = int(value_low), 
                                value_high = int(value_high), rupees='Rs', fallback_text='')
      
      except:
        logger.exception('Something Went Wrong')
        return render_template('ffp_index.html', form=form, value_low='', value_high='', rupees="", fallback_text='Something Went Wrong')

   
  return render_template('ffp_index.html', form=form, value_low=None, value_high=None, rupees="", fallback_text='')


@app.route("/DatabaseData", methods = ['GET','POST'])
def test():
    """
    :DESC: This is Hidden Api. It Retrieves Data from Database.
    :return: Render Databasedata.html Template
    """
    heading = ("id", "Airline", "Destination", "Day", "Month", "Source", "Total_Duration","Total_Stops")
    data = Connector()
    return render_template('Databasedata.html', heading=heading, data=data.getData())

if __name__ == '__main__':
	app.run(debug=True)