import os
import re
import json
import subprocess
import sys
import threading
from datetime import datetime
from groq import Groq
from tavily import TavilyClient

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.utils import get_color_from_hex
from kivy.clock import Clock

# ============================================================
#   J.A.R.V.I.S — APK EDITION
#   Built with Kivy + Groq + Tavily
# ============================================================

GROQ_KEY    = "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"
TAVILY_KEY  = "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"
MEMORY_FILE = "jarvis_memory.json"
USER_NAME   = "Fahad Khan"
CALL_NAME   = "Sir"
MAX_MEMORY  = 20

client = Groq(api_key=GROQ_KEY)
tavily = TavilyClient(api_key=TAVILY_KEY)

# ============================================================
#  MEMORY
# ============================================================

def load_memory():
    if os.path.exists(MEMORY_FILE):
        try:
            with open(MEMORY_FILE, "r") as f:
                return json.load(f)
        except:
            return []
    return []

def save_memory(history):
    with open(MEMORY_FILE, "w") as f:
        json.dump(history[-MAX_MEMORY:], f, indent=2)

def clear_memory():
    if os.path.exists(MEMORY_FILE):
        os.remove(MEMORY_FILE)
    return []

chat_history = load_memory()

# ============================================================
#  SPEAK
# ============================================================

def speak(text):
    clean = re.sub(r'[^\w\s.,!?\'"-]', '', text)
    os.system('pkill -f termux-tts-speak 2>/dev/null')
    os.system(f'termux-tts-speak -l en -v en-gb-x-gba-network -p 0.4 -r 0.9 "{clean}" &')

# ============================================================
#  APP PACKAGES
# ============================================================

APPS = {
    "whatsapp":      "com.whatsapp",
    "instagram":     "com.instagram.android",
    "facebook":      "com.facebook.katana",
    "twitter":       "com.twitter.android",
    "x":             "com.twitter.android",
    "tiktok":        "com.zhiliaoapp.musically",
    "snapchat":      "com.snapchat.android",
    "telegram":      "org.telegram.messenger",
    "discord":       "com.discord",
    "youtube":       "com.google.android.youtube",
    "gmail":         "com.google.android.gm",
    "maps":          "com.google.android.apps.maps",
    "chrome":        "com.android.chrome",
    "drive":         "com.google.android.apps.docs",
    "photos":        "com.google.android.apps.photos",
    "calendar":      "com.google.android.calendar",
    "translate":     "com.google.android.apps.translate",
    "play store":    "com.android.vending",
    "netflix":       "com.netflix.mediaclient",
    "spotify":       "com.spotify.music",
    "prime video":   "com.amazon.avod.thirdpartyclient",
    "hotstar":       "in.startv.hotstar",
    "zoom":          "us.zoom.videomeetings",
    "settings":      "com.android.settings",
    "calculator":    "com.android.calculator2",
    "clock":         "com.android.deskclock",
    "camera":        "com.android.camera2",
    "contacts":      "com.android.contacts",
    "phone":         "com.android.dialer",
    "messages":      "com.google.android.apps.messaging",
    "files":         "com.google.android.apps.nbu.files",
    "amazon":        "com.amazon.mShop.android.shopping",
    "flipkart":      "com.flipkart.android",
}

PAYMENT_APPS = [
    "paypal", "gpay", "google pay", "paytm", "phonepe",
    "bank", "payment", "transfer money", "send money"
]

def is_payment(name):
    return any(p in name.lower() for p in PAYMENT_APPS)

def find_package(name):
    name = name.lower().strip()
    if name in APPS:
        return APPS[name]
    for key, pkg in APPS.items():
        if name in key or key in name:
            return pkg
    return None

# ============================================================
#  DEVICE COMMANDS
# ============================================================

def open_app(name):
    if is_payment(name):
        return f"Payment apps are restricted for your security, {CALL_NAME}."
    pkg = find_package(name)
    if pkg:
        os.system(f"am start -a android.intent.action.MAIN -c android.intent.category.LAUNCHER -p {pkg} 2>/dev/null")
        return f"Opening {name.title()}, {CALL_NAME}."
    q = name.replace(" ", "+")
    os.system(f"am start -a android.intent.action.VIEW -d 'market://search?q={q}' 2>/dev/null")
    return f"Searching Play Store for {name}, {CALL_NAME}."

def close_app(name):
    pkg = find_package(name)
    if pkg:
        os.system(f"am force-stop {pkg} 2>/dev/null")
        return f"{name.title()} has been closed, {CALL_NAME}."
    return f"Could not find {name}, {CALL_NAME}."

