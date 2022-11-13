import requests


class imageTagging():
    def __init__(self, API_KEY, API_SECRET):
        self.API_KEY = API_KEY
        self.API_SECRET = API_SECRET
        self.IMAGE_URL = IMAGE_URL

    def tagging_obj(self, IMAGE_URL):
        response = requests.get(
            'https://api.imagga.com/v2/tags?image_url=%s' % IMAGE_URL,
            auth=(self.API_KEY, self.API_SECRET))

        tags = response.json()['result']['tags']
        for tag in tags:
            confidence = tag['confidence']
            tag_name = tag['tag']['en']
            print(f'Confidence: {confidence}, tag: {tag_name}')
            
        return tag_name, confidence


API_KEY = 'acc_de10f3569b04ef6'
API_SECRET = 'b1728fcb6d7f5a9ad0824c8e354e0817'
IMAGE_URL = 'https://wallpapercave.com/wp/wp3503654.jpg'

tag_name, confidence = imageTagging(API_KEY, API_SECRET).tagging_obj(IMAGE_URL)
print(tag_name, confidence)

# print(image.tagging_obj())
