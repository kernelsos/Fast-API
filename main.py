from fastapi import FastAPI, Path, HTTPException , Query
import json

app = FastAPI()

def load_data():
    with open("patients.json","r") as f:
        data = json.load(f)
    return data 



@app.get("/")
def hello():
    return {'message':'Patient management system API'}

@app.get("/about")
def about():
    return {'message':"A fully functional API to manage patient records"}

@app.get("/view")
def view_data():
    data = load_data()
    return data 

@app.get('/patient/{patient_id}')
def view_patient(patient_id: str = Path(...,description="ID of the patient in the DB", example="p001")):
    data = load_data()
    if patient_id in  data:
        return data[patient_id]
    raise HTTPException(status_code=404, detail = "Patient record not found")

@app.get("/sort")
def sort_patient(sortby: str = Query(..., description="Provide a valid field like height, weight or BMI"), order : str = Query(description="Sort in asc or desc prder")):

    valid_fields = ["height","weight","BMI"]
    if sortby not in valid_fields:
        raise HTTPException(status_code=400, detail=f'Invalid field, Please select from {valid_filed}')
    
    if order not in ["asc","desc"]:
        raise HTTPException(status_code=400, detail=f'select from asc or desc')

    data = load_data()
    sort_order = True if order=="desc" else False
    sorted_data = sorted(data.values(),key = lambda x: x.get(sortby,0),reverse=sort_order)
    return sorted_data
