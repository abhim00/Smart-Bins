import pandas as pd
from fastai.vision.learner import load_learner
from fastai.vision.image import open_image
from PIL import Image
import sys
from io import BytesIO
import json

def predict(filepath, company, bin):
    img = Image.open(filepath).resize((512,384), Image.ANTIALIAS)
    img.save(filepath)

    learn = load_learner("./ml-model/")

    category = str(learn.predict(open_image(filepath))[0])
    tensor_probs = learn.predict(open_image(filepath))[2]
    pred_probs = {
    "cardboard": round(float(tensor_probs[0]),2),
    "glass": round(float(tensor_probs[1]),2),
    "metal": round(float(tensor_probs[2]),2),
    "paper": round(float(tensor_probs[3]),2),
    "plastic": round(float(tensor_probs[4]),2),
    "trash": round(float(tensor_probs[5]),2)
    }
    ans = {
    "category": category,
    "pred_probs": pred_probs
    }
    

    with open("../" + company + '.json') as f:
        data = json.load(f)
    data[bin]["articles"].append(ans["category"])
    data[bin]["scanned_items"]+=1
    with open("../" + company + '.json', 'w') as json_file:
        #print(data["bin1"])
    	json.dump(data, json_file)

    return ans
