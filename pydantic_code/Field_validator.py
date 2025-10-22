from pydantic import BaseModel, Field, EmailStr, AnyUrl, field_validator
from typing import List, Dict, Optional


class Patient(BaseModel):

    name: str = Field(..., max_length=50)

    email: EmailStr

    linkedin_url: AnyUrl
    age: int = Field(gt=0, lt=100)
    weight: float = Field(gt=0)
    married: Optional[bool] = False
    allergies: Optional[List[str]] = Field(default=None, max_length=5)
    contact_details: Dict[str, str]
    
    #Email validator
    @field_validator('email')
    @classmethod
    def email_validator(cls, value):
        valid_domains = ['hdfc.com', 'icici.com']
        domain_name = value.split('@')[-1]
        if domain_name not in valid_domains:
            raise ValueError('Not a valid domain')
        return value

    #Name transformation
    @field_validator('name')
    @classmethod
    def transform_name(cls, value):
        return value.upper()

    @field_validator("age", mode='after')
    @classmethod
    def validate_age(cls, value):
        if 0 < value < 100:
            return value
        else:
            raise ValueError("Age should be between 0 and 100")

        
    # Field validator operates in two modes: 1. Before mode 2. After mode

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
    "email": "raju@hdfc.com",
    "linkedin_url": "https://linkedin.com/in/23453",  
    "age": "30", 
    "weight": 168,
    "married": True,
    "contact_details": {"phno": "703791xxx"}
}

# Instantiate, unpacking the dictionary and insert
patient1 = Patient(**patient_info) # Validation -> type coercion



insert_patient(patient1)
