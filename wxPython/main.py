from configparser import ConfigParser
import webbrowser
import traceback
import sys
import platform
from multiprocessing import Process, Queue
if len(config.get("main", "ym")) <= 2:
    messagebox.showinfo("[Яндекс Музыка]", "[Яндекс Музыка] Установка необходимых пакетов.")
    os.system('pip install yandex-music --upgrade')
    os.system('pip install pypresence')
    os.system('pip install pyqt6==6.5.0')
    os.system('pip install pymem')
    os.system('pip install wxPython==4.2.1')
config = ConfigParser()
config.read('info/config.ini')
import wx
from pypresence.exceptions import DiscordNotFound
from tkinter import messagebox

try:
    from wx import App, Frame, Menu, MenuItem, Icon, MessageDialog, OK, ICON_INFORMATION
    from wx.adv import TaskBarIcon
    from wx.html2 import WebView
    from modules.rpc import MRPC
    from modules.yandexmusic import MYAPI
except DiscordNotFound:
    dlg = MessageDialog(None, "[Яндекс Музыка]", "Сначала откройте Discord!", OK | ICON_INFORMATION)
    dlg.ShowModal()
    dlg.Destroy()
    sys.exit()
except Exception as e:
    with open('error.txt', 'w') as f:
        f.write(str(traceback.format_exc()))
    messagebox.showerror("[Яндекс Музыка]",
                         "[Яндекс Музыка] Замечен первый запуск программы, пожалуйста авторизируйтесь в следующем окне.")
    sys.exit()

linux = False
if "linux" in platform.system().lower():
    linux = True
q = Queue()
text_switch = 0
time_switch = 0
update = 0
text_button = None


class BrowserFrame(Frame):
    def __init__(self):
        super().__init__(None, title="Яндекс Музыка RPC", size=(298, 237),
                         style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER)
        self.SetIcon(Icon("assets/favicon.png"))

        panel = wx.Panel(self)
        self.ID_MENU_ITEM_GITHUB = wx.NewIdRef()
        self.ID_MENU_ITEM_OPEN_WINDOW = wx.NewIdRef()
        self.ID_MENU_ITEM_EXIT = wx.NewIdRef()
        wx.Log.SetActiveTarget(wx.LogStderr())

        self.checkBox = wx.CheckBox(panel, label="Включить DiscordRPC", pos=(16, 16))
        self.checkBox.Bind(wx.EVT_CHECKBOX, self.AppEnabling)

        self.checkBox_2 = wx.CheckBox(panel, label="Включить отображение времени трека", pos=(16, 46))
        self.checkBox_2.Bind(wx.EVT_CHECKBOX, self.TimeSwitch)

        self.checkBox_3 = wx.CheckBox(panel, label="Включить кнопку текста песни (если есть)", pos=(16, 76))
        self.checkBox_3.Bind(wx.EVT_CHECKBOX, self.TextSwitch)

        self.pushButton = wx.Button(panel, label="Обновить токен Яндекс Музыки", pos=(16, 110))
        self.pushButton.SetSize((250, 35))
        self.pushButton.Bind(wx.EVT_BUTTON, self.ForceUpdateToken)

        self.pushButton_2 = wx.Button(panel, label="Выход из приложения", pos=(16, 150))
        self.pushButton_2.SetSize((250, 35))
        self.pushButton_2.Bind(wx.EVT_BUTTON, self.fullexit)

        self.tray_icon = wx.adv.TaskBarIcon()
        self.tray_icon.SetIcon(Icon("assets/favicon.png"), "Яндекс Музыка | DiscordRPC")
        self.tray_icon.Bind(wx.adv.EVT_TASKBAR_LEFT_DOWN, self.tray_icon_activated)
        self.tray_icon.Bind(wx.adv.EVT_TASKBAR_RIGHT_DOWN, self.tray_right_click)
        self.Bind(wx.EVT_MENU, self.OnMenuItemSelected, id=self.ID_MENU_ITEM_GITHUB)
        self.Bind(wx.EVT_MENU, self.OnMenuItemSelected, id=self.ID_MENU_ITEM_OPEN_WINDOW)
        self.Bind(wx.EVT_MENU, self.OnMenuItemSelected, id=self.ID_MENU_ITEM_EXIT)

        self.Bind(wx.EVT_CLOSE, self.OnClose)

    def CreatePopupMenu(self):
        menu = wx.Menu()
        menu.Append(self.ID_MENU_ITEM_GITHUB, "Перейти на гитхаб")
        menu.Append(self.ID_MENU_ITEM_OPEN_WINDOW, "Показать")
        menu.AppendSeparator()
        menu.Append(self.ID_MENU_ITEM_EXIT, "Выход")
        return menu

    def OnMenuItemSelected(self, event):
        menu_id = event.GetId()
        match menu_id:
            case self.ID_MENU_ITEM_GITHUB:
                webbrowser.open("https://github.com/KycTik31/YMD-plus")
            case self.ID_MENU_ITEM_OPEN_WINDOW:
                self.tray_icon_activated("event")
            case self.ID_MENU_ITEM_EXIT:
                self.fullexit("event")

    def tray_right_click(self, event):
        self.PopupMenu(self.CreatePopupMenu())

    def tray_icon_activated(self, event):
        self.Show()

    def AppEnabling(self, event):
        if self.checkBox.GetValue():
            global thr
            thr = Process(target=MRPC().callPresence, args=(q,))
            thr.start()
            q.put([time_switch, text_switch, update])
        else:
            thr.terminate()
            MRPC().Clear()

    def TimeSwitch(self, event):
        global time_switch
        global update
        update = 1
        if self.checkBox_2.GetValue():
            time_switch = 1
        else:
            time_switch = 0
        q.put([time_switch, text_switch, update])
        update = 0

    def TextSwitch(self, event):
        global text_switch
        global update
        update = 1
        if self.checkBox_3.GetValue():
            text_switch = 1
        else:
            text_switch = 0
        q.put([time_switch, text_switch, update])
        update = 0

    def ForceUpdateToken(self, event):
        MYAPI().ForceUpdateToken()

    def fullexit(self, event):
        global ISTOEXITBLYAT
        ISTOEXITBLYAT = True
        try:
            thr.terminate()
        except NameError:
            pass
        finally:
            sys.exit()

    def OnClose(self, event):
        self.Hide()
        self.tray_icon.ShowBalloon("Яндекс Музыка | DiscordRPC", "Приложение свернуто в трей")

    def open_text(self, event):
        if text_button:
            webbrowser.open(text_button, new=2)
        else:
            webbrowser.open('https://github.com/KycTik31/YMD-plus', new=2)


if __name__ == '__main__':
    app = App()

    frame = BrowserFrame()
    frame.Show()

    app.MainLoop()
