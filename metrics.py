occurrences ={} 
with open("/home/eourjoa/Desktop/CassandraExporter/metrics_from_pod", "r") as file:
    for line in file.readlines():
        if not line.startswith("#"):
            metric = line.split("{")[0].strip()
            if metric != "":
                metrics = occurrences.get(metric, 0)
                metrics += 1
                occurrences[metric] = metrics 
    
    acumulator = 0
    for entry in occurrences:
        value = occurrences[entry]
        acumulator += value
        print(f"{entry}\t{value}")
    print(f"Total occurrences: {acumulator}")