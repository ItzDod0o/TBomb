import tkinter as tk
from tkinter import font, filedialog, messagebox, ttk
import threading
import pyautogui
import requests
from PIL import Image, ImageTk
import io
import os
import time  # Adding the time module

class TextBomberApp:
    def __init__(self, master):
        self.master = master
        self.master.title("TBomber (Beta 0.1)")  # Changed title
        self.master.geometry("1366x768")

        self.running = False

        # Load background image if available
        try:
            # Load a random image from the internet
            response = requests.get("https://www.themandarin.com.au/wp-content/uploads/2023/08/AdobeStock_94009599-e1691641794765.jpeg")
            image_data = response.content
            self.background_image = Image.open(io.BytesIO(image_data))
            self.background_image = self.background_image.resize((1366, 768))
            self.background_photo = ImageTk.PhotoImage(self.background_image)
            self.background_label = tk.Label(master, image=self.background_photo)
            self.background_label.place(relx=0.5, rely=0.5, anchor="center")
        except Exception as e:
            print("Error loading background image:", e)

        # Define themes
        self.themes = {
            "Light": {"bg": "white", "fg": "black", "button_bg": "#2196F3", "button_fg": "white"},
            "Dark": {"bg": "black", "fg": "white", "button_bg": "#4CAF50", "button_fg": "white"}
        }

        self.current_theme = tk.StringVar()
        self.current_theme.set("Light")

        # Create main frame
        self.main_frame = tk.Frame(master, bd=5, width=331, height=153)
        self.main_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Create widgets
        self.create_widgets()

    def create_widgets(self):
        LABEL_FONT = ("Arial", 12)

        # Create message label and entry
        self.message_label = tk.Label(self.main_frame, text="Enter the message to loop:", font=LABEL_FONT)
        self.message_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.message_entry = tk.Entry(self.main_frame, font=LABEL_FONT)
        self.message_entry.grid(row=0, column=1, padx=10, pady=5)

        # Create cooldown label and entry
        self.cooldown_label = tk.Label(self.main_frame, text="Cooldown time (seconds):", font=LABEL_FONT)
        self.cooldown_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.cooldown_entry = tk.Entry(self.main_frame, font=LABEL_FONT)
        self.cooldown_entry.grid(row=1, column=1, padx=10, pady=5)

        # Create start/stop button
        self.start_stop_button = tk.Button(self.main_frame, text="Start", font=LABEL_FONT, command=self.toggle_loop)
        self.start_stop_button.grid(row=2, column=0, columnspan=2, padx=10, pady=15, sticky="we")

        # Create open txt button
        self.open_txt_button = tk.Button(self.main_frame, text="Open Text File to test", font=LABEL_FONT, command=self.create_temp_text_file)
        self.open_txt_button.grid(row=3, column=0, columnspan=2, padx=10, pady=15, sticky="we")

        # Create open browser button
        self.open_browser_button = tk.Button(self.main_frame, text="This code is free so small donations means alot to me, Thank you! <3", font=LABEL_FONT, command=self.open_browser)
        self.open_browser_button.grid(row=4, column=0, columnspan=2, padx=10, pady=15, sticky="we")

        # Create message display label
        self.message_display = tk.Label(self.main_frame, text="", font=LABEL_FONT, wraplength=400)
        self.message_display.grid(row=5, columnspan=2, padx=10, pady=5)

        # Create additional message label
        additional_message = "Developed by ItzDod0"
        additional_label = tk.Label(self.main_frame, text=additional_message, font=("Arial", 10, "italic"), fg="red", borderwidth=1, relief="solid")
        additional_label.grid(row=6, columnspan=2, pady=10, padx=10, sticky="we")

        # Theme selector
        theme_label = tk.Label(self.main_frame, text="Theme:", font=LABEL_FONT)
        theme_label.grid(row=7, column=0, padx=10, pady=5, sticky="w")
        self.theme_selector = ttk.Combobox(self.main_frame, textvariable=self.current_theme, values=list(self.themes.keys()))
        self.theme_selector.grid(row=7, column=1, padx=10, pady=5)
        self.theme_selector.bind("<<ComboboxSelected>>", self.change_theme)
        self.theme_selector["state"] = "readonly"  # Lock the theme selector

        self.apply_theme()  # Apply theme initially

    def apply_theme(self):
        theme = self.themes[self.current_theme.get()]
        self.master.config(bg=theme["bg"])
        self.main_frame.config(bg=theme["bg"])
        self.message_label.config(bg=theme["bg"], fg=theme["fg"])
        self.cooldown_label.config(bg=theme["bg"], fg=theme["fg"])
        self.start_stop_button.config(bg=theme["button_bg"], fg=theme["button_fg"])
        self.open_txt_button.config(bg=theme["button_bg"], fg=theme["button_fg"])
        self.open_browser_button.config(bg=theme["button_bg"], fg=theme["button_fg"])
        self.message_display.config(bg=theme["bg"], fg=theme["fg"])
        self.theme_selector.config(background=theme["bg"], foreground=theme["fg"])

    def change_theme(self, event=None):
        self.apply_theme()

    def toggle_loop(self):
        if self.running:
            self.stop_loop()
        else:
            self.start_loop()

    def start_loop(self):
        try:
            message = self.message_entry.get()
            cooldown = float(self.cooldown_entry.get())
        except ValueError:
            messagebox.showerror("Bro you forgot to put the cooldown time or you're using letters to specify a time, I bet your education system is American.")
            return

        if not message:
            messagebox.showerror("Bruh what do you expect to send with no messages? Memes? Enter a message.")
            return

        self.running = True
        self.start_stop_button.config(text="Stop", command=self.stop_loop)

        thread = threading.Thread(target=self.loop_message, args=(message, cooldown))
        thread.start()

    def stop_loop(self):
        self.running = False
        self.start_stop_button.config(text="Start", command=self.start_loop)
        self.message_display.config(text="Looping stopped...")

    def loop_message(self, message, cooldown):
        while self.running:
            pyautogui.typewrite(message + '\n')
            time.sleep(cooldown)

    def create_temp_text_file(self):
        temp_file_path = "temp_text_file.txt"

        # Create and write to the temporary text file
        with open(temp_file_path, "w") as f:
            f.write("")

        print("Attempting to open file...")  # Debug print
        os.startfile(temp_file_path)
        print("File opened successfully.")  # Debug print

        # Schedule a check for file existence after 500 milliseconds
        self.master.after(500, self.check_file_existence, temp_file_path)

    def check_file_existence(self, temp_file_path):
        if not os.path.exists(temp_file_path):
            messagebox.showinfo("Temporary Text File", "Temporary text file closed.")
            return
        # Schedule another check after 500 milliseconds
        self.master.after(500, self.check_file_existence, temp_file_path)

    def open_browser(self):
        # Open a browser link
        os.system("start https://paypal.me/ItzDod0")


def main():
    root = tk.Tk()
    app = TextBomberApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
