import numpy as np
import pandas as pd
from markupsafe import escape
from flask import Flask, request, render_template, send_file, jsonify
import pickle
import warnings
import pandas as pd
warnings.simplefilter("ignore", UserWarning)

# Create flask app
app = Flask(__name__)

# Mapping dictionary for categorical variables
mapping_dict = {
    'Airline': {'Air Asia': 0, 'Air India': 1, 'GoAir': 2, 'IndiGo': 3, 'Jet Airways': 4, 
               'Jet Airways Business': 5, 'Multiple carriers': 6, 
               'Multiple carriers Premium economy': 7, 'No info': 8, 'SpiceJet': 9, 
               'Trujet': 10, 'Vistara': 11, 'Vistara Premium economy': 12},
    'Source': {'Banglore': 0, 'Chennai': 1, 'Delhi': 2, 'Kolkata': 3, 'Mumbai': 4, 'No info': 5},
    'Destination': {'Banglore': 0, 'Cochin': 1, 'Delhi': 2, 'Hyderabad': 3, 'Kolkata': 4, 
                   'New Delhi': 5, 'No info': 6},
    'Additional_Info': {'1 Long layover': 0, '1 Short layover': 1, '2 Long layover': 2, 
                      'Business class': 3, 'Change airports': 4, 
                      'In-flight meal not included': 5, 'No check-in baggage included': 6, 
                      'No info': 6, 'Red-eye flight': 8}
}

def convert_to_numeric(to_predict_list):
    D_DT = pd.to_datetime(to_predict_list.pop("D_DT"), format="%Y-%m-%dT%H:%M")
    A_DT = pd.to_datetime(to_predict_list.pop("A_DT"), format="%Y-%m-%dT%H:%M")
    to_predict_list.update({'D_Month':int(D_DT.month)})
    to_predict_list.update({'D_Day':int(D_DT.day)})
    to_predict_list.update({'D_Hour':int(D_DT.hour)})
    to_predict_list.update({'D_Minutes':int(D_DT.minute)})
    to_predict_list.update({'A_Month':int(A_DT.month)})
    to_predict_list.update({'A_Day':int(A_DT.day)})
    to_predict_list.update({'A_Hour':int(A_DT.hour)})
    to_predict_list.update({'A_Minutes':int(A_DT.minute)})
    DR = (((int(D_DT.hour)-int(A_DT.hour))*60) + (int(D_DT.minute)-A_DT.minute))
    to_predict_list.update({'Duration_Min':int(DR)})

# prediction function
def ValuePredictor(to_predict_list):
    # Convert categorical variables to numeric
    to_predict_list['Airline'] = mapping_dict['Airline'][to_predict_list['Airline']]
    to_predict_list['Source'] = mapping_dict['Source'][to_predict_list['Source']]
    to_predict_list['Destination'] = mapping_dict['Destination'][to_predict_list['Destination']]
    to_predict_list['Additional_Info'] = mapping_dict['Additional_Info'][to_predict_list['Additional_Info']]
    
    # Convert to list in the correct order
    feature_order = ['Airline', 'Source', 'Destination', 'Additional_Info', 'Stop_No', 
                    'D_Month', 'D_Day', 'D_Hour', 'D_Minutes', 
                    'A_Hour', 'A_Minutes', 'A_Month', 'A_Day', 'Duration_Min']
    to_predict = [to_predict_list[feature] for feature in feature_order]
    
    # Convert to numpy array and reshape
    to_predict = np.array(to_predict).reshape(1, 14)
    
    # Load model and predict
    loaded_model = pickle.load(open("model.pkl", "rb"))
    result = loaded_model.predict(to_predict)
    return result[0]
   
@app.route("/")
def Home():
    print('Request for index page received')
    return render_template("upload.html")

@app.route("/ind")
def ind():
    print('Request for individual received')
    return render_template("index.html")

@app.route("/result", methods = ["POST"])
def result():
    print('Request for predict page received')
    if request.method == 'POST':
        to_predict_list = request.form.to_dict()
        convert_to_numeric(to_predict_list)
        prediction = int(ValuePredictor(to_predict_list))
    
    return render_template("result.html", prediction_text=prediction)

@app.route("/predict_file", methods = ["POST"])
def predict_file():
    print('Request for Batch Prediction received')
    try:
        loaded_model = pickle.load(open("model.pkl", "rb"))
        df_in = pd.read_csv(request.files.get("file"))
        
        # Get the original feature names from the model
        feature_names = loaded_model.feature_names_in_
        
        # Ensure all required columns are present
        required_columns = ['Airline', 'Source', 'Destination', 'Additional_Info', 'Stop_No', 
                          'D_Month', 'D_Day', 'D_Hour', 'D_Minutes', 
                          'A_Hour', 'A_Minutes', 'A_Month', 'A_Day', 'Duration_Min']
        
        missing_columns = [col for col in required_columns if col not in df_in.columns]
        if missing_columns:
            return jsonify({'error': f'Missing columns: {", ".join(missing_columns)}'}), 400
        
        # Reorder columns to match the model's feature order
        df_in = df_in[feature_names]
        
        # Convert categorical variables to numeric
        category_col = ['Airline', 'Source', 'Destination', 'Additional_Info']
        for col in category_col:
            df_in[col] = df_in[col].map(mapping_dict[col])
        
        # Make predictions
        result = loaded_model.predict(df_in)
        df_in['Fare'] = result.tolist()
        
        # Save results
        df_in.to_csv("Predicted.csv", index=False)
        return send_file('Predicted.csv', download_name='Predicted.csv')
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)