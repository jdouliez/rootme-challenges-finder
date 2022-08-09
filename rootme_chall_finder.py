import os
import argparse
import os.path
import sys
from colorama import init, Fore, Style

from config import CHALL_CATEGORIES, DB_CHALLENGES_FILE, DB_FOLDER, SPIP_COOKIE_ENV
from auth import login
from users import display_info
from challenges import get_all_rootme_challenges, get_all_users_challenges, get_chall_ids, update_challenges_database

print()

parser = argparse.ArgumentParser(description='Find the RootMe challenges that you and your friends have not done yet and h@ck together!')

parser.add_argument("--update", help="Update the users database", required=False, action='store_true')
parser.add_argument("--login", help="The username to login with", required=False)
parser.add_argument("--cookie", help="Use the ROOTME_SPIP_SESSION env variable as session cookie", required=False)
parser.add_argument("--store-cookie", help="Save the user session cookie as an env variable", required=False, action='store_true')
parser.add_argument("--categories", '-c', help="Challenge categories (separated with a comma (,)", required=False)
parser.add_argument("--list-categories", help="List available categories", required=False, action='store_true')
parser.add_argument("--users", help="Users to compare (separated with a comma (,)", required=False)

args = parser.parse_args()
init()


if args.list_categories:
    print(Fore.YELLOW + "Available challenges categories are : ")
    for id,name in CHALL_CATEGORIES.items():
        print(f"* {name}")
    sys.exit(0)


if args.categories:
    for cat in args.categories.split(","):
        cat = cat.strip()
        if cat not in CHALL_CATEGORIES.values():
            print(Fore.RED + f"\n[-] The category \"{cat}\" does not exist!" + Style.RESET_ALL)
            sys.exit(1)


if not os.path.exists(DB_FOLDER):
    os.system(f"mkdir -p {DB_FOLDER}")

db_path = os.path.expanduser(DB_FOLDER + "/" + DB_CHALLENGES_FILE)
if not os.path.exists(db_path) and not args.update:
    print(Fore.YELLOW + "\n[-] You have no challs databases. Please use the --update option!" + Style.RESET_ALL)
    sys.exit(1)


if args.login:
    # TODO : Remove message when API works again
    print(Fore.RED + "\n[!] The RootMe login API does not seem to work properly. You should use the --cookie option instead!" + Style.RESET_ALL)
    sys.exit(2)
    print(Fore.YELLOW + "[+] Authentication ..." + Style.RESET_ALL)
    password = input(f"[>] RootMe password for account \"{args.login}\" : ")
    spip_cookie = login(args.login, password)
    del password

elif args.cookie:
    spip_cookie = args.cookie

elif os.environ.get(SPIP_COOKIE_ENV):
    print(Fore.YELLOW + "[+] Using Rootme spip cookie from env variable!\n" + Style.RESET_ALL)
    spip_cookie = os.environ.get(SPIP_COOKIE_ENV)

else:
    print(Fore.RED + "\n[!] You have to provide an authentication method. Please use the --login or --cookie option!" + Style.RESET_ALL)
    sys.exit(1)


if spip_cookie and args.store_cookie:
    # TODO : Seems broken. Env variable is not set
    os.environ[SPIP_COOKIE_ENV] = spip_cookie
    print(Fore.GREEN + "[+] Rootme cookie successfully saved in env variable!" + Style.RESET_ALL)


if args.update:
    update_challenges_database(cookie=spip_cookie)


if args.users and len(args.users.split(",")) < 2:
    print(Fore.RED + "\n[-] You have to provide at least two usernames. Please use the --users with some usernames separated with comma (,)!" + Style.RESET_ALL)
    sys.exit(1)
elif not args.users:
    exit(0)

rootme_challenges = get_all_rootme_challenges()
rootme_challenges_ids = get_chall_ids(rootme_challenges)

users_challenges, users_infos = get_all_users_challenges(args.users, spip_cookie)
users_challenges_ids = get_chall_ids(users_challenges)

print(Fore.GREEN + f"\n[+] ==========================")
print(f"[+]      Players info        ")
print(f"[+] ==========================" + Style.RESET_ALL)
for info in users_infos:
    display_info(info)

available = set(rootme_challenges_ids).difference(set(users_challenges_ids))
print(Fore.YELLOW + f"[+] We have found {len(available)} challenges hackable together.\n" + Style.RESET_ALL)

user_categories = [c.strip() for c in args.categories.split(",")] if args.categories else None
for cat_id, cat_name in CHALL_CATEGORIES.items():
    if args.categories and cat_name not in user_categories:
        continue

    print(Fore.GREEN + f"[+] {'=' * (22 + len(cat_name) + 2)}")
    print(f"[+]             {cat_name}            ")
    print(f"[+] {'=' * (22 + len(cat_name) + 2)}" + Style.RESET_ALL)

    for c in rootme_challenges:
        if c['id_challenge'] in available and int(c['id_rubrique']) == cat_id:
            print(f" * {c['titre']}")
    print("")
