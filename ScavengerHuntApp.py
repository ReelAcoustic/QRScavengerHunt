from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Color, RoundedRectangle
from kivy.utils import get_color_from_hex
from qr_scanner import scan_qr_code  # ✅ Real QR code scanner
import cv2
import numpy as np
import re  # ✅ Import regex module

objectives = [
    "Welcome to CRASH HQ.",
    "Near Hub City is our FOB, resupply inbound.",
    "We need new recruits, there's only one other bulldog in this town! Find him for additional personnel.",
    "Find the secret file, it should be somewhere information is stored on shelves!."
]

class RoundedBox(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            Color(*get_color_from_hex("#ffffffee"))
            self.rect = RoundedRectangle(radius=[20], pos=self.pos, size=self.size)
        self.bind(pos=self.update_rect, size=self.update_rect)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

class ScavengerHuntApp(App):
    def build(self):
        root = FloatLayout()

        with root.canvas.before:
            Color(*get_color_from_hex("#f0f0f0ff"))
            self.bg_rect = RoundedRectangle(pos=root.pos, size=root.size)
        root.bind(size=self.update_bg)

        mascot = Image(source='bulldog.png', size_hint=(.25, .25), pos_hint={'x': .02, 'y': .65})
        root.add_widget(mascot)

        dialog = Label(
            text="Hey! Let's start the hunt!",
            size_hint=(.6, .2),
            pos_hint={'x': .28, 'y': .7},
            halign='left',
            valign='middle',
            color=(0, 0, 0, 1),
            bold=True
        )
        dialog.bind(size=dialog.setter('text_size'))
        root.add_widget(dialog)

        card = RoundedBox(orientation='vertical',
                          padding=10,
                          spacing=10,
                          size_hint=(.9, .35),
                          pos_hint={'x': .05, 'y': .02})

        scroll = ScrollView(size_hint=(1, 1))

        self.objectives_label = Label(
            text="\n".join(f"[ ] {obj}" for obj in objectives),
            markup=True,
            size_hint=(1, None),
            halign='left',
            valign='top',
            color=(0, 0, 0, 1)
        )
        self.objectives_label.bind(texture_size=self.update_label_height)
        scroll.add_widget(self.objectives_label)
        card.add_widget(scroll)
        root.add_widget(card)

        scan_btn = Button(
            text="Scan QR Code",
            size_hint=(.5, .1),
            pos_hint={'center_x': .5, 'y': .4},
            background_color=get_color_from_hex("#4285F4"),
            color=(1, 1, 1, 1),
            font_size='20sp'
        )
        scan_btn.bind(on_press=self.real_scan)
        root.add_widget(scan_btn)

        self.dialog = dialog
        self.objectives = objectives
        self.completed = 0

        return root

    def update_label_height(self, *args):
        self.objectives_label.height = self.objectives_label.texture_size[1]
        self.objectives_label.text_size = (self.objectives_label.width, None)

    def update_bg(self, instance, value):
        self.bg_rect.pos = instance.pos
        self.bg_rect.size = instance.size

    def real_scan(self, instance):
        scanned = scan_qr_code()

        if scanned:
            match = re.search(r'(.*)ID=(\d+)$', scanned)
            if match:
                message, id_str = match.groups()
                oid = int(id_str)
                if oid < len(self.objectives):
                    self.objectives[oid] = f"[x] {self.objectives[oid]}"
                    self.dialog.text = f"Scanned: ID={oid} — Objective {oid + 1} complete!"
                else:
                    self.dialog.text = "ID is valid, but no matching objective."
            else:
                self.dialog.text = "Invalid QR format."

            self.objectives_label.text = "\n".join(self.objectives)
        else:
            self.dialog.text = "No QR code scanned."

if __name__ == '__main__':
    ScavengerHuntApp().run()
