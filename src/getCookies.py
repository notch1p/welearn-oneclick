import requests
import sys


def getCookies(cred, save=False):
    session = requests.Session()
    response = requests.get(
        'https://welearn.sflep.com/user/prelogin.aspx?loginret=http%3a%2f%2fwelearn.sflep.com%2fuser%2floginredirect.aspx', allow_redirects=False)
    rturl = response.headers['Location'].replace(
        'https://sso.sflep.com/idsvr', '')
    data = {
        'rturl': rturl,
        'account': cred[0],
        'pwd': cred[1],
    }
    session.post(
        "https://sso.sflep.com/idsvr/account/login", data=data)
    url = 'https://sso.sflep.com/idsvr'+rturl
    session.get(url)
    if save:
        with open('cookies.txt', 'w+') as data:
            data.write(str(session.cookies.get_dict()))
    return session.cookies.get_dict()


def getCookiesFromCommand(s):
    try:
        cred = s.split(':')
        return getCookies(cred)
    except:
        print('input username and password')
        sys.exit(1)


def getCookiesFromUser():
    cred = input("Input your username and password, split by ,: ").split(',')
    return getCookies(cred)


def parseCookie(s):
    return dict(map(lambda x: x.split('=', 1), s.split(';')))


def getFromCommand():
    if (sys.argv[1] == '--parse' or '-p'):
        try:
            return parseCookie(sys.argv[2])
        except:
            print('invalid input')
            sys.exit(1)
    elif (sys.argv[1] == '--user' or '-u'):
        try:
            return getCookiesFromCommand(sys.argv[2])
        except:
            print("invalid username & password")
            sys.exit(1)
