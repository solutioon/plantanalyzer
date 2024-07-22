from fastapi import FastAPI, File, UploadFile
import uvicorn
import json
import time
from fastapi.middleware.cors import CORSMiddleware
import google.generativeai as genai
import os

# Configuracion
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
generation_config = {
    "max_output_tokens": 2048,
    "temperature": 0,
    "top_p": 1,
    "response_mime_type": "application/json"
}

# inicializar modelo
model = genai.GenerativeModel("gemini-1.5-flash", generation_config=generation_config)

def get_gemini_response(prompt, image_data):
    prompt_parts = [
        prompt,
        image_data
    ]
    response = model.generate_content(prompt_parts)
    return response.text

async def input_image_details(uploaded_file):
    if uploaded_file is not None:
        bytes_data = await uploaded_file.read()
        return {
            "mime_type": uploaded_file.content_type,
            "data": bytes_data
        }
    else:
        raise FileNotFoundError("No has subido una imagen")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/planta")
async def analyze_receipt(
    image: UploadFile = File(...)
):
    """
    API endpoint to receive image file, and return the analyzed JSON response.
    """
    try:
        print("procesando la imagen")
        inicio = time.time()
        
        # Esperar el resultado de input_image_details
        imagen_data = await input_image_details(image)
        
        prompt = """
        You will be given a photo to analyze. Your task is to determine if the photo contains a plant and provide structured information about it. Follow these instructions:

        First, assess if the image contains a plant.
        If the image does not contain a plant, respond with only this message:
        "The photo does not correspond to a plant."
        If the image does contain a plant, provide the following structured data:
        {
        "name": "Common name of the plant",
        "scientificName": "Scientific (Latin) name of the plant",
        "description": "A brief description of the plant's appearance and characteristics",
        "status": "The current status of the plant in the photo (e.g., healthy, wilting, flowering)",
        "care": [
            "List of care instructions for the plant",
            "Each item should be a separate care tip",
            "Include watering, sunlight, soil, and temperature requirements if applicable"
        ]
        }

        Ensure all fields are filled with accurate information based on the plant in the photo.
        If you're uncertain about any specific detail, use "Unknown" for that field rather than guessing.
        Provide only the JSON response for plant images, with no additional text before or after.

        Remember to analyze the image carefully and provide the most accurate information possible based on what you can see in the photo.
        """
        response = get_gemini_response(prompt, imagen_data)
        print("La respuesta es:")
        print(response)
        final = time.time()
        print("Tiempo total de ejecución: ", final - inicio)
        # Intenta parsear la respuesta como JSON
        try:
            json_response = json.loads(response)
            return {"response": json_response}
        except json.JSONDecodeError:
            # Si no es JSON, devuelve la respuesta como texto
            return {"response": response}
    except FileNotFoundError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)