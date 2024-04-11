import json
# Given a json object with any depth, the functions turns it into a schema with key: data type pairs.
# Only accepts objects, not arrays
def json_to_schema(json_obj, schema=None):
    # Initial check to ensure json_obj is a dictionary
    if schema is None and not isinstance(json_obj, dict):
        raise ValueError('json_obj must be a dictionary')
    
    # Create empty structure when first called
    if schema is None:
        if isinstance(json_obj, dict):
            schema = {}
        else:
            schema = []
        
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
    # **** Need to compress the output so if there are multiple objects in the list, it should only return one schema
    elif isinstance(json_obj, list):
        # Potential Idea: track earlier structures and if a structure is repeated, don't add it to the schema instead of removing later
        unique_items = []
        seen_stuctures = set()
                
        for item in json_obj:
            # if value is a dictionary, append empty dict and call the function recursively
            if isinstance(item, dict):
                schema.append({})
                json_to_schema(item, schema[-1])
            # if value is a list, append empty list and call the function recursively
            elif isinstance(item, list):
                schema.append([])
                json_to_schema(item, schema[-1])
            # otherwise its a primitive type
            else:
                # only add the primitive type if it's not already in the schema
                if type(item).__name__ not in schema:
                    schema.append(type(item).__name__)
        # after iterating through all items in the list, remove duplicates
        # I already handle duplicate primitives so now I just need to handle duplicate lists and dictionaries
        unique_tuples = set(tuple(sorted(sub_schema.items())) for sub_schema in schema if isinstance(sub_schema, dict))
        print('unique tuples: ', unique_tuples)
        schema + [dict(tup) for tup in unique_tuples]
        print('schema: ', schema)   
        
        
    return schema


def main():
    json_obj = {
        # 'name': 'John Doe',
        # 'age': 30,
        # 'is_student': False,
        # 'address': {
        #     'street': '123 Main St',
        #     'city': 'Anytown',
        #     'zip': 12345
        # },
        # 'grades': [90, 85, 88],
        'classes': [
            {
                'name': 'Math',
                'grade': 90
            },
            {
                'name': 'Science',
                'grade': 85
            }
        ],
        # "list_of_lists": [[1, 2, 3], [4, 5, 6]],
    }
    schema = json_to_schema(json_obj)
    # json.dumps to format it
    print(json.dumps(schema, indent=4))
    
if __name__ == '__main__':
    main()