# Given a json object with any depth, the functions turns it into a schema with key: data type pairs.
# Only accepts objects, not arrays
def json_to_schema(json_obj, schema=None):
    # Initial check to ensure json_obj is a dictionary
    if schema is None and not isinstance(json_obj, dict):
        raise ValueError('json_obj must be a dictionary')
    
    # Create empty dict when first called
    if schema is None:
        schema = {}
        
    # handle when json_obj is a dictionary
    if isinstance(json_obj, dict):
        for key, value in json_obj.items():
            # if value is a dictionary, call the function recursively
            if isinstance(value, dict):
                schema[key] = {}
                json_to_schema(value, schema[key])
            # if value is a list, call the function recursively
            elif isinstance(value, list):
                schema[key] = []
                json_to_schema(value, schema[key])
            # otherwise its a primitive type
            else:
                schema[key] = type(value).__name__
                
    # handle when json_obj is a list
    elif isinstance(json_obj, list):
        # *** THIS IS WRONG ***
        schema[key] = []
        for item in json_obj:
            # if value is a dictionary, call the function recursively
            if isinstance(item, dict):
                schema[key] = {}
                json_to_schema(item, schema[key])
            # if value is a list, call the function recursively
            elif isinstance(value, list):
                schema[key] = []
                json_to_schema(value, schema[key])
            # otherwise its a primitive type
            else:
                schema[key] = type(value).__name__
    
        
    return schema


def main():
    json_obj = {
        'name': 'John Doe',
        'age': 30,
        'is_student': False,
        'address': {
            'street': '123 Main St',
            'city': 'Anytown',
            'zip': 12345
        },
        'grades': [90, 85, 88]
    }
    # schema = json_to_schema(json_obj)
    print(type(json_obj).__name__)
    
if __name__ == '__main__':
    main()