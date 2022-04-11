import json
import os
import requests

def pict_codeAnalysis_metadata_ids(response_json_text):
    contend = json.loads(response_json_text)
    apkname = contend["file_name"]
    ids = contend['code_analysis'].keys()
    return apkname, ids


def write_ids_and_apkname_to_file(ids, apkname, desfile_path):
    with open(desfile_path, 'a+') as f:
        f.write(str(apkname.encode("utf-8")) + ",")
        for id in ids:
            f.write(id + ",")
        f.write("\n")
        f.close()
    return


def find_apk_hash():
    mobsf_root_path = "E:\\Mobile-Security-Framework-MobSF-master\\mobsf\\uploads"
    dirs = os.listdir(mobsf_root_path)
    return dirs

# use mobsf api to collect all apk static json report
def get_all_json_reports():
    desfile_path = ".\\apk_code_analysis_riskid.csv"
    store_json_as  = ".\\jsons\\"
    # curl -X POST --url http://localhost:8000/api/v1/report_json --data "hash=82ab8b2193b3cfb1c737e3a786be363a" -H "X-Mobsf-Api-Key:68d67708c7fc314d828e29ab79e18259f0c11aaaf344ea65de6540d6ac7df919"
    # hash need to find in file explore

    headers = {"X-Mobsf-Api-Key" : "68d67708c7fc314d828e29ab79e18259f0c11aaaf344ea65de6540d6ac7df919"}
    dirs_hash = find_apk_hash()
    for hash_value in dirs_hash:
        payload = {"hash" : hash_value}
        response_json = requests.post(url="http://localhost:8000/api/v1/report_json", data=payload, headers=headers)
        if(response_json.status_code == 200):
            apkname, ids = pict_codeAnalysis_metadata_ids(response_json.text)
            print(apkname)
            open(store_json_as + apkname + ".json", "wt").writelines(response_json.text)
            write_ids_and_apkname_to_file(ids, apkname, desfile_path)
        else:
            print(hash_value + " is not scaned completely yet")

# collect useful info from apk json report file
def get_apkname_and_security_score():
    jsons_path = ".\\jsons\\"
    dirs = os.listdir(jsons_path)
    f = open("static_info_collect.csv", "w+")
    f.writelines("apkname" + "," + "security_score" + "," + "target_sdk" + "," + "min_sdk" + "," + "average_cvss" + "," + "host_os" + "," + "virus_total" + "\n")
    for dir in dirs:
        json_content = json.loads(open(jsons_path + dir).read())
        security_score = json_content["security_score"]
        target_sdk = json_content["target_sdk"]
        min_sdk = json_content["min_sdk"]
        average_cvss = json_content["average_cvss"]
        host_os = json_content["host_os"]
        virus_total = json_content["virus_total"]
        print(str(dir.encode("utf-8"))[2:-6]+ "," + str(security_score) + "," + str(target_sdk) + "," + str(min_sdk) + "," + str(average_cvss) + "," + str(host_os) + "," + str(virus_total))

        f.writelines(str(dir.encode("utf-8"))[2:-6] + "," + str(security_score) + "," + str(target_sdk) + "," + str(min_sdk) + "," + str(average_cvss) + "," + str(host_os) + "," + str(virus_total) + "\n")
    f.close()


get_apkname_and_security_score()