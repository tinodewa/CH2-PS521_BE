
import json
from fastapi import FastAPI, HTTPException, UploadFile
from pydantic import BaseModel
app = FastAPI()
from reppo.reppo_food import ReppoFood
from models.LoadModel import PredictedImg
from fastapi.responses import JSONResponse
# Import kelas PredictedImg dari file yang mengandung kelas tersebut


# # Contoh penggunaan
# model_path = 'models/allergen_food_model_v2'
# image_path = 'models/data/test/pecel/905.jpg'

# # Membuat objek PredictedImg
# predicted_img = PredictedImg(model_path)

# # Melakukan prediksi pada gambar tertentu
# predicted_class, predicted_probability = predicted_img.predict(image_path)

# # Menampilkan hasil prediksi
# print('Predicted class:', predicted_class)
# print('Predicted probability:', predicted_probability)


# # kode saya

# # Mendefinisikan path untuk menyimpan file JSON
# output_file_path = 'output_predictions.json'

# # Membuat dictionary dengan nilai-nilai yang ingin disimpan
# output_data = {
#    'predicted_class': int(predicted_class),
#    'predicted_food': food[int(predicted_class)],
#    'predicted_probability': float(predicted_probability)
# }

# # Menyimpan dictionary ke dalam file JSON
# with open(output_file_path, 'w') as json_file:
#    json.dump(output_data, json_file)

# GET
@app.get("/")
def root():
   return "Hello Home"
@app.get("/results")
def result():
   loaded_data = ReppoFood.read_json_file('models/output_predictions.json')   
   return loaded_data

# POST
class Item(BaseModel):
    image_path: str='img/'

@app.post("/export")
async def export_image(file: UploadFile):
   file_content = await file.read()

      # Tentukan path penyimpanan file
   save_path = f"img/{file.filename}"

      # Tulis data blob ke file
   with open(save_path, "wb") as f:
         f.write(file_content)
   model_path = 'models/allergen_food_model_v2'
   
   image_path = f'img/{file.filename}'  # Mengambil path gambar dari input
   
   try:
      predicted_img = PredictedImg(model_path)
      predicted_class,predicted_probability = predicted_img.predict(image_path)
   except Exception as e:
      raise HTTPException(status_code=500, detail=f"Error in prediction: {str(e)}")
   food = [
      'cumi asam manis',
      'gado gado',
      'martabak asin',
      'pecel',
      'tahu susu',
   ]
   predict_classTofloat = predicted_class
   predict_food = food[int(predict_classTofloat)]
   predict_probability = float(predicted_probability)
   desc = f'makanan {predict_food} memiliki {predict_probability * 100}% menyebabkan alergi'
   # # Mendefinisikan path untuk menyimpan file JSON
   # output_file_path = 'output_predictions.json'
   # # Membuat dictionary dengan nilai-nilai yang ingin disimpan
   # output_data = {
   #    'predicted_class':predict_classTofloat,
   #    'predicted_food': predict_food,
   #    'predicted_probability': predict_classTofloat
   # }

   # # Menyimpan dictionary ke dalam file JSON
   # with open(output_file_path, 'w') as json_file:
   #    json.dump(output_data, json_file)
   # # desc masih perlu diperbaiki karena tidak sesuai belum menggunakan nilai probadibility 
   result = {"describe": desc,"Predict_Food": predict_food,"Predict Probability": predict_probability}

   return JSONResponse(content=result)
   
