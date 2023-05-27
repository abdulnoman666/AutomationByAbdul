# Python 3.8.0
import re
import imaplib
import email
import traceback

# -------------------------------------------------
#
# Utility to read email from Gmail Using Python
#
# ------------------------------------------------
SMTP_SERVER = "imap.gmail.com"
SMTP_PORT = 993


def read_email_from_gmail(email_username, email_password):
    try:
        mail = imaplib.IMAP4_SSL(SMTP_SERVER)
        mail.login(email_username, email_password)
        mail.select('inbox')

        data = mail.search(None, 'ALL')
        mail_ids = data[1]
        id_list = mail_ids[0].split()
        first_email_id = int(id_list[0])
        latest_email_id = int(id_list[-1])

        data = mail.fetch(str(latest_email_id), '(RFC822)')
        for response_part in data:
            arr = response_part[0]
            if isinstance(arr, tuple):
                msg = email.message_from_string(str(arr[1], 'utf-8'))
                msg = str(msg)
                p = re.compile("Your Login Authentication Code is: (.*)")
                result = p.search(msg)
                otp = result[1]
                return otp


    except Exception as e:
        traceback.print_exc()
        print(str(e))
