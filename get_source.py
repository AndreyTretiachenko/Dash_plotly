import requests as rq
import pandas as pd
import datetime
import json
#import time
import os
from progress_bar import InitBar


def get_amo_users():
    with open(f"{os.path.join(os.path.dirname(__file__), 'token')}", "r", encoding="utf-8") as file_in:
        data = json.load(file_in)
    access_token = data["access_token"]
    r_amo_users = rq.get("https://meb290.amocrm.ru/api/v4/users",
                         headers={"Authorization": f"Bearer {access_token}"},
                         params={"limit": "300"}).json()
    return r_amo_users


def get_all_contact():
    df_contacts = pd.DataFrame()
    with open(f"{os.path.join(os.path.dirname(__file__), 'token')}", "r", encoding="utf-8") as file_in:
        data = json.load(file_in)
    access_token = data["access_token"]
    step = 1
    print(f"Начало: {datetime.datetime.now()}")
    rq.session()
    while True:
        r_temp = rq.get(f"https://meb290.amocrm.ru/api/v4/contacts",
                        headers={"Authorization": f"Bearer {access_token}"},
                        params={
                            "page": f"{step}",
                            "limit": "250"
                            #"filter[responsible_user_id]": f"{id_user}",
                        }
                        )
        if r_temp.status_code == 200:
            r_temp_json = r_temp.json()
            df_contacts_temp = pd.DataFrame.from_dict(r_temp_json["_embedded"]["contacts"])
            df_contacts = pd.concat([df_contacts, df_contacts_temp], ignore_index=True)
            step += 1
            print(f"Page {step} loaded")
        else:
            print(f"\nКонтакты закончились. Страниц контактов: {step}")
            break
    print(f"\nКонец: {datetime.datetime.now()}")
    return df_contacts


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
    with open(f"{os.path.join(os.path.dirname(__file__), 'token')}", "r", encoding="utf-8") as file_in:
        data = json.load(file_in)
    access_token = data["access_token"]
    refresh_token = data["refresh_token"]


    print(rq.get("https://meb290.amocrm.ru/api/v4/account", headers={"Authorization": f"Bearer {access_token}"}).text)
    if rq.get("https://meb290.amocrm.ru/api/v4/account", headers={"Authorization": f"Bearer {access_token}"}).status_code == 200:
        print("access OK")
    else:
        r_amo_refresh_query = rq.post("https://meb290.amocrm.ru/oauth2/access_token",
                                      json={
                                          "client_id": "ecb8ec97-98c3-4fd1-9777-a9935113974f",
                                          "client_secret": "JscDfuHoUTwLR8V5gkHMYIDdfXBQUHsgaXDx7Jv5yAZt3LgJKfkbm8Hsmkd0jQF6",
                                          "grant_type": "refresh_token",
                                          "refresh_token": f"{refresh_token}",
                                          "redirect_uri": "https://mail.ru"
                                      },
                                      headers={"Content-Type": "application/json"})
        print("access FALSE")
        print(r_amo_refresh_query)
        r_amo_refresh = r_amo_refresh_query.json()
        data["access_token"] = r_amo_refresh["access_token"]
        data["refresh_token"] = r_amo_refresh["refresh_token"]
        data["date_time_refresh"] = str(datetime.datetime.now())
        with open(f"{os.path.join(os.path.dirname(__file__), 'token')}", "w", encoding="utf-8") as file_out:
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

    df_amo_contact = pd.DataFrame.from_dict(
        r_amo_contact["_embedded"]["contacts"])[['id', 'name', 'first_name', 'last_name', 'responsible_user_id']]

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
    print(f"Начало: {datetime.datetime.now()}")
    bar = InitBar(title="Запрос в amoCRM", size=len(dict_dataframe), offset=0)
    for i in range(0, len(dict_dataframe), 1):
        bar(i)
        tel_num = dict_dataframe[i]['client']
        r_amo_contact_i = rq.get("https://meb290.amocrm.ru/api/v4/contacts",
                                 headers={"Authorization": f"Bearer {access_token}"},
                                 params={"query": f"{str(tel_num)[1:]}"})
        if r_amo_contact_i.status_code == 200:
            dict_dataframe[i]["amoCRM_client"] = "yes"
            r_amo_contact_i_json = r_amo_contact_i.json()
            dict_dataframe[i]["Link_amoCRM"] = f"https://meb290.amocrm.ru/contacts/detail/{r_amo_contact_i_json['_embedded']['contacts'][0]['id']}"
        else:
            dict_dataframe[i]["amoCRM_client"] = "no"
            dict_dataframe[i]["Link_amoCRM"] = "no link"

    print(f"\nКонец: {datetime.datetime.now()}")
    df_amo_megafon = pd.DataFrame.from_dict(dict_dataframe).T
    return df_amo_megafon


    # получение и валидация данных конец
    pass


# получение списка покупателей по салону из 1С
def get_source_1c():
    pass


def main():
    pass


if __name__ == "__main__":
    main()