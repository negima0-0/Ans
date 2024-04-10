import csv
from collections import defaultdict

def generate_ansible_inventory(csv_file):
    # ホストの分類を保持する辞書
    hosts_by_site = defaultdict(lambda: defaultdict(list))
    
    # CSVファイルを読み込み、データを分類
    with open(csv_file, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile, delimiter='\t')
        for row in reader:
            site = row['拠点名']
            hostname = row['ホスト名'].split('.')[0]  # ドメイン名を除外
            role = hostname.split('1')[0]  # '1'を区切りとして役割を特定
            hosts_by_site[site][role].append(hostname)
    
    # Ansibleインベントリファイルの生成
    with open('ansible_inventory.ini', 'w', encoding='utf-8') as inv_file:
        for site, roles in hosts_by_site.items():
            inv_file.write(f'[{site}:children]\n')
            for role in roles:
                inv_file.write(f'{site}_{role}\n')
            inv_file.write('\n')
            
            for role, hostnames in roles.items():
                inv_file.write(f'[{site}_{role}]\n')
                for hostname in hostnames:
                    inv_file.write(f'{hostname}\n')
                inv_file.write('\n')

# CSVファイルのパスを指定
csv_file = 'hosts.csv'
# 関数を呼び出してインベントリファイルを生成
generate_ansible_inventory(csv_file)
