import requests as rq
import pandas as pd
import datetime
import time


# получение списка звонков по салону из ВАТС Мегафон
def get_megafon_source(command, period, ctype):
    rq.session()
    r = rq.get("https://ip-vladikin.megapbx.ru/sys/crm_api.wcgp",
               params={
                   "cmd": command,
                   "token": "2f429531-c28c-4d4e-ace8-ff0aa763983f",
                   "period": period,
                   "type": ctype
               })
    try:
        with open(f"{command}_{period}_{ctype}.csv", "w") as f:
            f.write(r.text)
            f.close()
    except FileExistsError:
        print("File is already created")
    if command == "history":
        df = pd.read_csv(f"{command}_{period}_{ctype}.csv", header=None, usecols=[0, 1, 2, 3, 4, 5, 6, 7, 8])
        df = df.rename(columns={0: "UID", 1: "Type", 2: "client",
                                3: "account", 4: "via", 5: "Start",
                                6: "wait", 7: "duration", 8: "record"})
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

    pass


if __name__ == "__main__":
    main()