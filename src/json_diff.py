from jsondiff import diff

def compare_json(json1, json2):
    return diff(json1, json2)


def main():
    json1 = {
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
    json2 = {
        'name': 'Jane Doe',
        'age': 30,
        'is_student': False,
        'address': {
            # 'street': '123 Main St',
            'city': 'Anytown',
            'zip': 12345
        },
        'grades': [90, 85, 88]
    }
    json3 = {
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
    comparison = compare_json(json1, json3)
    print(comparison if comparison else 'No differences found')
    
if __name__ == '__main__':
    main()