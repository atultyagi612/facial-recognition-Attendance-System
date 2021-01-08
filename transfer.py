from datetime import date
from tkinter import messagebox

import gspread
import os.path
import xlsxwriter
from oauth2client.service_account import ServiceAccountCredentials

name = str(date.today())


def trans():
    if os.path.isfile(f'Backup/{name}.xlsx') == False:
        scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
                 "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_name('testSheets-9c1b98942881.json', scope)
        client = gspread.authorize(creds)
        sheet = client.open('fullbuster').sheet1
        messagebox.showinfo('Wait', 'please wait....')

        try:
            data = sheet.get_all_records()
            workbook = xlsxwriter.Workbook(f'Backup/{name}.xlsx')
            worksheet = workbook.add_worksheet()

            for row in range(1, len(data)):
                worksheet.write(row, 1, data[row]['Id'])
                worksheet.write(row, 2, data[row]['name'])
                worksheet.write(row, 3, data[row]['time'])
                worksheet.write(row, 4, data[row]['date'])

            workbook.close()

            sheet.delete_rows(2, len(data) + 2)
            messagebox.showinfo('Complete', 'Transfer complete ')
        except Exception as e:
            print(e)
    else:
        messagebox.showinfo('Error', 'Today backup is already present')
