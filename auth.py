import requests
import json
import sys

from config import ROOTME_BASE_URL
from colorama import Fore, Style

def login(login, password):
        r = requests.post(
            ROOTME_BASE_URL + '/login',
            json={
                'login': login.lower(),
                'password': password
            }
        )
        del password
        
        if r.status_code != 200:
            print(Fore.RED + 'An error occurred during login (HTTP %d)' % r.status_code + Style.RESET_ALL)
            sys.exit(2)
            return None
        else:
            response = json.loads(r.content)[0]
            
            if 'error' in response.keys():
                print(Fore.RED + 'An error occurred during login ->  %s : %s)' % (response['error']['code'], response['error']['message']) + Style.RESET_ALL)
                sys.exit(2)
            elif 'info' in response.keys():
                if "spip_session" in response['info'].keys() and response['info']['code'] == 200:
                    return response['info']["spip_session"]
                else:
                    return None
        