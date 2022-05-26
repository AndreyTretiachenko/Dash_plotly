from get_source import get_source_amocrm
from get_source import get_megafon_source, send_email
import pandas as pd
import matplotlib.pyplot as plt
import datetime


def save_excel(dataframe1, dataframe2, dataframe3, name, sheets):
    try:
        writer_excel = pd.ExcelWriter(f"{name}.xlsx")
        dataframe1.to_excel(writer_excel, startrow=0, sheet_name=sheets[0])
        dataframe2.to_excel(writer_excel, startrow=0, sheet_name=sheets[1])
        dataframe3.to_excel(writer_excel, startrow=0, sheet_name=sheets[2])
        for i in sheets:
            worksheet = writer_excel.sheets[i]  # pull worksheet object
            worksheet.set_column(5, 5, 20)  # set column width
            worksheet.set_column(4, 4, 45)  # set column width
            worksheet.set_column(0, 0, 7)  # set column width
            worksheet.set_column(3, 3, 13)  # set column width
            worksheet.set_column(2, 2, 10)  # set column width
            worksheet.set_column(1, 1, 15)  # set column width
            worksheet.set_column(6, 6, 35)  # set column width
        writer_excel.save()
        send_email("meb290@mail.ru", "meb290@mail.ru", "Аналитика по подозрительным звонкам", "Аналитика")
        return True
    except:
        return False


def creattable_plotlib(dataframe, name):
    fig, ax = plt.subplots()
    fig.patch.set_visible(False)
    plt.axis('off')
    plt.axis('tight')
    the_table = plt.table(cellText=dataframe.values, colLabels=dataframe.columns, loc='center')
    the_table.auto_set_column_width(col=list(range(len(dataframe.columns))))
    the_table.auto_set_font_size(False)
    the_table.set_fontsize(12)
    return plt.savefig(f"{name}.png")


def main():
    # настройки отображения таблицы в консоле
    pd.set_option('display.max_rows', 500)
    pd.set_option('display.max_columns', 500)
    pd.set_option('display.width', 1000)

    # запрос данных аккаунтов из мегафона
    account = get_megafon_source("accounts", "", "")
    print(datetime.datetime.today().date())
    data_sort_yesterday = get_source_amocrm(
        get_megafon_source("history", "yesterday", "out")[['client', 'Type']].groupby("client",
                                                                                      as_index=False).count().sort_values(
            "Type", ascending=False).query('Type > 3'))[['client', 'Type', 'amoCRM_client', 'Link_amoCRM', 'Name', 'User']].query(
        'Link_amoCRM != "no link"').head(20)

    data_sort_thisweek = get_source_amocrm(
        get_megafon_source("history", "this_week", "out")[['client', 'Type']].groupby("client",
                                                                                  as_index=False).count().sort_values(
            "Type", ascending=False).query('Type > 5'))[['client', 'Type', 'amoCRM_client', 'Link_amoCRM', 'Name', 'User']].query(
        'Link_amoCRM != "no link"').head(20)

    data_sort_lastweek = get_source_amocrm(
        get_megafon_source("history", "last_week", "out")[['client', 'Type']].groupby("client",
                                                                                  as_index=False).count().sort_values(
            "Type", ascending=False).query('Type > 5'))[['client', 'Type', 'amoCRM_client', 'Link_amoCRM', 'Name', 'User']].query(
        'Link_amoCRM != "no link"').head(20)
    print(save_excel(data_sort_yesterday, data_sort_thisweek, data_sort_lastweek, f"amo_scan {datetime.datetime.today().date()}", ["yesterday", "thisweek", "lastweek"]))


if __name__ == "__main__":
    main()