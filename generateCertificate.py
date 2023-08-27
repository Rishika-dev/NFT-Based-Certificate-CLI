from PIL import Image, ImageFont, ImageDraw
from ipfsUpload import uploadImage
import os
import requests
from io import BytesIO
import qrcode_terminal 

baseURI = os.getenv("baseURI")

def generateCertificate(title, firtName, lastName, walletAddress, gender, dob, mob, yob, doi, moi, yoi, uid):
        my_image = Image.open("./images/Final.png").convert("RGBA")
        title_font = ImageFont.truetype('Courgette-Regular.ttf', 200)
        date_font = ImageFont.truetype('Courgette-Regular.ttf', 80)
        image_editable = ImageDraw.Draw(my_image)
        width, height = my_image.size
        dateOfIssue = f"{doi}/{moi}/{yoi}"
        certificateTitle = title
        image_editable.text(
            (width/2, 1150), f"{firtName} {lastName}", (0, 0, 0), font=title_font, anchor="mm")
        image_editable.text((1122, 1800), dateOfIssue,
                            (0, 0, 0), font=date_font)
        image_editable.text((1544, 737), certificateTitle,
                            (0, 0, 0), font=date_font)  
        qr = generateQR(uid)
        my_image.paste(qr, (2290, 1688))
        if not os.path.exists("./image"):
            os.makedirs("./image")
        my_image.save("./image/result2.png")
        cid = uploadImage("result2")
        print("\n")
        qrcode_terminal.draw(f"{baseURI}{uid}")
        return cid


def generateQR(uid):
    url = "https://qrcode3.p.rapidapi.com/qrcode/text"
    payload = {
        "data": f"{baseURI}{uid}",
        "style": {
            "module": {
                "color": "#D169B5",
                "shape": "sieve"
            },
            "inner_eye": {"shape": "right_eye",
                          "color": "#1877F2"},
            "outer_eye": {"shape": "right_eye",
                          "color": "#489EAB"},
            "background": {}
        },
        "size": {
            "width": 400,
            "quiet_zone": 4,
            "error_correction": "M"
        },
        "output": {
            "filename": "qrcode",
            "format": "png"
        }
    }
    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": "d919db8a15mshad38dcadb7cf1a0p1593c9jsndc733f74531e",
        "X-RapidAPI-Host": "qrcode3.p.rapidapi.com"
    }

    response = requests.request("POST", url, json=payload, headers=headers)
    return Image.open(BytesIO(response.content))
