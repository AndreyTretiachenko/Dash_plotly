import requests as rq
import pandas as pd
import datetime
import time


# получение списка звонков по салону из ВАТС Мегафон
def get_megafon_source(command, period, type):
    rq.session()
    r = rq.get("https://ip-vladikin.megapbx.ru/sys/crm_api.wcgp",
               params={
                   "cmd": command,
                   "token": "2f429531-c28c-4d4e-ace8-ff0aa763983f",
                   "period": period,
                   "type": type
               })
    try:
        with open(f"{command}_{period}_{type}.csv", "w") as f:
            f.write(r.text)
            f.close()
    except FileExistsError:
        print("File is already created")
    if command == "history":
        df = pd.read_csv(f"{command}_{period}_{type}.csv", header=None)
        df = df.rename(columns={0: "index", 1: "UID", 2: "Type",
                                3: "client", 4: "account", 5: "via",
                                6: "start", 7: "wait", 8: "duration", 9: "record"})
        return df
    elif command == "accounts":
        df = pd.DataFrame.from_records(r.json())
        return df




# получение списка потенциальных покупателей из amoCRM
def get_source_amocrm():

    pass


# получение списка покупателей по салону из 1С
def get_source_1c():
    pass


def main():
    print(__name__)
    accounts = get_megafon_source("accounts", "", "")
    history = get_megafon_source("history", "yesterday", "miss")
    print(accounts.head())
    print(history.head())
    pass


if __name__ == "__main__":
    main()