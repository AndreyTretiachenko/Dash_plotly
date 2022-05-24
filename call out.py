from get_source import get_source_amocrm
from get_source import get_megafon_source
import pandas as pd

def main():
    pd.set_option('display.max_colwidth', None)
    account = get_megafon_source("accounts", "", "")
    print(account.columns)
    print(account[["realName", "telnum"]])
    data = get_megafon_source("history", "today", "out")
    print(data.columns)
    data_sort = get_source_amocrm(data[['client', 'Type']].groupby("client", as_index=False).count().sort_values("Type", ascending=False))
    print(data_sort[['client', 'Type', 'amoCRM_client', 'Link_amoCRM']].query('Link_amoCRM != "no link"').head(10))
    pass


if __name__ == "__main__":
    main()