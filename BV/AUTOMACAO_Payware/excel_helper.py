import pandas as pd
from openpyxl import load_workbook
from datetime import date
import os

table_path = os.environ["TABLE_PATH"]


def init(email_table):
    try:
        with pd.ExcelFile(table_path, engine='openpyxl') as reader:
            print(reader)
            table = reader.parse(table_path)
        
        homolog_table = pd.read_excel(table_path)
        target_table_name = list(homolog_table)[-1]
        target_table = homolog_table[target_table_name].copy(deep=True)

        print(email_table)
        print(target_table)

        target_table["Conta"] = email_table["Conta"]
        target_table["CdProduto"] = email_table["CdProduto"]

        return target_table
    except Exception as e:
        print(e)
        return False


def save(target_table):
    date_today = date.today().strftime("%d/%m/%Y").replace("/", "-")

    with pd.ExcelWriter(table_path, engine='openpyxl') as writer:
        book = load_workbook(table_path)
        writer.book = book
        sheets_list = book.worksheets
        writer.sheets = dict((ws.title, ws) for ws in sheets_list)

        target_table.to_excel(writer, sheet_name=(
            f"{date_today}" + "(0)"), header=True)

        writer.save()
