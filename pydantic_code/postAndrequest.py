from fastapi import FastAPI, Path, HTTPException, Query
from fastapi.responses import JSONResponse
import json
from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Literal

app = FastAPI()

# ------------------------------
# Patient Model
# ------------------------------
class Patient(BaseModel):
    id: Annotated[str, Field(..., description="ID of the patient", examples=["P001"])]
    name: Annotated[str, Field(..., description="Name of the patient")]
    city: Annotated[str, Field(..., description="City of residence")]
    age: Annotated[int, Field(..., gt=0, lt=120, description="Age of the patient")]
    gender: Annotated[Literal['male', 'female', 'others'], Field(..., description="Gender of the patient")]
    height: Annotated[float, Field(..., gt=0, description="Height of the patient in meters")]
    weight: Annotated[float, Field(..., gt=0, description="Weight of the patient in kilograms")]

    # Computed BMI
    @computed_field
    @property
    def bmi(self) -> float:
        bmi = round(self.weight / (self.height ** 2), 2)
        return bmi

    # Computed verdict
    @computed_field
    @property
    def verdict(self) -> str:
        if self.bmi < 18.5:
            return "Underweight"
        elif self.bmi < 25:
            return "Normal"
        elif self.bmi < 30:
            return "Overweight"
        else:
            return "Obese"


# ------------------------------
# Utility functions
# ------------------------------
def load_data():
    try:
        with open("patients.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}  # return empty dict if file not found


def save_data(data):
    with open("patients.json", "w") as f:
        json.dump(data, f, indent=4)


# ------------------------------
# API Routes
# ------------------------------
@app.get("/")
def hello():
    return {"message": "Patient Management System API"}


@app.get("/about")
def about():
    return {"message": "A fully functional API to manage patient records"}


@app.get("/view")
def view_data():
    data = load_data()
    return data


@app.get("/patient/{patient_id}")
def view_patient(
    patient_id: str = Path(..., description="ID of the patient in the DB", example="P001")
):
    data = load_data()
    if patient_id in data:
        return data[patient_id]
    raise HTTPException(status_code=404, detail="Patient record not found")


@app.get("/sort")
def sort_patient(
    sortby: str = Query(..., description="Provide a valid field like height, weight, or bmi"),
    order: str = Query("asc", description="Sort order: asc or desc"),
):
    valid_fields = ["height", "weight", "bmi"]

    if sortby.lower() not in valid_fields:
        raise HTTPException(status_code=400, detail=f"Invalid field. Choose from {valid_fields}")

    if order not in ["asc", "desc"]:
        raise HTTPException(status_code=400, detail="Select from asc or desc")

    data = load_data()
    sort_order = True if order == "desc" else False

    sorted_data = sorted(
        data.values(), key=lambda x: x.get(sortby, 0), reverse=sort_order
    )
    return sorted_data


@app.post("/create")
def create_patient(patient: Patient):

    # Load the existting data
    data = load_data()
    patient_id = patient.id.lower()
    
    # Check if the patient already exists
    if patient_id in data:
        raise HTTPException(status_code=400, detail="Patient already exists")
    
    # New patient added to the database
    data[patient_id] = patient.model_dump(exclude=['id'])

    #save into the json file
    save_data(data)  

    return JSONResponse(status_code=201, content={"message": "Patient created successfully"})
