from copy import copy
from models.attribute import AttributeModel
from .base_repository import Repository


class AttributeRepository(Repository):
    model = AttributeModel
    def __init__(self):
        super().__init__(self.model)

    async def create(self, payload:dict):
        processed_payload = self.process_payload(payload)
        record = await super().create(processed_payload)
        return record
    
    @staticmethod
    def process_payload(payload:dict):
        data = copy(payload)
        
        if data["is_numeric"] is False:
            keys_to_none = {"measurement_type", "unit"}
            for key in keys_to_none:
                data[key] = None 
        
        data["options"] = ( None 
                        if data["type"] != "select"
                        else data["options"]
                        )
        return data