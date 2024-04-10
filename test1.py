import csv
import yaml
import json

def classify_host(hostname):
    if hostname.startswith('asw'):
        return 'asw'
    elif hostname.startswith('dsw'):
        return 'dsw'
    elif hostname.startswith('gw'):
        return 'gw'
    else:
        return 'other'

def csv_to_yaml(csv_file):
    data = {}
    with open(csv_file, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            site = row['拠点名']
            hostname = row['ホスト名']
            ip_address = row['IPアドレス']
            description = row['説明']
            credential_id = int(row['認証情報ID'])
            group = classify_host(hostname)
            if site not in data:
                data[site] = {'asw': {}, 'dsw': {}, 'gw': {}, 'other': {}}
            data[site][group][hostname] = {
                'ansible_host': ip_address,
                'description': description,
                'credential': credential_id
            }
    return yaml.dump(data, allow_unicode=True, default_flow_style=False)

def csv_to_json(csv_file):
    data = {}
    with open(csv_file, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            site = row['拠点名']
            hostname = row['ホスト名']
            ip_address = row['IPアドレス']
            description = row['説明']
            credential_id = int(row['認証情報ID'])
            group = classify_host(hostname)
            if site not in data:
                data[site] = {'asw': {}, 'dsw': {}, 'gw': {}, 'other': {}}
            data[site][group][hostname] = {
                'ansible_host': ip_address,
                'description': description,
                'credential': credential_id
            }
    return json.dumps(data, ensure_ascii=False, indent=2)

csv_file = 'hosts.csv'  # ここにCSVファイルのパスを指定

# YAML形式に変換して保存
yaml_data = csv_to_yaml(csv_file)
with open('output.yaml', 'w', encoding='utf-8') as yaml_file:
    yaml_file.write(yaml_data)

# JSON形式に変換して保存
json_data = csv_to_json(csv_file)
with open('output.json', 'w', encoding='utf-8') as json_file:
    json_file.write(json_data)
