import requests
import smtplib
from re import sub
from lxml import html
from datetime import datetime
from email.message import EmailMessage


#Habilitar e-mail exclusivo para envios
#https://myaccount.google.com/lesssecureapps?pli=1&rapt=AEjHL4PQ6f4Osoyephe_UyNn--TxxzD1YvbhXCor_Rj1un5BK13srDEV9V0wOo_vmsEc1yDPRGdMoW3lrsGNZdB4PH_JPx6Lwg

def fetchCoinValue():
    urls = {
        "usd": {
            "url": "https://economia.awesomeapi.com.br/all/USD-BRL",
            "value": 0
        },
        "bcoin": {
            "url": "https://coinmarketcap.com/currencies/bombcrypto/",
            "value": 0
        },
        "spg": {
            "url": "https://coinmarketcap.com/currencies/space-crypto/",
            "value": 0
        }
    }


    requisicao = requests.get("https://economia.awesomeapi.com.br/all/USD-BRL")
    cotacao = requisicao.json()

    dolar = 0

    for coin in urls:
        url = urls[coin]["url"]
        response = requests.get(url)

        if(coin == "usd"):
            mainValue = float(requisicao.json()["USD"]["bid"])        
            dolar = urls[coin]["value"] = round(mainValue, 2)
            #urls[coin]["value"] = round(1 / mainValue, 2)
        else:
            htmlTree = html.fromstring(response.content)
            mainValue = htmlTree.xpath("//div[@class='priceValue ']//text()")[0]

            mainValue = float(mainValue.replace("$", "")) * dolar

            urls[coin]["value"] = round(mainValue, 2)

    return urls


def getEmailMessage(urls):
    msg = EmailMessage()
    msg["Subject"] = "Cotação Atual de Moedas - Lista de Favoritos"
    msg["From"] = "rodrigocezarleao@gmail.com"
    msg["To"] = "rodrigoczleo@yahoo.com.br"
    

    now = datetime.now()
    currentTime = now.strftime("%d/%m/%Y, %H:%M:%S")

    message = f"Cotação de '{currentTime}'\n\n"

    for coin in urls:
        value = urls[coin]["value"]
        message += f"{coin.upper()} - Cotação Atual: R$ {value} \n\n"

    msg.set_content(message)
    return msg


def sendEmailMessage():
    urls = fetchCoinValue()
    msg = getEmailMessage(urls)
    user = "rodrigocezarleao@gmail.com"
    password = "#Bradydekonoha97"
    
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(user, password)
        smtp.send_message(msg)
        

sendEmailMessage()