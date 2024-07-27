import gradio as gr
import mlflow.pyfunc
import pandas as pd

# MLflow modeli yükleme
model = mlflow.pyfunc.load_model("models:/final_rf_model/1")

# Tahmin fonksiyonu
def predict_heart_disease(age, sex, chest_pain_type, resting_blood_pressure, serum_cholestoral, fasting_blood_sugar, resting_ecg_results, max_heart_rate_achieved, exercise_induced_angina, oldpeak, slope_peak_exercise_st_segment, number_major_vessels, thal):
    input_data = pd.DataFrame({
        "age": [age],
        "sex": [sex],
        "chest_pain_type": [chest_pain_type],
        "resting_blood_pressure": [resting_blood_pressure],
        "serum_cholestoral": [serum_cholestoral],
        "fasting_blood_sugar": [fasting_blood_sugar],
        "resting_ecg_results": [resting_ecg_results],
        "max_heart_rate_achieved": [max_heart_rate_achieved],
        "exercise_induced_angina": [exercise_induced_angina],
        "oldpeak": [oldpeak],
        "slope_peak_exercise_st_segment": [slope_peak_exercise_st_segment],
        "number_major_vessels": [number_major_vessels],
        "thal": [thal]
    })

    prediction = model.predict(input_data)
    result = int(prediction[0])
    
    if result == 1:
        return "Kalp hastalığı riskiniz vardır, en kısa zamanda randevu alın", "red"
    else:
        return "Kalbinize iyi bakmışsınız tebrikler :)", "green"

# Gradio arayüzü
inputs = [
    gr.Number(label="Age"),
    gr.Dropdown(choices=[1, 0], label="Sex"),
    gr.Dropdown(choices=["cp_typical_angina", "cp_atypical_angina", "cp_non_anginal_pain", "cp_asymptomatic"], label="Chest Pain Type"),
    gr.Number(label="Resting Blood Pressure"),
    gr.Number(label="Serum Cholestoral"),
    gr.Dropdown(choices=[1, 0], label="Fasting Blood Sugar"),
    gr.Dropdown(choices=["ecg_normal", "ecg_st_t_wave_abnorm", "ecg_left_vent_hyper"], label="Resting ECG Results"),
    gr.Number(label="Max Heart Rate Achieved"),
    gr.Dropdown(choices=[1, 0], label="Exercise Induced Angina"),
    gr.Number(label="Oldpeak"),
    gr.Dropdown(choices=["slope_upsloping", "slope_flat", "slope_downsloping"], label="Slope Peak Exercise ST Segment"),
    gr.Dropdown(choices=[0, 1, 2, 3], label="Number Major Vessels"),
    gr.Dropdown(choices=["normal", "fixed_defect", "reversable_defect"], label="Thal")
]

outputs = gr.Textbox(label="Presence of Heart Disease")

def gradio_interface():
    gr.Interface(
        fn=predict_heart_disease, 
        inputs=inputs, 
        outputs=outputs,
        title="Heart Disease Prediction",
        description="Kalp hastalığı riski tahmin uygulaması"
    ).launch()


if __name__ == "__main__":
    gradio_interface()