def set_brightness(level):
    lvl = max(0, min(255, int(level)))
    os.system(f"settings put system screen_brightness {lvl} 2>/dev/null")
    os.system("settings put system screen_brightness_mode 0 2>/dev/null")
    return f"Brightness set to {int((lvl/255)*100)}%, {CALL_NAME}."

def wifi_on():
    os.system("svc wifi enable 2>/dev/null")
    return f"Wi-Fi enabled, {CALL_NAME}."

def wifi_off():
    os.system("svc wifi disable 2>/dev/null")
    return f"Wi-Fi disabled, {CALL_NAME}."

def data_on():
    os.system("svc data enable 2>/dev/null")
    return f"Mobile data enabled, {CALL_NAME}."

def data_off():
    os.system("svc data disable 2>/dev/null")
    return f"Mobile data disabled, {CALL_NAME}."

def bluetooth_on():
    os.system("svc bluetooth enable 2>/dev/null")
    return f"Bluetooth enabled, {CALL_NAME}."

def bluetooth_off():
    os.system("svc bluetooth disable 2>/dev/null")
    return f"Bluetooth disabled, {CALL_NAME}."

def dark_mode_on():
    os.system("cmd uimode night yes 2>/dev/null")
    return f"Dark mode activated, {CALL_NAME}."

def dark_mode_off():
    os.system("cmd uimode night no 2>/dev/null")
    return f"Dark mode deactivated, {CALL_NAME}."

def set_volume(level):
    lvl = max(0, min(15, int(level)))
    os.system(f"media volume --stream 3 --set {lvl} 2>/dev/null")
    return f"Volume set to {lvl}, {CALL_NAME}."

def take_screenshot():
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    os.system(f"screencap -p /sdcard/jarvis_{ts}.png 2>/dev/null")
    return f"Screenshot saved as jarvis_{ts}.png, {CALL_NAME}."

def get_battery():
    try:
        r = subprocess.run(["termux-battery-status"], capture_output=True, text=True, timeout=5)
        d = json.loads(r.stdout)
        return f"Battery is at {d.get('percentage','?')}%, status: {d.get('status','?')}, {CALL_NAME}."
    except:
        return f"Unable to read battery, {CALL_NAME}."

def get_time():
    now = datetime.now()
    return f"It is {now.strftime('%I:%M %p')}, {now.strftime('%A %B %d %Y')}, {CALL_NAME}."

def torch_on():
    os.system("termux-torch on 2>/dev/null")
    return f"Flashlight on, {CALL_NAME}."

def torch_off():
    os.system("termux-torch off 2>/dev/null")
    return f"Flashlight off, {CALL_NAME}."

def search_google(query):
    q = query.replace(" ", "+")
    os.system(f"am start -a android.intent.action.VIEW -d 'https://www.google.com/search?q={q}' 2>/dev/null")
    return f"Google search opened for {query}, {CALL_NAME}."

def search_youtube(query):
    q = query.replace(" ", "+")
    os.system(f"am start -a android.intent.action.VIEW -d 'https://www.youtube.com/results?search_query={q}' 2>/dev/null")
    return f"YouTube search opened for {query}, {CALL_NAME}."

def lock_screen():
    os.system("input keyevent 82 2>/dev/null")
    return f"Screen locked, {CALL_NAME}."

def press_home():
    os.system("input keyevent 3 2>/dev/null")
    return f"Going home, {CALL_NAME}."

def press_back():
    os.system("input keyevent 4 2>/dev/null")
    return f"Going back, {CALL_NAME}."

def battery_saver_on():
    os.system("settings put global low_power 1 2>/dev/null")
    return f"Battery saver enabled, {CALL_NAME}."

def battery_saver_off():
    os.system("settings put global low_power 0 2>/dev/null")
    return f"Battery saver disabled, {CALL_NAME}."

def dnd_on():
    os.system("cmd notification set_dnd priority 2>/dev/null")
    return f"Do Not Disturb enabled, {CALL_NAME}."

def dnd_off():
    os.system("cmd notification set_dnd off 2>/dev/null")
    return f"Do Not Disturb disabled, {CALL_NAME}."

# ============================================================
#  COMMAND ROUTER
# ============================================================

