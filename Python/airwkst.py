"""
    Replaces the airwkst web app. Yay for efficiency. Heavily WIP
"""

import aiohttp
import asyncio
import re


class Airwkst:

    URL = "https://albert.rit.edu/iii/airwkst/"

    def __init__(self):
        self.session = None

    async def run(self):
        self.session = aiohttp.ClientSession()
        await self.main_loop()

    async def main_loop(self):
        while not asyncio.get_event_loop().is_closed():
            command = await asyncio.get_event_loop().run_in_executor(None, lambda: input("> ").lower())
            try:
                await self.commands[command](self)
            except Exception as e:
                print("Exception:")
                print(e.__class__.__name__, e)

    async def login(self):
        url = self.URL + "airwkstcore"
        async with self.session.get(url) as response:
            if response.status != 200:
                print("Something went wrong!")
                print(response.status)

        data = {
            "login": "",  # TODO: Load from file this and the next
            "loginpassword": "",
            "submit.x": 45,
            "submit.y": 16,
            "submit": "submit",
            "validationstatus": "needlogin",
            "action": "ValidateAirWkstUserAction",
            "nextaction": "null",
            "purpose": "null",
            "subpurpose": "null"
        }
        async with self.session.post(url, data=data) as response:
            if response.status != 200:
                print("Something went wrong!")
                print(response.status)

        data = {
            "initials": "",  # TODO: Load from file this and the next
            "initialspassword": "",
            "submit.x": 48,
            "submit.y": 20,
            "submit": "submit",
            "validationstatus": "needinitials",
            "action": "ValidateAirWkstUserAction",
            "nextaction": "null",
            "purpose": "null",
            "subpurpose": "null"
        }
        async with self.session.post(url, data=data) as response:
            if response.status != 200:
                print("Something went wrong!")
                print(response.status)

        async with self.session.get(self.URL + "?action=GetAirWkstUserInfoAction&purpose=updinvdt") as response:
            if response.status != 200:
                print("Something went wrong!")
                print(response.status)

    async def post_book(self):
        barcode = " "
        while barcode != "":
            barcode = await asyncio.get_event_loop().run_in_executor(None, lambda: input("SCAN > "))
            if not re.match(r"R\d+", barcode, flags=re.I):
                if barcode != "":
                    print("Invalid Barcode!")
                continue
            data = {
                "searchstring": barcode,
                "submitbutton.x": 0,
                "submitbutton.y": 0,
                "submitbutton": "submit",
                "sourcebrowse": "airwkstpage",
                "action": "GetAirWkstItemOneAction",
                "prevscreen": "AirWkstItemRequestPage",
                "searchtype": "b",
                "purpose": "updinvdt"
            }
            url = "?action=GetAirWkstUserInfoAction&purpose=updinvdt"
            async with self.session.post(self.URL + "airwkstcore", data=data) as response:
                print(await response.text())
                print(response.status)
                pass

    async def shelflist(self):
        url = self.URL + "airwkstcore?action=LoadAirWkstDisplayShelflistProgressPageAction&purpose=shelflist_s&searchtype=b"
        async with self.session.get(url) as response:
            fake_param = re.search(r"<input.*?\"fakeparametertopreventcacheing\".*?value=\"(.*?)\"/>", await response.text()).group(1)
        url = self.URL + "airwkstcore"
        data = {
            "action": "GetShelflistAction",
            "purpose": "shelflist_s",
            "searchtype": "b",
            "batchtimebeg": "null",
            "fakeparametertopreventcacheing": fake_param
        }
        async with self.session.post(url) as response:
            print(await response.text())
        # url = self.URL + "airwkstcore?action=CompareShelflistAction&purpose=shelflist_s"
        # async with self.session.get(url) as response:
        #     print(await response.text())

    commands = {"scan": post_book, "shelf": shelflist, "login": login}


def main():
    loop = asyncio.get_event_loop()

    airwkst = Airwkst()

    loop.create_task(airwkst.run())
    loop.run_forever()


if __name__ == "__main__":
    main()
