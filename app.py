from flask import Flask, request, render_template
import pandas as pd
import joblib

app = Flask(__name__)

# Load trained model
model = joblib.load("heart_attack_model.pkl")

@app.route("/")
def home():
    return render_template("heartattack.html")  # Load frontend page
    

@app.route("/predict", methods=["POST"])
def predict():
    try:
        # Get user inputs
        user_input = [
            float(request.form["age"]),
            int(request.form["sex"]),
            int(request.form["cp"]),
            float(request.form["trestbps"]),
            float(request.form["chol"]),
            int(request.form.get("fbs", 0)),  # Checkbox
            int(request.form["restecg"]),
            float(request.form["thalach"]),
            int(request.form["exang"]),
            float(request.form["oldpeak"]),
            int(request.form["slope"]),
            int(request.form["ca"]),
            int(request.form["thal"])
        ]

        # Convert input into DataFrame
        input_df = pd.DataFrame([user_input], columns=[
            "age", "sex", "cp", "trestbps", "chol", "fbs", "restecg",
            "thalach", "exang", "oldpeak", "slope", "ca", "thal"
        ])

        # Make prediction
        prediction = model.predict(input_df)[0]
        result = "High Risk of Heart Attack" if prediction == 1 else "Low Risk of Heart Attack"

        return render_template("heartattack.html", prediction_text=result)
      # Map prediction to readable text
        labels = ["No Heart Attack", "Heart Attack"]
        result = labels[int(prediction[0])]
        confidence = f"{probabilities[0][1] * 100:.2f}%"  # Confidence percentage

        return render_template("home3.html.html", prediction=result, confidence=confidence)


    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    app.run(debug=True)
