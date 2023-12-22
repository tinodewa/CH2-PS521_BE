import json

class ReppoFood:
   def __init__(self, saved_model_path):
      self.saved_model_path = saved_model_path
# Membaca file JSON
   def read_json_file(file_path):
      """
      Fungsi ini membaca file JSON dan mengembalikan isi file dalam bentuk dictionary.

      Parameters:
      - file_path (str): Path menuju file JSON.

      Returns:
      - dict: Dictionary berisi data dari file JSON.
      """
      with open(file_path, 'r') as json_file:
         data = json.load(json_file)
      return data
   


