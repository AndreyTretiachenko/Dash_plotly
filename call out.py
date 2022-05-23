from get_source import get_source_amocrm
from get_source import get_megafon_source
import pandas as pd

def main():
    account = get_megafon_source("accounts", "", "")
    print(account.columns)
    print(account[["realName", "telnum"]])
    data = get_source_amocrm(get_megafon_source("history", "today", "out"))
    #data = pd.read_csv("history_this_week_out.csv")
    print(data.columns)
    print(data[['Type', 'client']].groupby("client").count().sort_values("Type", ascending=False).head(20))
    pass


if __name__ == "__main__":
    main()