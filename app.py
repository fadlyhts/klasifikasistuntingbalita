from flask import Flask, request, render_template, jsonify
from flask_cors import CORS
import os
import pickle
import pandas as pd
import numpy as np

app = Flask(__name__, static_folder='.', static_url_path='')

# Update CORS configuration
CORS(app, resources={
    r"/*": {
        "origins": ["https://fadlyhts.github.io", "http://localhost:5000", "https://klasifikasistuntingbalita.onrender.com"],
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})

# Load model
with open('stunting_model.pkl', 'rb') as f:
    model_objects = pickle.load(f)

scaler = model_objects['scaler']
feature_scores = model_objects['feature_scores']
best_models = model_objects['best_models']
target_columns = model_objects['target_columns']
k = model_objects['k']

def predict_status(input_data):
    try:
        # Define feature names exactly as in klasifikasi_fix.py
        feature_names = ['jk', 'bb_lahir', 'tb_lahir', 'berat', 'tinggi',
                        'zs_bbu', 'zs_tbu', 'zs_bbtb']
        
        # Create DataFrame with exact same structure as training
        input_df = pd.DataFrame([input_data], columns=feature_names)
        
        # Scale features using the same scaler
        input_scaled = pd.DataFrame(
            scaler.transform(input_df),
            columns=feature_names
        )

        status_maps = {
            'status_bbu': {
                0: 'Berat Badan Normal',
                1: 'Kurang',
                2: 'Sangat Kurang',
                3: 'Risiko Lebih'
            },
            'status_tbu': {
                0: 'Pendek',
                1: 'Sangat Pendek'
            },
            'status_bbtb': {
                0: 'Gizi Baik',
                1: 'Gizi Kurang',
                2: 'Gizi Buruk',
                3: 'Gizi Lebih',
                4: 'Obesitas',
                5: 'Risiko Gizi Lebih'
            }
        }

        predictions = {}
        for target in target_columns:
            # Get selected features for this target exactly as in training
            selected_features = feature_scores[target]['Feature'].head(k).tolist()
            
            # Use all possible features needed by the model
            all_possible_features = set(selected_features)
            if hasattr(best_models[target], 'feature_names_in_'):
                all_possible_features.update(best_models[target].feature_names_in_)

            # Prepare features in correct order
            X_pred = input_scaled[list(all_possible_features)].copy()
            
            # Get model and predict
            model = best_models[target]
            if hasattr(model, 'feature_names_in_'):
                required_features = model.feature_names_in_
                X_pred_ordered = X_pred[required_features]
                pred = model.predict(X_pred_ordered)
            else:
                X_pred_selected = X_pred[selected_features]
                pred = model.predict(X_pred_selected)

            predictions[target] = status_maps[target].get(int(pred[0]), 'Unknown')

        return predictions
    except Exception as e:
        print(f"Error in predict_status: {str(e)}")
        raise

@app.route('/')
def home():
    return app.send_static_file('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Data tidak ditemukan'}), 400

        # Convert and validate input
        processed_data = {
            'jk': 1 if str(data.get('jk', '')).upper() in ['L', 'LAKI', 'LAKI-LAKI'] else 0,
            'bb_lahir': float(data.get('bb_lahir', 0) or 0),
            'tb_lahir': float(data.get('tb_lahir', 0) or 0),
            'berat': float(data.get('berat', 0) or 0),
            'tinggi': float(data.get('tinggi', 0) or 0),
            'zs_bbu': float(data.get('zs_bbu', 0) or 0),
            'zs_tbu': float(data.get('zs_tbu', 0) or 0),
            'zs_bbtb': float(data.get('zs_bbtb', 0) or 0)
        }

        # Validate values
        for key, value in processed_data.items():
            if value == 0 and key != 'jk':
                return jsonify({'error': f'Field {key} harus diisi dengan benar'}), 400

        print("Processing data:", processed_data)
        result = predict_status(processed_data)
        print("Prediction result:", result)
        
        return jsonify(result)
    except ValueError as ve:
        print(f"Value Error: {str(ve)}")
        return jsonify({'error': str(ve)}), 400
    except Exception as e:
        print(f"Error in predict route: {str(e)}")
        return jsonify({'error': 'Terjadi kesalahan internal'}), 500

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', 'https://fadlyhts.github.io')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,POST,OPTIONS')
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))