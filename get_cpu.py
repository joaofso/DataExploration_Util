import json
import glob
from statistics import mean

PATH = "/home/eourjoa/Desktop/VNodeComparison/16vNodes/150t"


for file in glob.iglob(f"{PATH}/*"):
    if file.endswith("cpu.json"):
        print(file)
        with open(file) as cpu_file:
            cpu_loads = []
            content = json.load(cpu_file)
            for entry in content["data"]["result"]:
                pod = entry["metric"]["pod"]
                cpu_consumption = entry["value"][1]
                cpu_loads.append(float(cpu_consumption))
                #print(f"{pod}: {cpu_consumption}")
            print(f"Average: {mean(cpu_loads)}")