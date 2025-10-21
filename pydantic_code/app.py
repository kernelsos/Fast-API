from pydantic import BaseModel

class Patient(BaseModel):

    name : str
    age : int

def insert_patient(patient: Patient):
    print(patient.name)
    print(patient.age)
    print("Data insertion successful")

patient_info = {"name": "Gagan", "age": "30"} # Instantiate the pydantic object 

patient1 = Patient(**patient_info) # ** unpacking the dictionary

insert_patient(patient1)

