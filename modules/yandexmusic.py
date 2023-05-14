from configparser import ConfigParser
from yandex_music import Client
from modules.getToken import UpdateToken
import requests
import unicodedata
from tkinter import messagebox

config = ConfigParser()

config.read('info/config.ini')

if len(config.get("main", "ym")) <= 2:
    messagebox.showinfo("[Яндекс Музыка]", "[Яндекс Музыка] Замечен первый запуск программы, пожалуйста авторизируйтесь в следующем окне.")
    config.set("main", "ym", UpdateToken())
    print("[Яндекс Музыка] Успешный запуск")
    with open("info/config.ini", "w") as config_file:
        config.write(config_file)

    client = Client(config.get("main", "ym")).init()
else:
    print("[Яндекс Музыка] Успешный запуск")
    client = Client(config.get("main", "ym")).init()


class MYAPI:
    def __init__(self):
        self.lQ = client.queue(client.queues_list()[0].id)

    def ForceUpdateToken(self):
        config.set("main", "ym", UpdateToken())
        print("[Яндекс Музыка] Успешный запуск")
        with open("info/config.ini", "w") as config_file:
            config.write(config_file)

        client = Client(config.get("main", "ym")).init()

    def songTitle(self):
        last_track_id = self.lQ.get_current_track()
        last_track = last_track_id.fetch_track()
        return last_track.title

    def songArtist(self):
        lQid = self.lQ.get_current_track()
        last_track = lQid.fetch_track()
        return ', '.join(last_track.artists_name())

    def songLink(self):
        lQid = self.lQ.get_current_track()
        lQlt = lQid.fetch_track()
        return f"https://music.yandex.ru/album/{lQlt['albums'][0]['id']}/track/{lQlt['id']}/"

    def songID(self):
        return self.lQ.get_current_track()

    def songImage(self):
        lQid = self.lQ.get_current_track()
        lQlt = lQid.fetch_track()
        return "https://" + lQlt.cover_uri.replace("%%", "1000x1000")

    def text(self, artist: str, title: str):
        access_token = "PtMSJtYDeB_DPNGf9g7YQMi4-nEYPg4PZChoOJv7BUecFTkA4qCRfyZ50pibp81v"
        title = title.split('(', 1)[0].strip()
        title = title[:title.find('(')] + title[title.rfind(')') + 1:] if title.find(
            '(') != -1 and title.rfind(')') != -1 else title

        r = requests.get(f"http://api.genius.com/search?q={artist} {title}&access_token={access_token}")

        # pprint.pprint(r.json())
        for i in r.json()["response"]["hits"]:
            if "lyrics" not in i["result"]["url"]:
                ...
            elif "lyrics" in i["result"]["url"] and (title.lower().replace("ё", "e") in ''.join(
                    c for c in i["result"]["title"].lower() if unicodedata.category(c)[0] != 'C').replace("ё",
                                                                                                          "e").replace(
                "’", "'").replace("`", "'")) or (''.join(
                c for c in i["result"]["title"].lower() if
                unicodedata.category(c)[0] != 'C').replace("ё", "e") in title.lower().replace("ё", "e").replace("’",
                                                                                                                "'")):
                return i["result"]["url"]

        return None
