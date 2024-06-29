import pickle
import string
import numpy as np
from flask import Flask, request, jsonify, render_template
app = Flask(__name__)
model = pickle.load(open('model.pkl', 'rb'))

# Initialize an empty database list
database = []

@app.route('/')
def home():
    return render_template('index.html', pred_val=None, database=database)
@app.route('/predict', methods=['POST'])


def predict():
    int_features = [int(x) for x in request.form.values()]
    int_features[0] *= 0.4
    int_features[1] *= 0.9
    int_features[2] *= 2400
    int_features[3] *= 750000
    int_features[4] *= 0.36
    int_features = [round(x, 2) for x in int_features]

    est_diameter_min = int(request.form['est_diameter_min'])
    est_diameter_max = int(request.form['est_diameter_max'])
    relative_velocity = int(request.form['relative_velocity'])
    miss_distance = int(request.form['miss_distance'])
    absolute_magnitude = int(request.form['absolute_magnitude'])


    est_diameter_min *= 0.4
    est_diameter_max *= 0.9
    relative_velocity *= 2400
    miss_distance *= 750000
    absolute_magnitude *= 0.36

    est_diameter_min = round(est_diameter_min, 2)
    est_diameter_max = round(est_diameter_max, 2)
    relative_velocity = round(relative_velocity, 2)
    miss_distance = round(miss_distance, 2)
    absolute_magnitude = round(absolute_magnitude, 2)
    

    final_features = [np.array(int_features)]
    prediction = model.predict(final_features)
    output = round(prediction[0], 2)
    prediction_text = """For asteroid with parameters set to: XXX est_diameter_min: {} km, XXX est_diameter_max: {} km, XXX relative velocity: {} km/h, XXX miss distance: {} km, XXX absolute magnitude: {}, XXX prediction is: {} XXX ([0] - safe, [1] - hazardous)""".format(int_features[0], int_features[1], int_features[2], int_features[3], int_features[4], output)
    formatted_text = prediction_text.replace('XXX', '<br>')

    id_letter = string.ascii_uppercase[len(database) % 26]
    asteroid_id = f"2024 O{id_letter}"

    # Create a dictionary with the input data and the prediction
    asteroid = {
        'id': asteroid_id,
        'est_diameter_min': est_diameter_min,
        'est_diameter_max': est_diameter_max,
        'relative_velocity': relative_velocity,
        'miss_distance': miss_distance,
        'absolute_magnitude': absolute_magnitude,
        'hazardous': int(prediction)
    }

    # Add the dictionary to the database list at the first position
    database.insert(0, asteroid)

    # Keep only the last 5 entries
    if len(database) > 5:
        database.pop()


   
    return render_template('index.html', prediction_text=formatted_text, pred_val=output, database=database )
@app.route('/results', methods=['POST'])
def results():
    data = request.get_json(force=True)
    prediction = model.predict([np.array(list(data.values()))])
    output = prediction[0]
    return jsonify(output)
if __name__ == "__main__":
    app.run(debug=True)