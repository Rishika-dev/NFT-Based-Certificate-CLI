import requests

def uploadImage(image):
    # Enter your Pinata API keys here
    PINATA_API_KEY = 'd90c28d26dede747c963'
    PINATA_SECRET_API_KEY = 'a3f259cd366e8782f5d5310f745483f9a1963afa9ed665807c66122f6c5d858f'

    # Enter the file path and name of the image you want to upload
    IMAGE_FILE_PATH = 'image'
    IMAGE_FILE_NAME = f'{image}.png'

    # Set the Pinata API endpoint
    PINATA_ENDPOINT = 'https://api.pinata.cloud/pinning/pinFileToIPFS'

    # Set the headers for the API request
    headers = {
        'pinata_api_key': PINATA_API_KEY,
        'pinata_secret_api_key': PINATA_SECRET_API_KEY,
    }

    # Set the data for the API request
    data = {
        'file': (IMAGE_FILE_NAME, open('./'+IMAGE_FILE_PATH +'/'+ IMAGE_FILE_NAME, 'rb')),
    }

    # Make the API request
    response = requests.post(PINATA_ENDPOINT, headers=headers, files=data)

    # Print the cid of the uploaded image
    return response.json()['IpfsHash']
