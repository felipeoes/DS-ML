import win32com.client
import pythoncom
import re
import os
import pandas as pd
from payware import set_table

target_subjects = ["Novo Behavior Cartões"]
email_table = None


class Handler_Class(object):
    def OnNewMailEx(self, receivedItemsIDs):
        for ID in receivedItemsIDs.split(","):
            mail = outlook.Session.GetItemFromID(ID)
            subject = mail.Subject
            html_body = mail.HTMLBody

            attachments = list(mail.Attachments)
            print(subject)

            try:
                splitted_subject = subject.split("-")[2]

                match = re.search(r"\d{3}.*", splitted_subject)

                if target_subjects[0] in subject and match:
                    print("Email encontrado!")

                    table_body = pd.read_html(
                        html_body, header=0)[0]
                    email_table = table_body

                    for attachment in attachments:
                        print(attachment.FileName)
                        attachment.SaveAsFile(os.path.join(
                            os.getcwd() + "/attachments", attachment.FileName))

                    set_table(email_table)
                    break
            except Exception as e:
                print(e)
                continue


ol = win32com.client.Dispatch("Outlook.Application")
outlook = win32com.client.DispatchWithEvents(
    "Outlook.Application", Handler_Class)

# loop infinito que verifica se tem novas mensagens
pythoncom.PumpMessages()
