from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.list import MDList, OneLineIconListItem
from kivymd.uix.button import MDFloatingActionButton
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.textfield import MDTextField
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.label import MDLabel
from kivy.clock import Clock

from telethon import TelegramClient
import asyncio, threading, os

# =========================
# CONFIG (GANTI PUNYAMU)
# =========================
API_ID = 33093687
API_HASH = "e675d1248205231bea20c9124ccb26f7"
BOT_TOKEN = "8241686007:AAGxvxZo5-nQ3KVwVdnGzqTz41PGJA8PhQA"
CHANNEL_ID = -1003738287444

# =========================
# TELEGRAM CLIENT
# =========================
client = TelegramClient('app', API_ID, API_HASH).start(bot_token=BOT_TOKEN)

# =========================
# MAIN UI
# =========================
class MainScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.layout = MDBoxLayout(orientation='vertical')

        # TOP BAR
        self.toolbar = MDTopAppBar(
            title="TG Cloud Pro",
            right_action_items=[
                ["refresh", lambda x: self.load_files()]
            ]
        )
        self.layout.add_widget(self.toolbar)

        # SEARCH
        self.search = MDTextField(
            hint_text="Search file...",
            size_hint_x=1
        )
        self.search.bind(text=self.filter_files)
        self.layout.add_widget(self.search)

        # FILE LIST
        self.scroll = MDScrollView()
        self.list_view = MDList()
        self.scroll.add_widget(self.list_view)
        self.layout.add_widget(self.scroll)

        # FLOAT BUTTON
        self.fab = MDFloatingActionButton(
            icon="upload",
            pos_hint={"center_x": .9, "center_y": .1}
        )
        self.fab.bind(on_press=self.upload_files)

        self.add_widget(self.layout)
        self.add_widget(self.fab)

        self.files_cache = []
        self.load_files()

    # =========================
    # LOAD FILES
    # =========================
    def load_files(self):
        self.list_view.clear_widgets()
        self.list_view.add_widget(MDLabel(text="Loading..."))
        threading.Thread(target=self._load_files).start()

    def _load_files(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        files = loop.run_until_complete(self.get_files())
        self.files_cache = files

        def update_ui():
            self.show_files(files)

        Clock.schedule_once(lambda dt: update_ui())

    async def get_files(self):
        data = []
        async for msg in client.iter_messages(CHANNEL_ID):
            if msg.file:
                data.append(msg)
        return data

    # =========================
    # DISPLAY FILES
    # =========================
    def show_files(self, files):
        self.list_view.clear_widgets()

        for msg in files[:100]:
            item = OneLineIconListItem(text=msg.file.name)
            item.bind(on_press=lambda x, m=msg: self.download(m))
            self.list_view.add_widget(item)

    # =========================
    # SEARCH FILTER
    # =========================
    def filter_files(self, instance, text):
        filtered = [
            f for f in self.files_cache
            if text.lower() in f.file.name.lower()
        ]
        self.show_files(filtered)

    # =========================
    # UPLOAD
    # =========================
    def upload_files(self, instance):
        threading.Thread(target=self._upload).start()

    def _upload(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        path = "/storage/emulated/0/Download"

        for f in os.listdir(path):
            file_path = os.path.join(path, f)
            try:
                loop.run_until_complete(
                    client.send_file(CHANNEL_ID, file_path)
                )
            except:
                pass

        Clock.schedule_once(lambda dt: self.load_files())

    # =========================
    # DOWNLOAD
    # =========================
    def download(self, msg):
        threading.Thread(target=self._download, args=(msg,)).start()

    def _download(self, msg):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(
            msg.download_media(file="/storage/emulated/0/Download/")
        )

# =========================
# APP
# =========================
class TGCloudApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.theme_style = "Dark"
        return MainScreen()

TGCloudApp().run()
