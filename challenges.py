import os
import requests
import json

from urllib import request
from colorama import Fore, Style
from tqdm import tqdm
from pathlib import Path

from config import DB_CHALLENGES_FILE, DB_FOLDER, ROOTME_BASE_URL
from users import get_all_info_for_user

def update_challenges_database(cookie):
    print(Fore.YELLOW + "[+] Updating challenges database..." + Style.RESET_ALL)

    challenges = []

    for count in tqdm(range(0,500,50)): #472 challs
        url = f'{ROOTME_BASE_URL}/challenges?debut_challenges={count}'

        r = requests.get(url, cookies={"spip_session" : cookie})
        data = json.loads(r.text)

        for key in data[0]:
            challenges.append(data[0][key])

    filepath = os.path.expanduser(DB_FOLDER + "/" + DB_CHALLENGES_FILE)
    f = open(filepath, 'w')
    f.write(json.dumps(challenges))
    f.close()  

    print(Fore.GREEN + "[+] Challenges databases updated!\n\n" + Style.RESET_ALL)


def get_all_rootme_challenges():
    filepath = os.path.expanduser(DB_FOLDER + "/" + DB_CHALLENGES_FILE)
    chall_db = open(filepath, 'r')
    data = json.load(chall_db)
    chall_db.close()
    return data


def get_chall_ids(challenges):
    return [chall['id_challenge'] for chall in challenges]


def get_all_users_challenges(usernames, cookie):
    challenges = []
    infos = []

    for username in usernames.split(","):
        username = username.strip()
        info = get_all_info_for_user(username, cookie=cookie)
        challenges.append(info['validations'])
        rang = "noob" if "rang" not in info else info['rang']
        position = "X" if info["position"] == "" else info["position"]
        infos.append({"nom": info['nom'], "score": info['score'], "position": position, "rang": rang})

    return [c for chall_per_user in challenges for c in chall_per_user], infos