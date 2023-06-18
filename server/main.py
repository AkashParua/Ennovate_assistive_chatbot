from query import query
from fastapi import FastAPI, UploadFile
from io import BytesIO
from pydantic import BaseModel
import json
from PIL import Image ,ImageDraw
from ultralytics import YOLO

import http.client
model = YOLO("yolov8n.pt")
conn = http.client.HTTPSConnection("chatgpt-gpt-3-5.p.rapidapi.com")
app = FastAPI()

headers = {
    'content-type': "application/json",
    'X-RapidAPI-Key': "2cc2e51559msh8bb526082cca664p1ff7cejsn0005b8d416ef",
    'X-RapidAPI-Host': "chatgpt-gpt-3-5.p.rapidapi.com"
}


class QueryRequest(BaseModel):
    user_input: str

class QueryResponse(BaseModel):
    bot_response: str
    manual_text: str

@app.post("/query-request", response_model=QueryResponse)
def query_request(request: QueryRequest):
    
    docs = query(question=request.user_input , n=2)
    llm_query = f'given the following context : {" ".join(docs)} answer the question : {request.user_input}'

    payload = json.dumps({"query" : llm_query})
    conn.request("POST", "/ask", payload, headers)

    res = conn.getresponse()
    
    data = res.read().decode('utf-8')
    dic = json.loads(data)
 
    return QueryResponse(bot_response=dic['response'] ,  manual_text= " ".join(docs))


@app.post("/upload-image")
async def upload_image( target : str,image: UploadFile = UploadFile(...) ):
    # Read the image file contents
    image_bytes = await image.read()
    # Load the image bytes into a PIL Image object
    pil_image = Image.open(BytesIO(image_bytes))
    results = model.predict(source=pil_image)
   
    res = {}
    for result in results:
        bbox = result.boxes.xywh.tolist()
        classid = result.boxes.cls.tolist()
        conf = result.boxes.conf.tolist()
        nm = result.names
        for i , box in enumerate(bbox):
            box.insert(0,nm[classid[i]])
        res['response'] = bbox
    
    #checking whether the image is reaching the edges 
    count = 0
    adjust = "OK"
    draw = ImageDraw.Draw(pil_image)
    for bounding_box in res['response'] :
        if bounding_box[0] == target :
            #print(bounding_box[0])
            count += 1
            norm_xmid = bounding_box[1]/pil_image.size[0]
            norm_ymid = bounding_box[2]/pil_image.size[1]
            xmid = bounding_box[1]
            ymid = bounding_box[2]
            w =  bounding_box[3]
            h =  bounding_box[4]
            xmin = xmid - w/2
            ymin = ymid - h/2
            xmax = xmid + w/2
            ymax = ymid + h/2
            if norm_xmid < 0.1 :
                adjust = "move the object to the right"
            if norm_xmid > 0.9 :
                adjust = "move the object to the left"
            if norm_ymid < 0.1 :
                adjust = "the object is too high"
            if norm_ymid > 0.9 :
                adjust = "the object is too low"   
            draw.rectangle([(xmin, ymin), (xmax, ymax)], outline=(0, 255, 0), width=5)
    
    #pil_image.show()
    if count != 1:
        adjust = "Make sure only one object of interest is in frame"
    #print(count)
    res["adjust"] = adjust
    #adding bounding box to the image   
    return res





    

    