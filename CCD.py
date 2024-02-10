import pyperclip
import keyboard
import time
import requests
import tkinter as tk
from tkinter import messagebox
from bs4 import BeautifulSoup;


def load_html():
    global count, current_clipboard, text_content
    url = "http://server:82/knowledge-base/sensitive-and-new-client-list/"
    response = requests.get(url)
    html_content = response.text.lower()
    soup = BeautifulSoup(html_content, 'html.parser')
    text_content = soup.get_text()
    count = 0
    current_clipboard = ""


def on_key_press(event):
    global count, current_clipboard
    if event.name == 'c' and event.event_type == 'down' and keyboard.is_pressed('ctrl'):
        time.sleep(0.3)  # wait for the clipboard to update
        current_clipboard = pyperclip.paste()  
        print("You have copied:\t"+current_clipboard)
        count = text_content.count(current_clipboard.lower().strip())
        if count>0:
            print("The string "+ current_clipboard.strip() + f" appeared {count} times in the webpage.")
            print("="*55)
        else:
            print("The string "+ current_clipboard.strip() + " did NOT appear in the webpage.")
            print("="*55)

    elif event.name == 'q' and event.event_type == 'down' and keyboard.is_pressed('ctrl'):
        root = tk.Tk()
        root.withdraw()  # Hide the main window
        root.attributes('-topmost', 1)  # Make the messagebox appear on top
        if count>0:
            messagebox.showinfo("Alert", current_clipboard.strip() + " is a CRIT Client.")
        else:
            messagebox.showinfo("Alert", current_clipboard.strip() + " is NOT a crit.")
        root.destroy()  # Destroy the main window

    elif event.name == 'b' and event.event_type == 'down' and keyboard.is_pressed('ctrl'):
        load_html()
        root=tk.Tk()
        root.withdraw()
        root.attributes('-topmost', 1)
        messagebox.showinfo("Alert", "Critical Client List has been updated.")
        root.destroy()
        print("Critical Client List has been updated.")


def monitor_clipboard():
    print("Ready to use... \nPress [Ctrl+C] to copy and then [Ctrl+Q] to check if the client is a CRIT.\nPress [Ctrl+B] to refresh the Critical Client List.")
    print("*"*75)
    keyboard.on_press(on_key_press)
    keyboard.wait()

load_html()
monitor_clipboard()