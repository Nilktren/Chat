from customtkinter import*
from socket import*
import threading
class Window(CTk):
    def __init__(self):
        super().__init__()
        self.geometry("400x600")
        self.title("LogiTalk")
        self.menu = CTkFrame(self)
        self.menu.place(x=0,y=0)
        self.menu.configure(width=0)
        self.menu.pack_propagate(False)
        self.show_menu = False
        self.width_menu = 0
        self.text_menu = CTkLabel(self.menu,text = "Ваше ім'я")
        self.text_menu.pack(pady = 30)
        self.name_menu = CTkEntry(self.menu)
        self.name_menu.pack()
        self.knopka = CTkButton(self.menu, text = "Підключитися", command = self.connect_to_server, bg_color = "purple", fg_color = "purple")
        self.knopka.pack()
        self.settings_menu = CTkButton(self,width = 30,height = 30,text = "⚙️", command = self.show_hide, bg_color = "purple", fg_color = "purple")
        self.settings_menu.place(x = 5, y = 5)
        self.chat = CTkTextbox(self, state = "disable")
        self.chat.place(x = 100, y = 150)
        self.pole = CTkEntry(self, placeholder_text = "Напішіть повідомлення")
        self.pole.place(x = 0, y = 500)
        self.pole.bind("<Return>", self.send_by_enter)
        self.psend = CTkButton(self, text = "▶️", width = 20, height = 20, command = self.send_message, bg_color = "purple", fg_color = "purple")
        self.psend.place(x = 138, y = 505)
        self.adaptive()
    def send_by_enter(self, enter):
        self.send_message
    def connect_to_server(self):
        self.name =self.name_menu.get()
        try:
            self.client_socket = socket(AF_INET, SOCK_STREAM)
            self.client_socket.connect(("7.tcp.eu.ngrok.io", 17378))
            self.client_socket.send(self.name.encode("utf-8"))
            threading.Thread(target = self.receive_messages).start()
        except Exception as e:
            self.add_message(f"Помилка підключення: {e}")
    def add_message(self, text):
        self.chat.configure(state = "normal")
        self.chat.insert("end", text + "\n")
        self.chat.configure(state = "disable")
        self.chat.see("end")
    def send_message(self):
        msg = self.pole.get()
        if msg:
            self.add_message(f"{self.name}: {msg}")
            a = f"TEXT@{self.name}@{msg}\n"
            try:
                self.client_socket.send(a.encode("utf-8"))
            except:
                pass
        self.pole.delete(0, "end")
    def receive_messages(self):
        basa = ""
        while True:
            try:
                data = self.client_socket.recv(4096).decode()
                if not data:
                    break
                basa += data
                line, basa = basa.split("\n", 1)
                self.rozbor(line)
            except:
                break
        self.client_socket.close()
    def rozbor(self, line):
        if not line:
            return
        parts = line.split("@", 3)
        massage_type = parts[0]
        if massage_type == "TEXT":
            if len(parts) >= 3:
                name_person = parts[1]
                text_msg = parts[2]
                self.add_message(f"{name_person}: {text_msg}")
    def adaptive(self):
        self.menu.configure(height = self.winfo_height())
        self.chat.configure(width = self.winfo_width() - self.menu.winfo_width(), height = self.winfo_height() - self.pole.winfo_height())
        self.chat.place(x = self.menu.winfo_width(), y = 25)
        self.pole.configure(width = self.winfo_width() - self.menu.winfo_width() - 210, height = 30)
        self.pole.place(x = self.menu.winfo_width(), y = self.winfo_height() - 220)
        self.psend.configure(width = self.pole.winfo_height(), height = self.pole.winfo_height() - 5)
        self.psend.place(x = self.winfo_width() - 200, y = self.winfo_height() - 220)
        self.after(20,self.adaptive)

    def show_hide(self):
        if self.show_menu == True:
            self.show_menu = False
            self.close_menu()
    
        else:
            self.show_menu = True
            self.open_menu()
    def close_menu(self):
        if self.width_menu > 0 :
            self.width_menu -= 30
            self.menu.configure(width = self.width_menu)
            self.after(30,self.close_menu)
    def open_menu(self):
        if self.width_menu < 200 :
            self.width_menu += 30
            self.menu.configure(width = self.width_menu)
            self.after(30,self.open_menu)
window = Window()
window.mainloop()