from fastapi import FastAPI
from fastapi import FastAPI, Query
from app.stream import streaming_camera
from utils.time_stamp import get_time_stamp
from db.controller_db import update_db,delete_db,load_db
from fastapi import FastAPI, UploadFile
import cv2
import numpy as np
from utils.detect import load_model, get_label

app = FastAPI()
FM,session = load_model()

def process_request(request):
    nparr = np.frombuffer(request, np.uint8)
    return cv2.imdecode(nparr, cv2.IMREAD_COLOR)

@app.get("/")
async def root():
    return 'Hello'

@app.get("/get_time_stamp")
async def time_stamp(video_path: str = Query(...)): 
    delete_db()
    streaming_camera(video_path)
    #Load labels from database
    chain_labels = load_db()  
    # Get time stamp
    time_stamp = get_time_stamp(chain_labels)
    
    return time_stamp

@app.post("/classify")
async def classify(anchor: UploadFile,predict: UploadFile):
    anchor = process_request(await anchor.read())
    predict =process_request(await predict.read())
    label = get_label(FM, session, anchor, predict)
    return str(label)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)