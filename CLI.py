from art import *
from rich.console import Console
from InquirerPy import inquirer
from reqHandler import ReqHandler
from InquirerPy.base.control import Choice
from generateCertificate import generateCertificate
from termcolor import colored
from yaspin import yaspin
from pyfiglet import Figlet as pyg
import uuid
import qrcode_terminal
import os

baseURI = os.getenv("baseURI")

# NFT Based Certification System
# Rishika Sharma
console = Console()
reqHandler = ReqHandler()
username = password = None


def getGender(genderId):
    if genderId == 0:
        return "Male"
    elif genderId == 1:
        return "Female"
    else:
        return "Other"


def greeting():
    # console.print(text2art("NFT", font="banner3-d"), style="bold red")
    # console.print(text2art("Rishika Sharma", font="small"), style="bold red")
    projectName = pyg(font="slant", width=100, justify="center")
    print(colored(projectName.renderText(
        "NFT based certification system"), "blue", attrs=["bold"]))
    creator = pyg(font="slant", width=100, justify="center")
    print(colored(creator.renderText(
        "Rishika Sharma"), "yellow", attrs=["bold"]))


def login():
    global username, password
    console.print("Please Login", style="bold green")
    username = inquirer.text(message="Enter Username").execute()
    password = inquirer.secret(message="Enter Password").execute()
    if (user := reqHandler.login(username, password)):
        console.print("Logged In", style="bold green")
        console.print("Welcome", username, user['email'], style="bold green")
    else:
        console.print("Invalid Credentials", style="bold red")
        login()


def selectMenu():
    option = inquirer.select(
        message="Select an option for NFT certificate:",
        choices=[Choice(name="Generate", value='generate'), Choice(name="Modify", value='modify'), Choice(
            name="View", value='view'), Choice(name="Burn", value='burn'), Choice(name="Exit", value='exit')]
    ).execute()
    if option == 'generate':
        generate()
    elif option == 'modify':
        modify()
    elif option == 'view':
        view()
    elif option == 'burn':
        burn()
    elif option == 'exit':
        exit()


def generate():

    print("Generate")
    title = inquirer.text(message="Enter Certificate Title").execute()
    first_name = inquirer.text(message="Enter First Name").execute()
    last_name = inquirer.text(message="Enter Last Name").execute()
    genderSelect = inquirer.select(
        message="Select your gender:",
        choices=["Male", "Female", "Other"]
    ).execute()
    if genderSelect == "Male":
        gender = 0
    elif genderSelect == "Female":
        gender = 1
    else:
        gender = 2

    dob = inquirer.text(message="Enter Date of Birth(DD)").execute()
    mob = inquirer.text(message="Enter Month of Birth(MM)").execute()
    yob = inquirer.text(message="Enter Year of Birth(YYYY)").execute()

    doi = inquirer.text(message="Enter Date of Issue(DD)").execute()
    moi = inquirer.text(message="Enter Month of Issue(MM)").execute()
    yoi = inquirer.text(message="Enter Year of Issue(YYYY)").execute()
    walletAddress = inquirer.text(message="Enter Wallet Address").execute()

    print("Certificate Details:")
    print(f"Title: {title}")
    print(f"Recipient Name: {first_name} {last_name}")
    print(f"Gender: {getGender(gender)}")
    print(f"Date of Birth: {dob}-{mob}-{yob}")
    print(f"Date of Issue: {doi}-{moi}-{yoi}")
    print(f"Wallet Address: {walletAddress}")   

    confirm = inquirer.confirm(
        message="Do you want to generate the certificate?").execute()
    uid = uuid.uuid4().hex
    with yaspin(text="Generating Certificate Information", color="green") as spinner:
        try:
            cid = generateCertificate(
                title, first_name, last_name, walletAddress, gender, dob, mob, yob, doi, moi, yoi, uid)
            spinner.ok("✔ ")

        except:
            spinner.fail("✖ ")
    with yaspin(text="Saving Certificate", color="green") as spinner:
        try:
            reqHandler.sendCertificateDetails(
                title, first_name, last_name, gender, dob, mob, yob, doi, moi, yoi, walletAddress, cid, uid)
            spinner.ok("✔ ")

        except:
            spinner.fail("✖ ")
    if not confirm:
        generate()


