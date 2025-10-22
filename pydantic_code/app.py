from pydantic import BaseModel, Field, EmailStr, AnyUrl
from typing import List, Dict, Optional

# EmailStr command is not working , use command "pip install "pydantic[email]"""

class Patient(BaseModel):
    name: str = Field(..., max_length=50)
    email: EmailStr
    linkedin_url: AnyUrl
    age: int = Field(gt=0, lt=100)
    weight: float = Field(gt=0)
    married: Optional[bool] = False
    allergies: Optional[List[str]] = Field(default=None, max_length=5)
    contact_details: Dict[str, str]

def insert_patient(patient: Patient):
    print(patient.name)
    print(patient.age)
    print(patient.married)
    print(patient.allergies)
    print(patient.contact_details)
    print(patient.email)
    print(patient.linkedin_url)
    print("Data insertion successful")

patient_info = {
    "name": "Gagan",
    "email": "raju@gmail.com",
    "linkedin_url": "https://linkedin.com/in/23453",  
    "age": 30, 
    "weight": 168,
    "married": True,
    "contact_details": {"phno": "703791xxx"}
}

# Instantiate and insert
patient1 = Patient(**patient_info)
insert_patient(patient1)
