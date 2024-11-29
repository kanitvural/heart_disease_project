import gradio as gr
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
import pandas as pd
import mlflow.sklearn


app = FastAPI()

model_path = "models:/final_rf_model/1" 
model = mlflow.sklearn.load_model(model_path)

class HeartDiseaseInput(BaseModel):
    age: int
    sex: bool
    chest_pain_type: str
    resting_blood_pressure: int
    serum_cholesterol: int
    fasting_blood_sugar: bool
    resting_ecg_results: str
    maximum_heart_rate_achieved: int
    exercise_induced_angina: bool
    st_depression_induced_by_exercise: float
    slope_peak_exercise_st_segment: str
    number_major_vessels: int
    thal: str

def predict(input_data: HeartDiseaseInput):
    input_df = pd.DataFrame([input_data.model_dump()])
    
    prediction = model.predict(input_df)
    
    if prediction[0] == 0:
        return "<div style='color: green; font-size: 20px; font-weight: bold;'>You've taken great care of your heart, congratulations! 💖😊</div>"
    else:
        return "<div style='color: red; font-size: 20px; font-weight: bold;'>You are at risk of heart disease, please schedule an appointment as soon as possible! ⚠️❤️‍🩹</div>"


@app.post("/predict")
async def predict_endpoint(input_data: HeartDiseaseInput):
    return predict(input_data)

# Gradio interface
def gradio_predict(age, sex, chest_pain_type, resting_blood_pressure, serum_cholesterol, fasting_blood_sugar, resting_ecg_results, maximum_heart_rate_achieved, exercise_induced_angina, st_depression_induced_by_exercise, slope_peak_exercise_st_segment, number_major_vessels, thal):
    input_data = HeartDiseaseInput(
        age=age,
        sex=sex,
        chest_pain_type=chest_pain_type,
        resting_blood_pressure=resting_blood_pressure,
        serum_cholesterol=serum_cholesterol,
        fasting_blood_sugar=fasting_blood_sugar,
        resting_ecg_results=resting_ecg_results,
        maximum_heart_rate_achieved=maximum_heart_rate_achieved,
        exercise_induced_angina=exercise_induced_angina,
        st_depression_induced_by_exercise=st_depression_induced_by_exercise,
        slope_peak_exercise_st_segment=slope_peak_exercise_st_segment,
        number_major_vessels=number_major_vessels,
        thal=thal
    )
    return predict(input_data)

gradio_interface = gr.Interface(
    fn=gradio_predict,
    inputs=[
        gr.Slider(minimum=0, maximum=100, value=50, label="Age"),
        gr.Dropdown(choices=[0, 1], value=0, label="Sex", info="0 = Female, 1 = Male", type="index"),
        gr.Dropdown(choices=["cp_typical_angina", "cp_atypical_angina", "cp_non_anginal_pain", "cp_asymptomatic"], value="cp_typical_angina", label="Chest Pain Type"),
        gr.Slider(minimum=90, maximum=200, value=120, label="Resting Blood Pressure"),
        gr.Slider(minimum=120, maximum=600, value=200, label="Serum Cholesterol"),
        gr.Dropdown(choices=[0, 1], value=0, label="Fasting Blood Sugar"),
        gr.Dropdown(choices=["ecg_normal", "ecg_st_t_wave_abnormality", "ecg_left_ventricular_hypertrophy"], value="ecg_normal", label="Resting ECG Results"),
        gr.Slider(minimum=70, maximum=210, value=150, label="Maximum Heart Rate Achieved"),
        gr.Dropdown(choices=[0, 1], value=0, label="Exercise Induced Angina"),
        gr.Slider(minimum=0, maximum=7, value=1.0,label="ST Depression Induced by Exercise"),
        gr.Dropdown(choices=["slope_upsloping", "slope_flat", "slope_downsloping"], value="slope_upsloping", label="Slope Peak Exercise ST Segment"),
        gr.Slider(minimum=0, maximum=3, step=1, value=0, label="Number of Major Vessels"),
        gr.Dropdown(choices=["thal_normal", "thal_fixed_defect","thal_reversable_defect"], value="thal_normal", label="Thal")
    ],
    outputs=gr.HTML(),
    title="Heart Disease Risk Prediction"
)

gradio_interface.launch(share=True)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