def modify():
    tokenId = inquirer.text(message="Enter Token ID").execute()
    print("Modify")

    try:
        with yaspin(text="Fetching Certificate", color="green") as spinner:
            # certificate = reqHandler.getCertificate(tokenId)
            certificateData = reqHandler.getCertificateDetails(tokenId)
            spinner.ok("✔ Certificate Fetched ")

        title = inquirer.text(
            'Title', default=f"{certificateData[0]}").execute()
        firstName = inquirer.text(
            'First Name', default=f"{certificateData[1]}").execute()
        lastName = inquirer.text(
            'Last Name', default=f"{certificateData[2]}").execute()
        genderSelect = inquirer.select(
            message="Select your gender:",
            choices=["Male", "Female", "Other"],
            default=f"{getGender(certificateData[9])}"
        ).execute()
        if genderSelect == "Male":
            gender = 0
        elif genderSelect == "Female":
            gender = 1
        else:
            gender = 2        
        dob = inquirer.text(
            'Date of Birth', default=f"{certificateData[3]}").execute()
        dom = inquirer.text(
            'Month of Birth', default=f"{certificateData[4]}").execute()
        doy = inquirer.text(
            'Year of Birth', default=f"{certificateData[5]}").execute()
        doi = inquirer.text(
            'Date of Issue', default=f"{certificateData[6]}").execute()
        moi = inquirer.text(
            'Month of Issue', default=f"{certificateData[7]}").execute()
        yoi = inquirer.text(
            'Year of Issue', default=f"{certificateData[8]}").execute()
        with yaspin(text="Generating Certificate Information", color="green") as spinner:
            cid = generateCertificate(
                title, firstName, lastName, certificateData[12], gender, dob, dom, doy, doi, moi, yoi, certificateData[11])
            reqHandler.modifyCertificateDetails(tokenId,title,firstName,lastName,gender,dob,dom,doy,doi,moi,yoi,certificateData[12],cid, certificateData[11])
            spinner.ok("✔ ")


    except Exception as e:
        print(e)
        spinner.fail("✖")

def view():

    tokenId = inquirer.text(message="Enter Token ID").execute()
    with yaspin(text="Fetching Certificate", color="green") as spinner:
        try:
            # certificate = reqHandler.getCertificate(tokenId)
            certificateData = reqHandler.getCertificateDetails(tokenId)
            spinner.ok("✔ Certificate Fetched ")
            print()
            print('Certificate title: ', certificateData[0],colored('✔', 'green'))
            print('First Name: ', certificateData[1])
            print('Last Name: ', certificateData[2])
            print('Gender: ', getGender(certificateData[9]))         
            print('Month of Birth: ', certificateData[4])
            print('Year of Birth: ', certificateData[5])
            print('Date of Issue: ', certificateData[6])
            print('Month of Issue: ', certificateData[7])
            print('Year of Issue: ', certificateData[8])
            # print(getGender(certificateData[9]))
            print('IPFS Hash: ', certificateData[10])
            print('Unique Id: ', certificateData[11])
            print('Wallet Address: ', certificateData[12])
            print()
            qrcode_terminal.draw(f"{baseURI}{certificateData[11]}")

        except Exception as e:
            spinner.fail("✖")
            print("Certificate not found")


def burn():
    print("Burn")
    tokenId = inquirer.text(message="Enter Token ID").execute()
    with yaspin(text="Burning Certificate", color="green") as spinner:
        try:
            reqHandler.burnCertificate(tokenId)
            spinner.ok("✔ Certificate Burned ")

        except:
            spinner.fail("✖ ")


def exit():
    # print(exit)
    console.print(
        "Thank you for using NFT Based Certification System", style="bold green")
    quit()


def main():
    greeting()
    login()
    while(1):
        selectMenu()


main()
