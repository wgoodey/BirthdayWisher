from data import login
from datetime import datetime
import smtplib
import os
import random
import csv

EMAIL = login.email
PASSWORD = login.password
LETTERS_DIRECTORY = 'data/letters/'
PLACEHOLDER = "[NAME]"
this_month = datetime.now().month
today = datetime.now().day

try:
    with open("data/birthdays.csv") as file:
        reader = csv.DictReader(file)
        all_birthdays = [row for row in reader]

except FileNotFoundError:
    print("birthdays.csv file could not be found.")

else:
    for contact in all_birthdays:
        if int(contact["month"]) == this_month and int(contact["day"]) == today:

            # pick a random form letter
            try:
                path = f"{LETTERS_DIRECTORY}{random.choice(os.listdir(LETTERS_DIRECTORY))}"
            except FileNotFoundError:
                os.makedirs(LETTERS_DIRECTORY)
                print("The 'data/letters' directory could not be located, so one was was created. "
                      "Place form letters in this directory and try again.")
            except IndexError:
                print("The 'data/letters' directory is empty. Place some form letters in the directory and try again.")

            else:
                # read form letter
                with open(path) as letter:
                    message = letter.read()
                # check that the letter is formatted with a name placeholder
                if PLACEHOLDER not in message:
                    print(f"Letter {path} should be formatted with {PLACEHOLDER} in place of the recipient's name.")
                else:
                    # insert contact's name
                    message = message.replace(PLACEHOLDER, contact["name"])
                    # send email
                    with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
                        connection.starttls()
                        connection.login(user=EMAIL, password=PASSWORD)
                        connection.sendmail(from_addr=EMAIL,
                                            to_addrs=contact["email"],
                                            msg=f"To: {contact['email']}\nSubject: Happy Birthday\n\n{message}")
