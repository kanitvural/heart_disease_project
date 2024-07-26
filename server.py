from fastapi import FastAPI
import uvicorn
from gradio import Interface

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Heart Disease Prediction API"}

# Gradio arayüzünü FastAPI ile entegre et
gradio_interface = Interface(
    fn=predict_heart_disease, 
    inputs=inputs, 
    outputs=outputs,
    title="Heart Disease Prediction",
    description="Kalp hastalığı riski tahmin uygulaması"
)

@app.get("/heart_disease")
def get_gradio_interface():
    gradio_interface.launch(server_name="0.0.0.0", server_port=7860, share=True, inline=False)
    return {"message": "Gradio interface launched"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
