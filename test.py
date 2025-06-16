import json


with open('/Users/nraviz/Library/Application Support/JetBrains/PyCharm2023.3/scratches/scratch_2.json', 'r') as file:
    json_data = file.read()

# Convert JSON to a dictionary
data = json.loads(json_data)
print(data)

# Create a map between 'key' and 'readable_name'
key_to_readable_name = {
    item["key"]: item["readable_name"]
    for item in data['properties'] if isinstance(item, dict) and "key" in item and "readable_name" in item
}

# Print the map
print(key_to_readable_name)
