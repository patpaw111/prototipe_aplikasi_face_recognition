# from fastapi import FastAPI, HTTPException
# from pydantic import BaseModel
# from typing import List
# import os
# import cv2
# import numpy as np
# import base64
# from pathlib import Path
# import random
# from fastapi.middleware.cors import CORSMiddleware

# app = FastAPI()

# # CORS middleware untuk frontend yang berjalan di domain atau port yang berbeda
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # Bisa disesuaikan dengan URL frontend yang spesifik
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # Model data yang diterima dari frontend
# class OrderRequest(BaseModel):
#     menu: List[str]
#     photos: List[str]  # Base64-encoded photos

# # Model data yang dikirimkan ke frontend
# class OrderResponse(BaseModel):
#     menu: List[str]
#     expression: str
#     status: str

# # Fungsi untuk menyimpan foto ke folder pelanggan
# def save_photos(photos: List[str], folder_name: str):
#     save_path = Path(f"./orders/{folder_name}")
#     save_path.mkdir(parents=True, exist_ok=True)
#     for i, photo in enumerate(photos):
#         try:
#             decoded_data = base64.b64decode(photo.split(",")[1])
#             np_data = np.frombuffer(decoded_data, np.uint8)
#             img = cv2.imdecode(np_data, cv2.IMREAD_COLOR)
#             if img is not None:
#                 cv2.imwrite(str(save_path / f"photo_{i+1}.jpg"), img)
#             else:
#                 raise ValueError("Failed to decode image")
#         except Exception as e:
#             raise HTTPException(
#                 status_code=400,
#                 detail=f"Error processing photo {i+1}: {str(e)}"
#             )

# # Fungsi untuk menganalisis ekspresi wajah (simulasi)
# def analyze_photos(folder_name: str) -> str:
#     expressions = ["Happy", "Neutral", "Unhappy"]
#     # Placeholder logic: Randomly choose an expression
#     return random.choice(expressions)

# @app.post("/order", response_model=OrderResponse)
# async def process_order(order: OrderRequest):
#     if not order.menu or not order.photos:
#         raise HTTPException(status_code=400, detail="Menu or photos cannot be empty.")
#     if len(order.photos) != 20:
#         raise HTTPException(status_code=400, detail="Exactly 20 photos are required.")

#     # Buat folder untuk pelanggan baru
#     customer_id = f"pelanggan{len(os.listdir('./orders')) + 1}"
#     save_photos(order.photos, customer_id)

#     # Analisis ekspresi wajah
#     expression = analyze_photos(customer_id)

#     # Kirimkan respons
#     return OrderResponse(
#         menu=order.menu,
#         expression=expression,
#         status="Success"
#     )

# # Menambahkan pengecekan untuk memastikan folder 'orders' ada
# if not os.path.exists('./orders'):
#     os.makedirs('./orders')

# # ^refaktor code di atas ^

# # uvicorn main:app --reload

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import os
import cv2
import numpy as np
import base64
from pathlib import Path
import random
from fastapi.middleware.cors import CORSMiddleware
from collections import Counter

app = FastAPI()

# CORS middleware untuk frontend yang berjalan di domain atau port yang berbeda
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Bisa disesuaikan dengan URL frontend yang spesifik
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Model data yang diterima dari frontend
class OrderRequest(BaseModel):
    menu: List[str]
    photos: List[str]  # Base64-encoded photos

# Model data yang dikirimkan ke frontend
class OrderResponse(BaseModel):
    menu: List[str]
    expression: str
    status: str

# Fungsi untuk menyimpan foto ke folder pelanggan
def save_photos(photos: List[str], folder_name: str):
    save_path = Path(f"./orders/{folder_name}")
    save_path.mkdir(parents=True, exist_ok=True)
    for i, photo in enumerate(photos):
        try:
            decoded_data = base64.b64decode(photo.split(",")[1])
            np_data = np.frombuffer(decoded_data, np.uint8)
            img = cv2.imdecode(np_data, cv2.IMREAD_COLOR)
            if img is not None:
                cv2.imwrite(str(save_path / f"photo_{i+1}.jpg"), img)
            else:
                raise ValueError("Failed to decode image")
        except Exception as e:
            raise HTTPException(
                status_code=400,
                detail=f"Error processing photo {i+1}: {str(e)}"
            )

# Fungsi untuk menganalisis ekspresi wajah menggunakan OpenCV
def analyze_photos(folder_name: str) -> str:
    expressions = ["Happy", "Neutral", "Unhappy"]
    
    # Memuat classifier Haar Cascade untuk deteksi wajah
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    expression_results = []

    for i in range(1, 21):  # Iterasi untuk 20 foto
        image_path = Path(f"./orders/{folder_name}/photo_{i}.jpg")
        if not image_path.exists():
            raise HTTPException(status_code=400, detail=f"Photo_{i} not found for analysis.")
        
        img = cv2.imread(str(image_path))
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Deteksi wajah
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        # Jika wajah terdeteksi, pilih ekspresi secara acak (simulasi)
        if len(faces) > 0:
            expression_results.append(random.choice(expressions))
        else:
            expression_results.append("No face detected")

    # Menghitung ekspresi yang paling sering muncul
    most_common_expression = Counter(expression_results).most_common(1)[0][0]
    return most_common_expression

