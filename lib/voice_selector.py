import os
import glob
import subprocess

CHARACTER_VOICE_SWITCH = {
    "Shadowheart": "v3ed74f063c6042dc83f6f034cb47c679",
    "Astarion": "vc7c13742bacd460a8f65f864fe41f255"
}

# 사용자로부터 캐릭터 선택
print("음성을 수정할 캐릭터를 선택하세요. (1: Shadowheart, 2: Astarion)")
selected_character = int(input("숫자 입력: "))

if selected_character == 1:
    input_character = CHARACTER_VOICE_SWITCH["Shadowheart"]
elif selected_character == 2:
    input_character = CHARACTER_VOICE_SWITCH["Astarion"]
else:
    print("올바른 숫자를 입력하세요.")
    exit()

print("[+] 음성 변환을 시작합니다. 사양에 따라서 10분이상 소요 될 수 있습니다.")
wem_files = glob.glob('./Voice/Mods/Gustav/Localization/English/SoundBanks/*.wem')
output_folder = './Mangio-RVC-v23.7.0/audios'
for wem_file in wem_files:
    if os.path.basename(wem_file).startswith(input_character):
        output_wav_file = os.path.join(output_folder, os.path.splitext(os.path.basename(wem_file))[0] + '.wav')
        subprocess.run(['./lib/vgmstream/vgmstream-cli.exe', '-o', output_wav_file, wem_file], stdout=subprocess.PIPE)

print("[+] 음성 변환 완료")