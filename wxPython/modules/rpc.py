from configparser import ConfigParser
from pypresence import Presence
from modules.yandexmusic import MYAPI
import time
import pymem
from pymem.ptypes import RemotePointer
from pymem.process import module_from_name


config = ConfigParser()
config.read('info/config.ini')


class MRPC:
    dRPC = Presence(client_id=config.get('main', 'ds'))

    dRPC.connect()

    def getPointerAddress(self, base, offsets, pm):
        remote_pointer = RemotePointer(pm.process_handle, base)
        for offset in offsets:
            if offset != offsets[-1]:
                remote_pointer = RemotePointer(pm.process_handle, remote_pointer.value + offset)
        return remote_pointer.value + offsets[-1]

    def musicTime(self, pm, gameModule):
        return [
            pm.read_double(MRPC().getPointerAddress(gameModule + 0x012C0BC8, [0x38, 0x10, 0xC0, 0x410, 0xEA8], pm)) * (
                    pm.read_double(MRPC().getPointerAddress(gameModule + 0x012C0BC8, [0x40, 0x38, 0x70], pm)) / 100),
            pm.read_double(MRPC().getPointerAddress(gameModule + 0x012C0BC8, [0x38, 0x10, 0xC0, 0x410, 0xEA8], pm))]

    def Clear(self):
        self.dRPC.clear()

    def mywavePresence(self):
        self.dRPC.update(
            details="Моя волна",
            large_image="https://github.com/maj0roff/YandexMusicDiscordRPC/raw/main/fallback-black_2.gif",
            small_image="https://github.com/maj0roff/YandexMusicDiscordRPC/blob/main/logo.png?raw=true",
            large_text=f"На своей волне"
        )

    def updatePresence(self, aritst, song, image_link, song_link, song_time=None, lyrics=None, time_switch=False):
        # from main import change_button
        if lyrics is not None:
            btns = [
                {
                    "label": "Слушать",
                    "url": song_link
                },
                {
                    "label": "Текст",
                    "url": lyrics
                }
            ]
        else:
            btns = [
                {
                    "label": "Слушать",
                    "url": song_link
                }
            ]
        if song_time is not None:
            self.dRPC.update(
                details=f"{aritst} - {song}",
                large_image=image_link,
                small_image="https://github.com/maj0roff/YandexMusicDiscordRPC/blob/main/logo.png?raw=true",
                large_text=f"{aritst} - {song}",
                buttons=btns,
                end=time.time() + song_time
            )
        elif time_switch:
            self.dRPC.update(
                details=f"{aritst} - {song}",
                state="Пауза",
                large_image=image_link,
                small_image="https://github.com/maj0roff/YandexMusicDiscordRPC/blob/main/logo.png?raw=true",
                large_text=f"{aritst} - {song}",
                buttons=btns,
            )
        else:
            self.dRPC.update(
                details=f"{aritst} - {song}",
                large_image=image_link,
                small_image="https://github.com/maj0roff/YandexMusicDiscordRPC/blob/main/logo.png?raw=true",
                large_text=f"{aritst} - {song}",
                buttons=btns,
            )

    def callPresence(self, queue):
        switch = 0
        lasttrack = 0
        song_time_switch = 0
        song_time_check = 0
        data = queue.get()
        time_switch = data[0]
        text_switch = data[1]
        update = data[2]
        while True:
            try:
                if not queue.empty():
                    data = queue.get()
                    time_switch = data[0]
                    text_switch = data[1]
                    update = data[2]
                if update != 1:
                    api = MYAPI()
                    songid = api.songID()
                    artist = api.songArtist()
                    song = api.songTitle()
                    image_link = api.songImage()
                    song_link = api.songLink()
                    if time_switch == 1:
                        pm = pymem.Pymem("Y.Music.exe")
                        gameModule = module_from_name(pm.process_handle, "Y.Music.dll").lpBaseOfDll
                        song_time = self.musicTime(pm, gameModule)
                        if song_time_check != song_time[0]:
                            if song_time_switch == 1:
                                song_time_switch = 0
                                if text_switch == 1:
                                    self.updatePresence(artist, song, image_link, song_link,
                                                        song_time=song_time[1] - song_time[0],
                                                        lyrics=api.text(artist, song), time_switch=time_switch)
                                else:
                                    self.updatePresence(artist, song, image_link, song_link,
                                                        song_time=song_time[1] - song_time[0], time_switch=time_switch)
                            elif song_time[0] - song_time_check > 4:
                                if text_switch == 1:
                                    self.updatePresence(artist, song, image_link, song_link,
                                                        song_time=song_time[1] - song_time[0],
                                                        lyrics=api.text(artist, song), time_switch=time_switch)
                                else:
                                    self.updatePresence(artist, song, image_link, song_link,
                                                        song_time=song_time[1] - song_time[0], time_switch=time_switch)
                            song_time_check = song_time[0]
                        else:
                            song_time_switch = 1
                            if text_switch == 1:
                                self.updatePresence(artist, song, image_link, song_link, lyrics=api.text(artist, song),
                                                    time_switch=time_switch)
                            else:
                                self.updatePresence(artist, song, image_link, song_link, time_switch=time_switch)
                    if songid != lasttrack:
                        lasttrack = songid
                        switch = 1
                    if switch == 1:
                        switch = 0
                        try:
                            if time_switch == 1 and text_switch == 0:
                                pm = pymem.Pymem("Y.Music.exe")
                                gameModule = module_from_name(pm.process_handle, "Y.Music.dll").lpBaseOfDll
                                songtime = self.musicTime(pm, gameModule)
                                self.updatePresence(artist, song, image_link, song_link,
                                                    song_time=songtime[1] - songtime[0], time_switch=time_switch)
                            elif text_switch == 1 and time_switch == 0:
                                self.updatePresence(artist, song, image_link, song_link, lyrics=api.text(artist, song),
                                                    time_switch=time_switch)
                            elif text_switch == 1 and time_switch == 1:
                                pm = pymem.Pymem("Y.Music.exe")
                                gameModule = module_from_name(pm.process_handle, "Y.Music.dll").lpBaseOfDll
                                songtime = self.musicTime(pm, gameModule)
                                self.updatePresence(artist, song, image_link, song_link,
                                                    song_time=songtime[1] - songtime[0],
                                                    lyrics=api.text(artist, song), time_switch=time_switch)
                            else:
                                self.updatePresence(artist, song, image_link, song_link, time_switch=time_switch)
                        except Exception as e:
                            if text_switch == 1:
                                self.updatePresence(artist, song, image_link, song_link, lyrics=api.text(artist, song),
                                                    time_switch=time_switch)
                            else:
                                self.updatePresence(artist, song, image_link, song_link, time_switch=time_switch)
                else:
                    update = 0
                    api = MYAPI()
                    artist = api.songArtist()
                    song = api.songTitle()
                    image_link = api.songImage()
                    song_link = api.songLink()
                    try:
                        if time_switch == 1 and text_switch == 0:
                            pm = pymem.Pymem("Y.Music.exe")
                            gameModule = module_from_name(pm.process_handle, "Y.Music.dll").lpBaseOfDll
                            songtime = self.musicTime(pm, gameModule)
                            self.updatePresence(artist, song, image_link, song_link,
                                                song_time=songtime[1] - songtime[0], time_switch=time_switch)
                        elif text_switch == 1 and time_switch == 0:
                            self.updatePresence(artist, song, image_link, song_link, lyrics=api.text(artist, song),
                                                time_switch=time_switch)
                        elif text_switch == 1 and time_switch == 1:
                            pm = pymem.Pymem("Y.Music.exe")
                            gameModule = module_from_name(pm.process_handle, "Y.Music.dll").lpBaseOfDll
                            songtime = self.musicTime(pm, gameModule)
                            self.updatePresence(artist, song, image_link, song_link,
                                                song_time=songtime[1] - songtime[0],
                                                lyrics=api.text(artist, song), time_switch=time_switch)
                        else:
                            self.updatePresence(artist, song, image_link, song_link, time_switch=time_switch)
                    except Exception as e:
                        if text_switch == 1:
                            self.updatePresence(artist, song, image_link, song_link, lyrics=api.text(artist, song),
                                                time_switch=time_switch)
                        else:
                            self.updatePresence(artist, song, image_link, song_link, time_switch=time_switch)
            except Exception as e:
                print(e)
                self.mywavePresence()
            time.sleep(0.01)
