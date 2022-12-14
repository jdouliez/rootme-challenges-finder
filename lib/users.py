import requests
import json
import sys

from colorama import Fore, Style
from config import ROOTME_BASE_URL


def search_for_user_id(user_to_search, cookie):
    r = requests.get(ROOTME_BASE_URL + "/auteurs", params={"nom": user_to_search}, cookies={"spip_session" : cookie})
    if r.status_code == 200:
        users = json.loads(r.content)[0]
        for user in users.values():
            if user['nom'] == user_to_search:
                return user['id_auteur']
    elif r.status_code == 401:
        print(Fore.RED + f"\n[!] You are not authorized to use the APi. Check your cookie! \n"  + Style.RESET_ALL)
        print(Fore.YELLOW + "[*] Bye.." + Style.RESET_ALL)
        sys.exit(2)
    else:
        return None


def get_info_from_id(user_id, cookie):
    r = requests.get(f'{ROOTME_BASE_URL}/auteurs/{user_id}', cookies={"spip_session" : cookie})
    if r.status_code == 401:
        print(Fore.RED + f"\n[!] You are not authorized to use the APi. Check your cookie! \n"  + Style.RESET_ALL)
        print(Fore.YELLOW + "[*] Bye.." + Style.RESET_ALL)
        sys.exit(2)
    return json.loads(r.content)


def get_all_info_for_user(username, cookie):
    user_id = search_for_user_id(username, cookie)

    if user_id is None:
        print(Fore.RED + f"\n[!] User {username} has not been found.\nPlease check your spelling!" + Style.RESET_ALL)
        sys.exit(2)

    return get_info_from_id(user_id, cookie = cookie) 


def display_info(info):
    print(f"User \"{Fore.RED + info['nom'] + Style.RESET_ALL}\" is a {info['rang']}")
    print(f" * Score : {info['score']}")
    print(f" * Position : {info['position']}")
    print()
