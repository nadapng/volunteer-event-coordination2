import json

class Event:
    """ Implements a Event entity """

    def __init__(self):
        self.id = 0
        self.title = ""
        self.description = ""
        self.location = ""
        self.starts_at = ""
        self.ends_at = ""
        self.capacity = 0
        self.created_by = 0
        self.created_at = ""

    def __str__(self)-> str:
        return self.to_json()
    
    def __repr__(self)-> str:
        return self.to_json()
    
    def to_json(self)-> str:
        supplier_dict = {}
        supplier_dict["id"] = self.id
        supplier_dict["title"] = self.title
        supplier_dict["description"] = self.description
        supplier_dict["location"] = self.location
        supplier_dict["starts_at"] = self.starts_at
        supplier_dict["ends_at"] = self.ends_at
        supplier_dict["capacity"] = self.capacity
        supplier_dict["created_by"] = self.created_by
        supplier_dict["created_at"] = self.created_at

        return json.dumps(supplier_dict)