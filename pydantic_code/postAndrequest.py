from fastapi import FastAPI, Path, HTTPException, Query
from fastapi.responses import JSONResponse
import json
from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Literal, Optional

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

class PatientUpdate(BaseModel):
    name: Annotated[Optional[str], Field(default=None)]
    city: Annotated[Optional[str], Field(default=None)]
    age: Annotated[Optional[int], Field(gt=0, lt=120, default=None)]
    gender: Annotated[Optional[Literal['male', 'female', 'others']], Field(default=None)]
    height: Annotated[Optional[float], Field(gt=0, default=None)]
    weight: Annotated[Optional[float], Field(gt=0, default=None)]



# ------------------------------
# Utility functions
# ------------------------------
def load_data():
    try:
        with open("patient.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}  # return empty dict if file not found


def save_data(data):
    with open("patient.json", "w") as f:
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
    patient_id = patient.id.lower() #there was a mismatch of case in patient id
    
    # Check if the patient already exists
    if patient_id in data:
        raise HTTPException(status_code=400, detail="Patient already exists")
    
    # New patient added to the database
    data[patient_id] = patient.model_dump(exclude=['id'])

    #save into the json file
    save_data(data)  

    return JSONResponse(status_code=201, content={"message": "Patient created successfully"})


@app.put('/edit/{patient_id}')
def update_patient(patient_id: str, patient_update: PatientUpdate):

    data = load_data()

    if patient_id not in data:
        raise HTTPException(status_code=404, detail="Patient ID not found")
    
    existing_patient_info = data[patient_id]
    # To make things easily convert patient_update object into dictionary using model.dump and unset to include only the fields given by the user not all fields

    updated_patient_info = patient_update.model_dump(exclude_unset=True)

    for key, value in updated_patient_info.items():
        existing_patient_info[key] = value

    # existing_patient_info -> pydantic object -> updated bmi + verdict -> pydantic object -> dict
    existing_patient_info['id'] = patient_id

    patient_pydantic_obj = Patient(**existing_patient_info) # Running only this command can give error because you cannot make pydantic model directly from the patients.json dictionary because one id is missing.

    #pydantic object -> dict
    existing_patient_info = patient_pydantic_obj.model_dump(exclude="id")

    # Add this dict to data
    data[patient_id] = existing_patient_info

    #save Data
    save_data()

    return JSONResponse(status_code=200, content={'message': "Patient details updated"})

@app.delete('/delete/{patient_id}')
def delete_patient(patient_id: str):
    #Load data
    data = load_data()
    if patient_id not in data:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    del data[patient_id]

    save_data(data)

    return JSONResponse(status_code=200, content={"message":"Patient deleted"})