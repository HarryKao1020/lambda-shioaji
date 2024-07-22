# for local test

import shioaji as sj

if __name__ == "__main__":
    api = sj.Shioaji(simulation=True)
    SHIOAJI_APIKEY = ""
    SHIOAJI_SECRETKEY = ""
    accounts = api.login(SHIOAJI_APIKEY, SHIOAJI_SECRETKEY)
    print(accounts)
