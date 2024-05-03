# External Imports
# Import only with "import package",
# it will make explicitly in the code where it came from.

# Turns all annotations into string literals.
# This is one exception to the external import rule.
from __future__ import annotations
import json


class NextObject:
    """
    Represents an object created from a response of the iControl REST API.

    Attributes:
        properties (dict): A dictionary representing the properties of the object as
                           returned by the iControl REST API.
    """

    def __init__(self, properties: dict):
        if not isinstance(properties, dict):
            raise ValueError("properties must be a dictionary")
        self.properties = properties

    def __str__(self) -> str:
        """Converts the object to a string in JSON format with indentation for readability."""
        try:
            return json.dumps(self.properties, indent=4)
        except TypeError as e:
            return f"Error converting to string: {str(e)}"
