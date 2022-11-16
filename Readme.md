# Advertisment Registration Services
Cloud Computing's first assignment

In this project, you implement an ad registration service. The purpose of this exercise is to get to know and work with cloud services; You use these services for different parts of your service, such as "database", "object-based storage", "image processing" and "email sending".
Advertisements include all types of vehicles. Each user can send an advertisement of his vehicle in the form of a combination of text and image descriptions, along with his email address. Your service checks the registered ad in the first step. Each ad is placed in its corresponding category according to the type of vehicle in its image (car, motorcycle, bicycle, etc.). If the image contains
If there are no vehicles, the ad will be rejected. Finally, after processing the ad, the user will be notified of the result of his ad registration by sending an email. In this email, if the ad is approved, a link to the ad along with its category will be placed. If the ad is rejected, this will be mentioned in the email.

Your software consists of two services. The first service is responsible for receiving user requests and responding to them. The second service has the task of processing (determining the category or rejecting the ad).
First service
This service consists of two APIs.
- Ad registration API:
1. This API receives the information of an ad, including text, image, and sending email.
2. The information of this ad, including the text and email address of the sender, is stored in the database and a unique identifier is considered for it.
3. It stores the image in an object storage. We choose the name of the image in this storage so that we can retrieve the image of an ad based on its identifiers. 
4. Writes the ad ID for processing into the RabbitMQ queue. 
5. As a response to request 2, a message like "Your ad was registered with ID X" will be sent to the user.

- API to receive ads:
1. This API receives the ID of an ad. 
2. If the ID related to an ad is not checked, in response, a message like "Your ad is in the review queue" will be sent to the user. q
3. If the ID related to an ad is rejected, a message like "Your ad was not approved" will be given in response. 
4. If this ID corresponds to a verified ad, the information of this ad including text, image, category and status will be returned in the response.

Second service
The task of this service is to read ads from the RabbitMQ queue, process them and store the result in the database. 
1. This service is connected to the RabbitMQ queue and listens for new messages. Each message corresponds to a registered advertisement. 
2. Each message read from the queue contains an advertisement ID. With this ID, the ad photo is received from the object storage. 
3. The ad photo is sent to photo tagging service 4 for processing. From the response of the tagging service, the first tag is selected as the ad category. Put this category in the category column of the database. 
4. By using the email sending service, an email is sent to the user to inform the user of the status (approval or rejection) of his ad.

<img width="852" alt="1" src="https://user-images.githubusercontent.com/71961438/201540370-806d9d6b-5b7b-44bd-8b1a-1b33537e5d87.png">

I will name the cloud services used:
• For the cloud host, Abrarvan is used.
• I used Aiven for the database (mySQL).
• Other services were also used according to the agenda. Like RabbitMQ, Imagga and mailgun
• For the object storage, Abrarvan was also used, in which I made a bucket.


I returned the message Your post was submitted successfully with id.


When the ad is approved and we have a vehicle, if we ask for the ID, the required data and response image will be given. If you pay attention, I encoded the image to base64, and postman does not show the image and gives base64, which can be converted to an image using online converters.


For another code, the only thing I did was to take the photo in the form of a url, and in the output, the response that we get is the photo in the form of a url (the same url of our photo is in Abrarvan's dashboard) and the app.py and Proxies.py code has changed a bit. 

When the ad is not approved (I gave a photo of a turbine), the response we have is as follows.


The received email is as follows.