def parse_and_execute(text):
    t = text.lower().strip()

    for pat in [r"open (.+)", r"launch (.+)", r"go to (.+)"]:
        m = re.search(pat, t)
        if m:
            return True, open_app(m.group(1).strip())

    for pat in [r"close (.+)", r"kill (.+)"]:
        m = re.search(pat, t)
        if m:
            return True, close_app(m.group(1).strip())

    m = re.search(r"brightness (?:to )?(\d+)", t)
    if m:
        val = int(m.group(1))
        return True, set_brightness(int((val/100)*255) if val<=100 else val)
    if "full brightness" in t or "max brightness" in t:
        return True, set_brightness(255)
    if "auto brightness" in t:
        os.system("settings put system screen_brightness_mode 1 2>/dev/null")
        return True, f"Auto brightness on, {CALL_NAME}."

    if "wifi on" in t or "turn on wifi" in t:
        return True, wifi_on()
    if "wifi off" in t or "turn off wifi" in t:
        return True, wifi_off()
    if "data on" in t or "mobile data on" in t:
        return True, data_on()
    if "data off" in t or "mobile data off" in t:
        return True, data_off()
    if "bluetooth on" in t or "turn on bluetooth" in t:
        return True, bluetooth_on()
    if "bluetooth off" in t or "turn off bluetooth" in t:
        return True, bluetooth_off()
    if "dark mode on" in t:
        return True, dark_mode_on()
    if "dark mode off" in t or "light mode" in t:
        return True, dark_mode_off()
    if "dnd on" in t or "do not disturb on" in t:
        return True, dnd_on()
    if "dnd off" in t or "do not disturb off" in t:
        return True, dnd_off()
    if "battery saver on" in t:
        return True, battery_saver_on()
    if "battery saver off" in t:
        return True, battery_saver_off()
    if "flashlight on" in t or "torch on" in t:
        return True, torch_on()
    if "flashlight off" in t or "torch off" in t:
        return True, torch_off()
    if "lock screen" in t or "lock phone" in t:
        return True, lock_screen()
    if "go home" in t or "home screen" in t:
        return True, press_home()
    if "go back" in t or "press back" in t:
        return True, press_back()
    if "screenshot" in t:
        return True, take_screenshot()
    if "battery" in t:
        return True, get_battery()
    if "what time" in t or "current time" in t or "what day" in t:
        return True, get_time()

    m = re.search(r"volume (?:to )?(\d+)", t)
    if m:
        return True, set_volume(m.group(1))
    if "mute" in t:
        return True, set_volume(0)
    if "max volume" in t or "full volume" in t:
        return True, set_volume(15)

    m = re.search(r"(?:youtube|play on youtube)(?: for)? (.+)", t)
    if m:
        return True, search_youtube(m.group(1))
    m = re.search(r"(?:google|search for) (.+)", t)
    if m:
        return True, search_google(m.group(1))

    if any(w in t for w in ["clear memory", "reset memory", "forget everything"]):
        global chat_history
        chat_history = clear_memory()
        return True, f"Memory cleared, {CALL_NAME}. Starting fresh."

    return False, None

# ============================================================
#  WEB SEARCH + AI
# ============================================================

SEARCH_TRIGGERS = ["news","latest","today","weather","price","who is","what is","score","2026","trending"]

def search_web(query):
    try:
        results = tavily.search(query=query, search_depth="advanced", max_results=3)
        return "\n".join([r["content"] for r in results.get("results", [])])
    except:
        return ""

def get_ai_response(user_input):
    global chat_history
    now = datetime.now().strftime("%A, %B %d, %Y at %I:%M %p")
    web_context = ""
    if any(w in user_input.lower() for w in SEARCH_TRIGGERS):
        web_context = search_web(user_input)

    system_prompt = (
        f"You are J.A.R.V.I.S. Personal AI of {USER_NAME}. Always call him {CALL_NAME}. "
        f"Date: {now}. Personality: intelligent, calm, loyal, British tone like JARVIS from Iron Man. "
        f"Web data: {web_context}. "
        f"Always reply in 3 to 4 complete sentences. Never break character."
    )

    chat_history.append({"role": "user", "content": user_input})
    messages = [{"role": "system", "content": system_prompt}] + chat_history[-MAX_MEMORY:]

    try:
        res = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            max_tokens=350
        )
        reply = res.choices[0].message.content
        chat_history.append({"role": "assistant", "content": reply})
        save_memory(chat_history)
        return reply
    except Exception as e:
        return f"System error, {CALL_NAME}: {e}"

# ============================================================
#  KIVY UI
# ============================================================

