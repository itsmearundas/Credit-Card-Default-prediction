import joblib
import pandas as pd
import numpy as np
from flask import Flask, request, render_template, jsonify

# Load the trained Random Forest model
model_filename = 'random_forest_credit_default_model.joblib'
loaded_model = joblib.load(model_filename)

# Define the preprocessing steps
def preprocess_input(data):
    """
    Preprocesses a single data point (dictionary) to match the format
    expected by the trained Random Forest model.
    """
    # Convert the single data point to a DataFrame
    df_single = pd.DataFrame([data])

    # Replicate feature engineering steps
    df_single['Payement_Value'] = df_single['PAY_SEPT'].astype(int) + df_single['PAY_AUG'].astype(int) + df_single['PAY_JUL'].astype(int) + df_single['PAY_JUN'].astype(int) + df_single['PAY_MAY'].astype(int) + df_single['PAY_APR'].astype(int)
    df_single['Dues'] = (df_single['BILL_AMT_APR'].astype(float)+df_single['BILL_AMT_MAY'].astype(float)+df_single['BILL_AMT_JUN'].astype(float)+df_single['BILL_AMT_JUL'].astype(float)+df_single['BILL_AMT_SEPT'].astype(float))-(df_single['PAY_AMT_APR'].astype(float)+df_single['PAY_AMT_MAY'].astype(float)+df_single['PAY_AMT_JUN'].astype(float)+df_single['PAY_AMT_JUL'].astype(float)+df_single['PAY_AMT_AUG'].astype(float)+df_single['PAY_AMT_SEPT'].astype(float))

    # Handle rare categories in EDUCATION and MARRIAGE
    df_single['EDUCATION'] = np.where(df_single['EDUCATION'].astype(int) == 5, 4, df_single['EDUCATION'].astype(int))
    df_single['EDUCATION'] = np.where(df_single['EDUCATION'].astype(int) == 6, 4, df_single['EDUCATION'].astype(int))
    df_single['EDUCATION'] = np.where(df_single['EDUCATION'].astype(int) == 0, 4, df_single['EDUCATION'].astype(int))
    df_single['MARRIAGE'] = np.where(df_single['MARRIAGE'].astype(int) == 0, 3, df_single['MARRIAGE'].astype(int))

    # One Hot Encoding for EDUCATION and MARRIAGE
    df_single = pd.get_dummies(df_single, columns=['EDUCATION', 'MARRIAGE'], drop_first=False)

    # One Hot Encoding for PAY_SEPT to PAY_APR
    pay_columns = ['PAY_SEPT', 'PAY_AUG', 'PAY_JUL', 'PAY_JUN', 'PAY_MAY', 'PAY_APR']
    df_single = pd.get_dummies(df_single, columns=pay_columns, drop_first=True)

    # Label Encoding for SEX
    sex_mapping = {"FEMALE": 0, "MALE": 1}
    df_single['SEX'] = df_single['SEX'].astype(int).replace(sex_mapping)

    # Drop the original ID column if it exists
    if 'ID' in df_single.columns:
        df_single.drop('ID', axis=1, inplace=True)

    # Expected columns from training
    expected_columns = ['LIMIT_BAL', 'SEX', 'AGE', 'BILL_AMT_SEPT', 'BILL_AMT_AUG', 'BILL_AMT_JUL', 'BILL_AMT_JUN', 'BILL_AMT_MAY', 'BILL_AMT_APR', 'PAY_AMT_SEPT', 'PAY_AMT_AUG', 'PAY_AMT_JUL', 'PAY_AMT_JUN', 'PAY_AMT_MAY', 'PAY_AMT_APR', 'EDUCATION_1', 'EDUCATION_2', 'EDUCATION_3', 'EDUCATION_4', 'MARRIAGE_1', 'MARRIAGE_2', 'MARRIAGE_3', 'PAY_SEPT_-1', 'PAY_SEPT_0', 'PAY_SEPT_1', 'PAY_SEPT_2', 'PAY_SEPT_3', 'PAY_SEPT_4', 'PAY_SEPT_5', 'PAY_SEPT_6', 'PAY_SEPT_7', 'PAY_SEPT_8', 'PAY_AUG_-1', 'PAY_AUG_0', 'PAY_AUG_1', 'PAY_AUG_2', 'PAY_AUG_3', 'PAY_AUG_4', 'PAY_AUG_5', 'PAY_AUG_6', 'PAY_AUG_7', 'PAY_AUG_8', 'PAY_JUL_-1', 'PAY_JUL_0', 'PAY_JUL_1', 'PAY_JUL_2', 'PAY_JUL_3', 'PAY_JUL_4', 'PAY_JUL_5', 'PAY_JUL_6', 'PAY_JUL_7', 'PAY_JUL_8', 'PAY_JUN_-1', 'PAY_JUN_0', 'PAY_JUN_1', 'PAY_JUN_2', 'PAY_JUN_3', 'PAY_JUN_4', 'PAY_JUN_5', 'PAY_JUN_6', 'PAY_JUN_7', 'PAY_JUN_8', 'PAY_MAY_-1', 'PAY_MAY_0', 'PAY_MAY_1', 'PAY_MAY_2', 'PAY_MAY_3', 'PAY_MAY_4', 'PAY_MAY_5', 'PAY_MAY_6', 'PAY_MAY_7', 'PAY_MAY_8', 'PAY_APR_-1', 'PAY_APR_0', 'PAY_APR_1', 'PAY_APR_2', 'PAY_APR_3', 'PAY_APR_4', 'PAY_APR_5', 'PAY_APR_6', 'PAY_APR_7', 'PAY_APR_8']

    for col in expected_columns:
        if col not in df_single.columns:
            df_single[col] = 0

    # Reindex the DataFrame to match the order of columns in the training data
    df_single = df_single[expected_columns]

    return df_single

app = Flask(__name__)

@app.route('/')
def home():
    """Home page route"""
    return render_template('home.html')

@app.route('/assess')
def assess():
    """Assessment form page route"""
    return render_template('input.html')

@app.route('/predict', methods=['POST'])
def predict():
    """Prediction route - processes form data and returns results"""
    try:
        # Retrieve form data
        form_data = request.form

        # Convert form data to dictionary and ensure correct types
        input_data = {key: float(value) if '.' in value else int(value) for key, value in form_data.items()}

        # Preprocess the input data
        processed_input = preprocess_input(input_data)

        # Make prediction
        prediction = loaded_model.predict(processed_input)[0]

        # Determine the prediction result message
        result_message = "will NOT default on their credit card." if prediction == 0 else "will default on their credit card."

        # Render the result template
        return render_template('result.html', prediction_text=f'The customer {result_message}')

    except Exception as e:
        return render_template('result.html', prediction_text=f'Error processing request: {str(e)}')

@app.route('/about')
def about():
    """About page route"""
    return render_template('about.html')

@app.errorhandler(404)
def page_not_found(e):
    """Handle 404 errors"""
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(e):
    """Handle 500 errors"""
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)