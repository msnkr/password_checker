import requests
import hashlib
import sys


def request_api_data(query_characters):
    url = 'https://api.pwnedpasswords.com/range/' + query_characters
    res = requests.get(url)
    if res.status_code != 200:
        raise RuntimeError(f'{res.status_code} error. Please check your api and try again.')
    return res


def get_password_leaks(hashes, hashes_to_check):
    hashes = (line.split(':') for line in hashes.text.splitlines())
    for h, count in hashes:
        if h == hashes_to_check:
            return count
    return 0


def pwned_api_check(password):
    sha1password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    firs5_char, tail = sha1password[:5], sha1password[5:]
    response = request_api_data(firs5_char)
    return get_password_leaks(response, tail)


def main(args):
    for password in args:
        count = pwned_api_check(password)
        if count:
            print(f'Your password has been used {count} times. Please change it.')
        else:
            print('This password is safe.')
        return 'Done.'


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))