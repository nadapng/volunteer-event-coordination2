import json
from volunteer_event_coordination.infrastructure_layer.event import Event
from typing import List

class User:
    """ Implements a User entity """

    def __init__(self):
        self.id = 0
        self.full_name = ""
        self.email = ""
        self.phone = ""
        self.role = ""
        self.created_at = ""
        self.events:List[Event] = []

    def __str__(self)-> str:
        return self.to_json()
    
    def __repr__(self)-> str:
        return self.to_json()
    
    def to_json(self)-> str:
        supplier_dict = {}
        supplier_dict["id"] = self.id
        supplier_dict["full_name"] = self.full_name
        supplier_dict["email"] = self.email 
        supplier_dict["phone"] = self.phone
        supplier_dict["role"] = self.role
        supplier_dict["created_at"] = self.created_at
        supplier_dict["events"] = []

        for event in self.events:
            supplier_dict["events"].append(event.__dict__)
        
        return json.dumps(supplier_dict)