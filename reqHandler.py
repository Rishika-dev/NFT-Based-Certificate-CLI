import requests
from yaspin import yaspin
import os
from dotenv import load_dotenv
from ipfsUpload import uploadImage

load_dotenv()

backend_url = os.getenv("BACKEND_URL")


class ReqHandler:
    def __init__(self):
        self.url = backend_url
        self.header = {}

    def login(self, username, password):
        with yaspin(text="Logging In", color="green") as spinner:
            try:
                token = requests.post(self.url + "/login", json={
                    "username": username,
                    "password": password
                })
                self.header = {
                    "authorization": token.json()["token"]
                }
                spinner.ok("✔")
                return token.json()
            except:
                spinner.fail("✖")
                return False

    def sendCertificateDetails(self, title, firstName, lastName, gender, dob, mob, yob, doi, moi, yoi, walletAddress, cid, uid):

        response = requests.post(self.url + "/certificate",
                                 json={"title": title,
                                       "firstName": firstName,
                                       "lastName": lastName,
                                       "gender": gender,
                                       "dateOfBirth": dob,
                                       "monthOfBirth": mob,
                                       "yearOfBirth": yob,
                                       "dateOfIssue": doi,
                                       "monthOfIssue": moi,
                                       "yearOfIssue": yoi,
                                       "walletAddress": walletAddress,
                                       "imageCID": cid,
                                       "uniqueId": uid}
                                 )

    def getCertificateDetails(self, tokenId):

        response = requests.get(
            backend_url + "/certificate/details/" + tokenId)
        if(response.status_code == 200):
            return response.json()
        else:
            raise Exception ("Certificate not found")

    def modifyCertificateDetails(self, tokenId, title, firstName, lastName, gender, dob, mob, yob, doi, moi, yoi, walletAddress, cid, uid):
        response = requests.put(
            backend_url + "/certificate/edit/",
            json={"tokenId": tokenId,
                "title": title,
                  "firstName": firstName,
                  "lastName": lastName,
                  "gender": gender,
                  "dateOfBirth": dob,
                  "monthOfBirth": mob,
                  "yearOfBirth": yob,
                  "dateOfIssue": doi,
                  "monthOfIssue": moi,
                  "yearOfIssue": yoi,
                  "walletAddress": walletAddress,
                  "imageCID": cid,
                  "uniqueId": uid
            }   
        )

    def burnCertificate(self, tokenId):
        response = requests.delete(
            backend_url + "/certificate/burn/" + tokenId)
