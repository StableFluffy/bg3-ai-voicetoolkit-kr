import os
import glob
import subprocess
import re
import uuid

print("[+] 확장자 변환 시작")

wem_files = glob.glob('./Wem/*.*')

pattern = r"\.wav_[0-9A-F]+.wem$"
subst = ".wem"

for wem_file in wem_files:
    updated_name = re.sub(pattern, subst, wem_file)
    if wem_file != updated_name:
        os.rename(wem_file, updated_name)

print("[+] 확장자 변환 완료")


# Copy Folder ./Mod_Folder/Sample
input_mod = input("모드의 이름을 지정해주세요 : ")
input_description = input("모드의 설명을 입력해주세요 : ")
print("[+] 폴더 복사 시작")
source_folder = '.\lib\Mod_Folder\SampleMod'
destination_folder = f'.\lib\Mod_Folder\{input_mod}'
subprocess.run(['xcopy', source_folder, destination_folder, '/e', '/i', '/h', '/y'])

wem_files = glob.glob('./Wem/*.*')
for wem_file in wem_files:
    os.rename(wem_file, f'./lib/Mod_Folder/{input_mod}/Mods/Gustav/Localization/English/Soundbanks/{os.path.basename(wem_file)}')
print("[+] 폴더 복사 완료")

import xml.etree.ElementTree as ET
tree = ET.parse(f'./lib/Mod_Folder/{input_mod}/Mods/SampleMod/meta.lsx')
root = tree.getroot()

for attribute in root.findall(".//attribute"):
    attribute_id = attribute.get("id")
    
    if attribute_id == "Name":
        attribute.set("value", input_mod)
    elif attribute_id == "Folder":
        attribute.set("value", input_mod)
    elif attribute_id == "Description":
        attribute.set("value", input_description)
    elif attribute_id == "UUID":
        uuid_str = str(uuid.uuid4())
        attribute.set("value", uuid_str)

# 수정된 내용을 파일에 저장
tree.write(f'./lib/Mod_Folder/{input_mod}/Mods/SampleMod/meta.lsx')

with open(f'./lib/Mod_Folder/{input_mod}/Mods/SampleMod/meta.lsx', "r+") as f:
    content = f.read()
    f.seek(0, 0) # move cursor to the beginning of the file
    f.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n" + content)

if not os.path.exists(f'./lib/Mod_Folder/{input_mod}/Mods/{input_mod}'):
    os.rename(f'./lib/Mod_Folder/{input_mod}/Mods/SampleMod', f'./lib/Mod_Folder/{input_mod}/Mods/{input_mod}')

print("[+] lsx 생성 완료.")
print("[+] pak 파일 생성 시작")
source_directory = os.path.join(os.getcwd(), 'lib\Mod_Folder', input_mod)
destination_directory = os.path.join(os.getcwd(), 'Mods', input_mod + '.pak')

# divine.exe로 pak 파일 생성
subprocess.run(['.\lslib\Tools\divine.exe', '-g', 'bg3', '-s', source_directory, '-d', destination_directory, '-a', 'create-package', '-c', 'none'], shell=True)
with open(f'./Mods/{input_mod}.pak', 'rb+') as f:
  f.seek(0x15)
  f.write(int.to_bytes(25, 4, byteorder='little'))
print("[+] pak 파일 생성 완료")