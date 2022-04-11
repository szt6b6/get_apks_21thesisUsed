# read data from file apk_code_analysis_riskid.csv
with open(r"apk_code_analysis_riskid.csv") as f:
    all_data = f.readlines()
f.close()

# get anrodi risk ids from all_data
ids = []
for one_data in all_data:
    ids += one_data.split(",")[1:-2]
    ids = list(set(ids))

# count the times of id in all_data
count_results = {}
for id in ids:
    count_results[id] = 0
    for one_data in all_data:
        count_results[id] += one_data.count(id)

# write sorted result into file android_code_potential_risks.csv
count_results = dict(sorted(count_results.items(), key=lambda item: item[1]))
with open("android_code_potential_risks.csv", "w+") as f:
    for id, count in count_results.items():
        f.writelines(id + " , " + str(count) + "\n")
print(count_results)