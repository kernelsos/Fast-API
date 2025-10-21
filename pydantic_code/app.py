from pydantic import BaseModel
from typing import List, Dict, Optional

class Patient(BaseModel):

    name : str
    age : int
    weight: float
    married: Optional[bool] = False
    allergies: Optional[List[str]] = None
    contact_details: Dict[str,str]

def insert_patient(patient: Patient):
    print(patient.name)
    print(patient.age)
    print(patient.married)
    print(patient.allergies)
    print(patient.contact_details)
    print("Data insertion successful")

patient_info = {"name": "Gagan", "age": "30", "weight":168 ,"married": True, "contact_details":{"phno":"703791xxx"}} # Instantiate the pydantic object 

patient1 = Patient(**patient_info) # ** unpacking the dictionary

insert_patient(patient1)

