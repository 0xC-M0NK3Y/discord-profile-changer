import requests
import base64
import sys
import random
import json
from bs4 import BeautifulSoup
from io import BytesIO
from PIL import Image
import os
import uuid
from tls_client import Session

"""

	Usage: profile_changer.py <profiles.json>

	Updates your discord profile with a random profile of the profiles.json

	Set your username to name
	Set your bio to bio
	Set your pronouns to pronouns

	For the picture, it searchs on google image the picture field
	and takes a random image as your profile picture

"""

def get_image_from_google(picture):
        url = f'https://www.google.com/search?client=firefox-b-e&q={picture}&tbm=isch&source=lnms'
        r = requests.get(url)
        soup = BeautifulSoup(r.text, "html.parser")
        rand = random.randint(0, len(soup.find_all('img'))-1)
        i = 0
        for imgs in soup.find_all("img"):
                if i >= rand:
                        img = imgs.get('src')
                        r = requests.get(img)
                        if r.status_code == 200:
                                break  
                i += 1

        if r.headers['Content-Type'] == 'image/jpeg':
                print("in jpeg:", r.headers['Content-Length'])
                tmp = Image.open(BytesIO(r.content))
                fname = str(uuid.uuid1)+".jpg"
                tmp.save(fname)
                with open(fname, "rb") as fp:
                        img_base64 = base64.b64encode(fp.read())
                        os.remove(fname)
        elif r.headers['Content-Type'] == 'image/png':
                print("In png")
                img_base64 = base64.b64encode(r.text.encode())
        else:
                # not often
                print("Image format not supported")
                exit(1)
        return img_base64
                
def main():

        if len(sys.argv) != 2:
                print(f'Usage {sys.argv[0]} <profiles.json>')
                exit(1)

        with open(sys.argv[1], 'r') as f:
                profiles = json.load(f)

        rand = random.randint(0, len(profiles['profiles'])-1)
        prof = profiles['profiles'][rand]

        avatar = f"data:image/png;base64,{get_image_from_google(prof['picture']).decode()}"
                
        data_1 = {"pronouns": prof['pronouns'],
                  "bio": prof['bio']}
        data_2 = {"avatar": avatar,
                  "global_name": prof['name']}

        url_1 = "https://discord.com/api/v9/users/%40me/profile" # pour commentaires
        url_2 = "https://discord.com/api/v9/users/@me" # pour photo et nom

        # Dump with your navigator the headers
        headers = {
                "Method": "PATCH",
                "Scheme": "https",
                'Host': 'discord.com',
                #'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0',
                'Accept': '*/*',
                'Accept-Language': 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3',
                'Accept-Encoding': 'gzip, deflate, br',
                'Content-Type': 'application/json',
                'Authorization': '<your token>',
                'X-Super-Properties': 'eyJvcyI6IkxpbnV4IiwiYnJvd3NlciI6IkZpcmVmb3giLCJkZXZpY2UiOiIiLCJzeXN0ZW1fbG9jYWxlIjoiZnIiLCJicm93c2VyX3VzZXJfYWdlbnQiOiJNb3ppbGxhLzUuMCAoWDExOyBMaW51eCB4ODZfNjQ7IHJ2OjEwOS4wKSBHZWNrby8yMDEwMDEwMSBGaXJlZm94LzExNS4wIiwiYnJvd3Nlcl92ZXJzaW9uIjoiMTE1LjAiLCJvc192ZXJzaW9uIjoiIiwicmVmZXJyZXIiOiJodHRwczovL3d3dy5nb29nbGUuY29tLyIsInJlZmVycmluZ19kb21haW4iOiJ3d3cuZ29vZ2xlLmNvbSIsInNlYXJjaF9lbmdpbmUiOiJnb29nbGUiLCJyZWZlcnJlcl9jdXJyZW50IjoiaHR0cHM6Ly9kaXNjb3JkLmNvbS8iLCJyZWZlcnJpbmdfZG9tYWluX2N1cnJlbnQiOiJkaXNjb3JkLmNvbSIsInJlbGVhc2VfY2hhbm5lbCI6InN0YWJsZSIsImNsaWVudF9idWlsZF9udW1iZXIiOjI4MDIzMSwiY2xpZW50X2V2ZW50X3NvdXJjZSI6bnVsbH0=',
                'X-Discord-Locale': 'fr',
                'X-Discord-Timezone': 'Europe/Paris',
                'X-Debug-Options': 'bugReporterEnabled',
                # 'Content-Length': '729659',
                'Origin': 'https://discord.com',
                'Alt-Used': 'discord.com',
                'Connection': 'keep-alive',
                # 'Cookie': '',
                'Sec-Fetch-Dest': 'empty',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Site': 'same-origin',
                'Pragma': 'no-cache',
                'Cache-Control': 'no-cache',
                'TE': 'trailers',
        }

        # bypass captcha
        ses = Session(client_identifier="chrome_115", random_tls_extension_order=True)
        
        r = ses.patch(url_1, headers=headers, json=data_1)
        print(f'Status 1 = {r.status_code}')
        r = ses.patch(url_2, headers=headers, json=data_2)
        print(f'Status 2 = {r.status_code}')
        

if __name__ == '__main__':
        main()
