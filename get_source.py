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
    #if rq.get("https://meb290.amocrm.ru/api/v4/account", headers = {"Authorization": f"Bearer {r_amo_access_token}"}, params = {}).status_code == 400:

    r_amo = rq.post("https://meb290.amocrm.ru/oauth2/access_token",
                        json={
                            "client_id": "ecb8ec97-98c3-4fd1-9777-a9935113974f",
                            "client_secret": "JscDfuHoUTwLR8V5gkHMYIDdfXBQUHsgaXDx7Jv5yAZt3LgJKfkbm8Hsmkd0jQF6",
                            "grant_type": "authorization_code",
                            "code": "def502003f3f81ff39d8489805dddb42020a9cb0441b889b195f22882fa5a55d1fa21d2e5e931923d292307b3972db73011effa27ac60ce8d58d5d88aea8cd288eb02feaea1222d3c99b3609a0ed162628c91849c474bb1988ed96bd0806c44c438ac1349bcdc214e2d0a09f90225ea66fbbdb52009054ec618b6c77b7288c82e035662ec96d7079ee3d5e1af54287145232cc9b760c06e3f58a7698a43c46bb9f02b7e1eb6d1282f0b0ae0ed83f845d7a2f69cf290836af9e2da21572fbd2b8fc4de5b101d8f48bb28324f59dffc111ea21c9451c3e6c37ba1751741be02695f65b1f0a92b78cdc84910e52360df7213c5a2addff5c095012a3edd4e15f82f68ef2885d11ce260f15cc3c74b0be190125a548a0d66ae3fffde2393538517215a74ffb1d41717a46a418a612b6d159fb1a084f0a8d810aa15772e43dee6d57bbdd9a81e4c41219e071eb8a2952bba0bb69efef8a51cd71bf95bd7ecd99307ae5c228b3b600142bb12fe4ac33ee9482bd713a352d7df7037ff8b18d0748e326e05b206fa494a1c2ad826ba8c782a56e5995da22d483d7eb78bf051466db1600f132007f61147f4f7890dca9af72ef64d5fab8bebb90a26c6fe2",
                            "redirect_uri": "https://mail.ru"
                        },
                        headers={"Content-Type": "application/json"}
                        )
    #r_amo_refresh = rq.post("https://meb290.amocrm.ru/oauth2/access_token",
                            #json={
                                #"client_id": "ecb8ec97-98c3-4fd1-9777-a9935113974f",
                                #"client_secret": "JscDfuHoUTwLR8V5gkHMYIDdfXBQUHsgaXDx7Jv5yAZt3LgJKfkbm8Hsmkd0jQF6",
                                #"grant_type": "refresh_token",
                                #"refresh_token": "def5020062676b3e6f3a327abc9f8e863a7b1b01f8fc3b35377e918df5ae2e3f4fa77e1985b220909c3f2a80a99ce0131c841ebe0134293581c7bb4d0888d126d891bcbb94a997baddb85972aea495c523e09cfd57298c808e0ccda5955a7d7d7213a462495f74d97d7d7682a6675b259b7dd1334dbdd806d61f3db667f12db6b56445adfd775a8454af03c452e5ced3133aeacce166c0547555f8f53813441a36d9202131c3bc91c9af334370b44158a80247b56534740f0b61414f47a807f644a35e80d1e8b2e068c9f6f56bb72f5eae0d36aeb0e3f4b282b9dfbbad952a1b2d1cfba9f31b5caf4abc953d485b1a61ee8715f2ae2a16c00056cc6bd248ec2e0f98e9671f0378b90d14d39ef42d61f32fa49c7b74e53caa2717352990c36de0146b68bc88837140ad98fa422db421d0f83b0369007ae6d3d8a628666355178d5f620b4ff06dbcfd8b3a02f333eafb0677e5ec52edf1768f1c0458f8528c19f7ff13ed8a34df712251720f4bbf3e45e3e595e9a0d4e6f53c500955e715ed57dfcc69d053075ecb5101a84115553e35ae87b514253ab73f33431de4d7839c0b6c281e57dbfc652faa709ca1b1cf17ef48d017adbd2e94078ad2",
                                #"redirect_uri": "https://mail.ru"
                            #},
                            #headers={"Content-Type": "application/json"}
                            #)
    print(r_amo.text)
    pass


# получение списка покупателей по салону из 1С
def get_source_1c():
    pass


def main():
    get_source_amocrm()
    pass


if __name__ == "__main__":
    main()