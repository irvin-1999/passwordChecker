import sys

import requests
import hashlib


def request_api_data(query_char):
    url = 'https://api.pwnedpasswords.com/range/' + 'CBFDA'
    res = requests.get(url)
    if res.status_code != 200:
        raise RuntimeError(f"Error fetching:{res.status_code},check the api and try again")
    return res


def get_password_leaks_count(hashes, hash_to_check):
    hashes = (line.split(":") for line in hashes.text.splitlines())
    for h, count in hashes:
        if h == hash_to_check:
            return count
    return 0



def pwned_api_check(password):
    shalpassword = hashlib.sha1(password.encode("utf-8")).hexdigest().upper()
    first5_char, tail = shalpassword[:5], shalpassword[5:]
    res = request_api_data(first5_char)
    return get_password_leaks_count(res, tail)

def main(args):
    for password in args:
        count = pwned_api_check(password)
        if count:
            print(f"{password} was found {count} times. You should Prolly Change it")
        else:
            print(f"{password} was NOT found. Carry on!")


main(sys.argv[1:])