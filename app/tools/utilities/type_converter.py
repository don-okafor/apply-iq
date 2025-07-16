from typing import Any, Dict
import json

class TypeConverter:

    def __init__(self):
        pass

    def get_dict_from_json(self, json_data:str) -> Dict[str, Any]:
        """Return the json data."""
         # Clean the string
        if json_data and json_data.startswith("```json"):
            # Remove ```json and get JSON body
            json_data = json_data.strip("`").split("\n", 1)[1]  
            json_data = json_data.rsplit("\n```", 1)[0]
            # Convert JSON text to Python dictionary
            return json.loads(json_data)
        else:
            return json_data