@app.post("/order", response_model=OrderResponse)
async def process_order(order: OrderRequest):
    if not order.menu or not order.photos:
        raise HTTPException(status_code=400, detail="Menu or photos cannot be empty.")
    if len(order.photos) != 20:
        raise HTTPException(status_code=400, detail="Exactly 20 photos are required.")

    # Buat folder untuk pelanggan baru
    customer_id = f"pelanggan{len(os.listdir('./orders')) + 1}"
    save_photos(order.photos, customer_id)

    # Analisis ekspresi wajah menggunakan OpenCV untuk semua foto
    expression = analyze_photos(customer_id)

    # Kirimkan respons
    return OrderResponse(
        menu=order.menu,
        expression=expression,
        status="Success"
    )

# Menambahkan pengecekan untuk memastikan folder 'orders' ada
if not os.path.exists('./orders'):
    os.makedirs('./orders')

# from fastapi import FastAPI, HTTPException
# from pydantic import BaseModel
# from typing import List
# import os
# import cv2
# import numpy as np
# import base64
# from pathlib import Path
# from fer import FER  # Menggunakan pustaka FER untuk deteksi ekspresi wajah
# from collections import Counter
# from fastapi.middleware.cors import CORSMiddleware

# app = FastAPI()

# # CORS middleware untuk frontend yang berjalan di domain atau port yang berbeda
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # Bisa disesuaikan dengan URL frontend yang spesifik
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # Model data yang diterima dari frontend
# class OrderRequest(BaseModel):
#     menu: List[str]
#     photos: List[str]  # Base64-encoded photos

# # Model data yang dikirimkan ke frontend
# class OrderResponse(BaseModel):
#     menu: List[str]
#     expression: str
#     status: str

# # Fungsi untuk menyimpan foto ke folder pelanggan
# def save_photos(photos: List[str], folder_name: str):
#     save_path = Path(f"./orders/{folder_name}")
#     save_path.mkdir(parents=True, exist_ok=True)
#     for i, photo in enumerate(photos):
#         try:
#             decoded_data = base64.b64decode(photo.split(",")[1])
#             np_data = np.frombuffer(decoded_data, np.uint8)
#             img = cv2.imdecode(np_data, cv2.IMREAD_COLOR)
#             if img is not None:
#                 cv2.imwrite(str(save_path / f"photo_{i+1}.jpg"), img)
#             else:
#                 raise ValueError("Failed to decode image")
#         except Exception as e:
#             raise HTTPException(
#                 status_code=400,
#                 detail=f"Error processing photo {i+1}: {str(e)}"
#             )

# # Fungsi untuk menganalisis ekspresi wajah menggunakan pustaka FER
# def analyze_photos(folder_name: str) -> str:
#     # Menggunakan model FER untuk deteksi ekspresi wajah
#     detector = FER()

#     expression_results = []

#     for i in range(1, 21):  # Iterasi untuk 20 foto
#         image_path = Path(f"./orders/{folder_name}/photo_{i}.jpg")
#         if not image_path.exists():
#             raise HTTPException(status_code=400, detail=f"Photo_{i} not found for analysis.")
        
#         img = cv2.imread(str(image_path))

#         # Analisis ekspresi wajah menggunakan FER
#         emotion, score = detector.top_emotion(img)
#         expression_results.append(emotion)  # Menyimpan ekspresi yang terdeteksi

#     # Menghitung ekspresi yang paling sering muncul
#     most_common_expression = Counter(expression_results).most_common(1)[0][0]
#     return most_common_expression

# @app.post("/order", response_model=OrderResponse)
# async def process_order(order: OrderRequest):
#     if not order.menu or not order.photos:
#         raise HTTPException(status_code=400, detail="Menu or photos cannot be empty.")
#     if len(order.photos) != 20:
#         raise HTTPException(status_code=400, detail="Exactly 20 photos are required.")

#     # Buat folder untuk pelanggan baru
#     customer_id = f"pelanggan{len(os.listdir('./orders')) + 1}"
#     save_photos(order.photos, customer_id)

#     # Analisis ekspresi wajah menggunakan FER untuk semua foto
#     expression = analyze_photos(customer_id)

#     # Kirimkan respons
#     return OrderResponse(
#         menu=order.menu,
#         expression=expression,
#         status="Success"
#     )

# # Menambahkan pengecekan untuk memastikan folder 'orders' ada
# if not os.path.exists('./orders'):
#     os.makedirs('./orders')
