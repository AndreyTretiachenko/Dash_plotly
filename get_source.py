import requests as rq
import pandas as pd
import datetime
import time
import json
import os


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
def get_source_amocrm(dataframe):
    # проверка и обновление токенов для доступа к amoCRM начало
    with open(f"{os.path.dirname(__file__)}\\token", "r", encoding="utf-8") as file_in:
        data = json.load(file_in)
    access_token = data["access_token"]
    refresh_token = data["refresh_token"]
    if rq.get("https://meb290.amocrm.ru/api/v4/account",
        headers = {"Authorization": f"Bearer {access_token}"}).status_code != "200":
        print("access OK")
    else:
        print("access FALSE")
        r_amo_refresh = rq.post("https://meb290.amocrm.ru/oauth2/access_token",
        json={
        "client_id": "ecb8ec97-98c3-4fd1-9777-a9935113974f",
        "client_secret": "JscDfuHoUTwLR8V5gkHMYIDdfXBQUHsgaXDx7Jv5yAZt3LgJKfkbm8Hsmkd0jQF6",
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
        "redirect_uri": "https://mail.ru"
        },
        headers={"Content-Type": "application/json"}
        ).json()
        data["access_token"] = r_amo_refresh["access_token"]
        data["refresh_token"] = r_amo_refresh["refresh_token"]
        data["date_time_refresh"] = str(datetime.datetime.now())
        with open(f"{os.path.dirname(__file__)}\\token", "w") as file_out:
            json.dump(data, file_out)
        access_token = data["access_token"]
        refresh_token = data["refresh_token"]
        print("New access amoCRM:")
        print(r_amo_refresh)
    # проверка и обновление токенов для доступа к amoCRM конец

    # получение и валидация данных начало

    # получение контакта из амо по номеру телефона начало
    r_amo_contact = rq.get("https://meb290.amocrm.ru/api/v4/contacts",
                           headers={"Authorization": f"Bearer {access_token}"},
                           params={
                               "query": "9115629907"
                           }
                           ).json()

    df_amo_contact = pd.DataFrame.from_dict(r_amo_contact["_embedded"]["contacts"])[['id', 'name', 'first_name', 'last_name', 'responsible_user_id']]

    i = 0
    contact_list = []
    for contact in r_amo_contact["_embedded"]["contacts"]:
        j = 0
        for value_contact in r_amo_contact["_embedded"]["contacts"][i]["custom_fields_values"][j]["values"]:
            contact_list.append("".join(c for c in value_contact['value'] if c.isdecimal())[1:])
            j += 1
        i += 1
    df_amo_contact = df_amo_contact.join(pd.DataFrame(contact_list), lsuffix='', rsuffix='_join')
    df_amo_contact = df_amo_contact.rename(columns={0: "phone_num"})

    # получение контакта из амо по номеру телефона конец

    dict_dataframe = dataframe.T.to_dict()
    for i in range(0, 656, 1):
        print(i)
        tel_num = dict_dataframe[i]['client']
        r_amo_contact_i = rq.get("https://meb290.amocrm.ru/api/v4/contacts",
                               headers={"Authorization": f"Bearer {access_token}"},
                               params={"query": f"{str(tel_num)[1:]}"}
                               )

        if r_amo_contact_i.status_code == 200:
            dict_dataframe[i]["amoCRM_client"] = "yes"
        else:
            dict_dataframe[i]["amoCRM_client"] = "no"
    df_amo_megafon = pd.DataFrame.from_dict(dict_dataframe).T
    print(df_amo_megafon[["UID", "Type", "client", "amoCRM_client"]])
    # получение и валидация данных конец
    pass


# получение списка покупателей по салону из 1С
def get_source_1c():
    pass


def main():
    get_source_amocrm(get_megafon_source("history", "yesterday", "out"))
    pass


if __name__ == "__main__":
    main()