class JarvisUI(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', padding=10, spacing=10, **kwargs)
        Window.clearcolor = get_color_from_hex("#0a0a0a")

        # Header
        header = Label(
            text="J.A.R.V.I.S",
            font_size="28sp",
            bold=True,
            color=get_color_from_hex("#00d4ff"),
            size_hint_y=None,
            height=50
        )
        self.add_widget(header)

        subtitle = Label(
            text=f"Online — {USER_NAME}",
            font_size="13sp",
            color=get_color_from_hex("#888888"),
            size_hint_y=None,
            height=25
        )
        self.add_widget(subtitle)

        # Chat display
        scroll = ScrollView(size_hint_y=0.7)
        self.chat_label = Label(
            text="JARVIS: All systems operational, Sir.\n",
            font_size="14sp",
            color=get_color_from_hex("#e0e0e0"),
            text_size=(Window.width - 30, None),
            size_hint_y=None,
            valign="top",
            markup=True
        )
        self.chat_label.bind(texture_size=self.chat_label.setter("size"))
        scroll.add_widget(self.chat_label)
        self.add_widget(scroll)
        self.scroll = scroll

        # Input area
        input_row = BoxLayout(size_hint_y=None, height=50, spacing=8)

        self.text_input = TextInput(
            hint_text="Type a command or question...",
            multiline=False,
            background_color=get_color_from_hex("#1a1a2e"),
            foreground_color=get_color_from_hex("#ffffff"),
            hint_text_color=get_color_from_hex("#555555"),
            cursor_color=get_color_from_hex("#00d4ff"),
            font_size="14sp"
        )
        self.text_input.bind(on_text_validate=self.on_send)
        input_row.add_widget(self.text_input)

        send_btn = Button(
            text="SEND",
            size_hint_x=None,
            width=80,
            background_color=get_color_from_hex("#00d4ff"),
            color=get_color_from_hex("#000000"),
            bold=True,
            font_size="13sp"
        )
        send_btn.bind(on_press=self.on_send)
        input_row.add_widget(send_btn)
        self.add_widget(input_row)

        # Quick command buttons
        quick_row1 = BoxLayout(size_hint_y=None, height=42, spacing=6)
        for label, cmd in [("🔋 Battery", "battery"), ("📶 WiFi Info", "wifi info"),
                            ("📸 Screenshot", "screenshot"), ("⏰ Time", "what time is it")]:
            btn = Button(
                text=label,
                background_color=get_color_from_hex("#1a1a2e"),
                color=get_color_from_hex("#00d4ff"),
                font_size="12sp",
                bold=True
            )
            btn.cmd = cmd
            btn.bind(on_press=self.quick_cmd)
            quick_row1.add_widget(btn)
        self.add_widget(quick_row1)

        quick_row2 = BoxLayout(size_hint_y=None, height=42, spacing=6)
        for label, cmd in [("🌙 Dark Mode", "dark mode on"), ("☀️ Light Mode", "dark mode off"),
                            ("🔕 Mute", "mute"), ("🔊 Max Vol", "max volume")]:
            btn = Button(
                text=label,
                background_color=get_color_from_hex("#1a1a2e"),
                color=get_color_from_hex("#00d4ff"),
                font_size="12sp",
                bold=True
            )
            btn.cmd = cmd
            btn.bind(on_press=self.quick_cmd)
            quick_row2.add_widget(btn)
        self.add_widget(quick_row2)

        quick_row3 = BoxLayout(size_hint_y=None, height=42, spacing=6)
        for label, cmd in [("💡 Torch On", "flashlight on"), ("💡 Torch Off", "flashlight off"),
                            ("🏠 Home", "go home"), ("🔒 Lock", "lock screen")]:
            btn = Button(
                text=label,
                background_color=get_color_from_hex("#1a1a2e"),
                color=get_color_from_hex("#00d4ff"),
                font_size="12sp",
                bold=True
            )
            btn.cmd = cmd
            btn.bind(on_press=self.quick_cmd)
            quick_row3.add_widget(btn)
        self.add_widget(quick_row3)

        # Speak greeting
        threading.Thread(target=lambda: speak(f"Good day, {CALL_NAME}. Jarvis is fully online."), daemon=True).start()

    def quick_cmd(self, btn):
        self.process_command(btn.cmd)

    def on_send(self, *args):
        query = self.text_input.text.strip()
        if not query:
            return
        self.text_input.text = ""
        self.add_message(f"[color=#00d4ff]YOU:[/color] {query}")
        threading.Thread(target=self.process_command, args=(query,), daemon=True).start()

    def add_message(self, msg):
        def update(*args):
            self.chat_label.text += f"{msg}\n\n"
            self.scroll.scroll_y = 0
        Clock.schedule_once(update)

    def process_command(self, query):
        was_command, response = parse_and_execute(query)
        if not was_command or not response:
            response = get_ai_response(query)
        self.add_message(f"[color=#ff9800]JARVIS:[/color] {response}")
        threading.Thread(target=lambda: speak(response), daemon=True).start()


class JarvisApp(App):
    def build(self):
        self.title = "J.A.R.V.I.S"
        return JarvisUI()


if __name__ == "__main__":
    JarvisApp().run()
