import os
import json

DIR="./tables"
os.makedirs(DIR, exist_ok=True)

with open("table.json") as table_template:
    table_content = json.load(table_template)

for i in range(1000):
    table_name = f"blobs{i}"
    table_content["tableName"] = table_name
    with open(os.path.join(DIR, f"cilrate-{table_name}"), mode="w") as output:
        output.write(json.dumps(table_content))
