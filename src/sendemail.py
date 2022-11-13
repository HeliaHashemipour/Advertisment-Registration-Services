import requests


class sendEmail():
    def __init__(self, DOMAIN, API_KEY, EMAIL_ADDRESS, TEXT, SUBJECT):
        self.DOMAIN = DOMAIN
        self.API_KEY = API_KEY
        self.EMAIL_ADDRESS = EMAIL_ADDRESS
        self.TEXT = TEXT
        self.SUBJECT = SUBJECT

    def send_simple_message(self, email, subject, text):
        return requests.post(
            f"https://api.mailgun.net/v3/{self.DOMAIN}/messages",
            auth=("api", self.API_KEY),
            data={"from": f"<mailgun@{self.DOMAIN}>",
                  "to": [email],
                  "subject": subject,
                  "text": text})

    def send_response(self):
        response = self.send_simple_message(
            self.EMAIL_ADDRESS, self.SUBJECT, self.TEXT)
        # print(response.json())
        return response.json()


DOMAIN = "sandbox946608aa307241419f0a093a1fdd500c.mailgun.org"
API_KEY = "818378731d5374cd733ec4f5c5abf6c4-48c092ba-a51fd35d"
EMAIL_ADDRESS = "heliahashemipour2@gmail.com"
TEXT = "Your ad has been accepted!"
SUBJECT = "Cloud Computing HW1"

email_response = sendEmail(
    DOMAIN, API_KEY, EMAIL_ADDRESS, TEXT, SUBJECT).send_response()

print(email_response)


# print(image.tagging_obj())
