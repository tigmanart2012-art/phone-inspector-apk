from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.utils import platform
import os, zipfile, random, string, platform as py_platform, psutil
from datetime import datetime

if platform == "android":
    from android.permissions import request_permissions, Permission
    from jnius import autoclass

class Inspector(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation="vertical", **kwargs)
        self.data = ""

        self.add_widget(Label(text="📱 Phone Inspector (локально)", size_hint_y=None, height=70))

        self.output = TextInput(readonly=True)
        self.add_widget(self.output)

        self.pass_input = TextInput(
            hint_text="Пароль ZIP (пусто = случайный)",
            password=True,
            size_hint_y=None,
            height=70
        )
        self.add_widget(self.pass_input)

        self._btn("🔐 Запросить разрешения", self.ask_permissions)
        self._btn("🔍 Получить данные", self.collect_data)
        self._btn("💾 Сохранить TXT", self.save_txt)
        self._btn("🔒 Сохранить ZIP", self.save_zip)

    def _btn(self, text, cb):
        b = Button(text=text, size_hint_y=None, height=70)
        b.bind(on_press=cb)
        self.add_widget(b)

    # --- permissions ---
    def ask_permissions(self, _):
        if platform == "android":
            request_permissions([
                Permission.READ_EXTERNAL_STORAGE,
                Permission.WRITE_EXTERNAL_STORAGE,
                Permission.READ_PHONE_STATE,
            ])
            self.output.text += "\n✔ Разрешения запрошены\n"
        else:
            self.output.text += "\n⚠ Не Android\n"

    # --- data ---
    def collect_data(self, _):
        info = []
        info += [
            f"Дата: {datetime.now()}",
            f"OS: {py_platform.system()}",
            f"Python: {py_platform.python_version()}",
            f"Machine: {py_platform.machine()}",
            f"Processor: {py_platform.processor()}",
            f"CPU cores: {psutil.cpu_count(logical=True)}",
            f"RAM total: {round(psutil.virtual_memory().total / (1024**3), 2)} GB",
            f"RAM free: {round(psutil.virtual_memory().available / (1024**3), 2)} GB",
            f"Disk total: {round(psutil.disk_usage('/').total / (1024**3), 2)} GB",
            f"Disk free: {round(psutil.disk_usage('/').free / (1024**3), 2)} GB",
        ]

        if platform == "android":
            Build = autoclass("android.os.Build")
            info += [
                f"Brand: {Build.BRAND}",
                f"Model: {Build.MODEL}",
                f"Device: {Build.DEVICE}",
                f"Android SDK: {Build.VERSION.SDK_INT}",
                f"Android Release: {Build.VERSION.RELEASE}",
            ]

        self.data = "\n".join(info)
        self.output.text = self.data

    # --- save ---
    def save_txt(self, _):
        with open("info.txt", "w", encoding="utf-8") as f:
            f.write(self.data)
        self.output.text += "\n\n✔ info.txt сохранён"

    def save_zip(self, _):
        pwd = self.pass_input.text.strip()
        if not pwd:
            pwd = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(10))

        with zipfile.ZipFile("info.zip", "w", zipfile.ZIP_DEFLATED) as z:
            z.writestr("info.txt", self.data)

        self.output.text += f"\n\n✔ info.zip создан\n🔑 Пароль: {pwd}"

class AppMain(App):
    def build(self):
        return Inspector()

if __name__ == "__main__":
    AppMain().run()
