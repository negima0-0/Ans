import csv
import re
from collections import defaultdict

def extract_role(hostname):
    match = re.match(r"(asw|dsw|gw)", hostname)
    if match:
        return match.group(1)  # 役割の接頭辞を返す
    return "unknown"  # パターンに一致しない場合

def generate_ansible_inventory(csv_file):
    hosts_by_site = defaultdict(lambda: defaultdict(list))
    
    with open(csv_file, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile, delimiter='\t')
        for row in reader:
            site = row['拠点名']
            hostname = row['ホスト名'].split('.')[0]
            role = extract_role(hostname)
            hosts_by_site[site][role].append(hostname)
    
    with open('ansible_inventory.ini', 'w', encoding='utf-8') as inv_file:
        for site, roles in hosts_by_site.items():
            # 各サイトの子グループを定義
            if roles:  # 役割が存在する場合のみ
                inv_file.write(f'[{site}:children]\n')
                for role in roles:
                    inv_file.write(f'{site}_{role}\n')
                inv_file.write('\n')
            
            # 各役割ごとにホスト名を記述
            for role, hostnames in roles.items():
                inv_file.write(f'[{site}_{role}]\n')
                for hostname in hostnames:
                    inv_file.write(f'{hostname}\n')
                inv_file.write('\n')

csv_file = 'hosts.csv'
generate_ansible_inventory(csv_file)
