from pydantic import BaseModel

class Address(BaseModel):

    city: str
    state: str
    pincode: int



class Patient(BaseModel):

    name: str
    age: int
    address: Address

def display():
    print(address1.city)
    print("Address updated")

address_dict = {'city':'Meerut', "state": "Uttar Pradesh", 'pincode':"656677"}

address1 = Address(**address_dict)

display()