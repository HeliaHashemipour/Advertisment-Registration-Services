from RabbitMQ import RabbitMQ_Send
message = "48.jpg"
(RabbitMQ_Send().send(message))


import requests


# DOMAIN = "sandbox2c66c8ba08704e23ba2ee5a08e0eb08a.mailgun.org"
# API_KEY = "91d1efd9903f3dd0c627b3bc30c341e8-2de3d545-1257bc0e"
# EMAIL_ADDRESS = "heliahashemipour@aut.ac.ir"
# TEXT = "Your ad has been accepted!"
# SUBJECT = "Cloud Computing HW1"

# # get YOUR_DOMAIN_NAME and YOUR_API_KEY from Mailgun dashboard
# def send_simple_message(email, subject, text):
# 	return requests.post(
# 		f"https://api.mailgun.net/v3/{DOMAIN}/messages",
# 		auth=("api", API_KEY),
# 		data={"from": f"<mailgun@{DOMAIN}>",
# 			"to": [email],
# 			"subject": subject,
# 			"text": text})

# response = send_simple_message(EMAIL_ADDRESS, SUBJECT, TEXT)
# print(response.json())