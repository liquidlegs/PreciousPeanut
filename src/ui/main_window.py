import tkinter as tk
from tkinter import ttk
from tkinter.colorchooser import askcolor
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter.simpledialog import askstring
from tkinter.messagebox import showerror
from file_ops import load_config_file, update_config_file
from file_ops import read_file, write_file
from xor_ops import encrypt_string, decrypt_string

APP_NAME = "PreciousPeanut"

class MainWindow(tk.Tk):

    def __init__(self):
        tk.Tk.__init__(self)
        self.geometry("800x600")
        self.title(APP_NAME)
        self.create_top_menu()
        self.config = load_config_file()
        self.apply_config_settings()

    
    def create_top_menu(self) -> None:
        self.menu_bar = tk.Menu(self)
        menu_bar = self.menu_bar

        self.text_area = tk.Text(self)
        self.text_area.config(borderwidth="1", relief="solid")
        self.text_area.pack(expand=1, fill="both")

        self.file_button_menu = tk.Menu(menu_bar, tearoff=0)
        self.edit_button_menu = tk.Menu(menu_bar, tearoff=0)
        self.help_button_menu = tk.Menu(menu_bar, tearoff=0)

        menu_bar.add_cascade(menu=self.file_button_menu, label="File")
        menu_bar.add_cascade(menu=self.edit_button_menu, label="Edit")
        menu_bar.add_cascade(menu=self.help_button_menu, label="Help")

        self.bind("<Control-n>", lambda event: self.on_key_press(event, "New"))
        self.bind("<Control-o>", lambda event: self.on_key_press(event, "Open"))
        self.bind("<Control-s>", lambda event: self.on_key_press(event, "Save"))
        self.bind("<Control-p>", lambda event: self.on_key_press(event, "Preferences"))
        self.bind("<Control-q>", lambda event: self.quit())

        self.file_button_menu.add_command(label="New", command=self.new_file)
        self.file_button_menu.add_command(label="Open", command=self.open_file)
        self.file_button_menu.add_command(label="Save", command=self.save_file)
        self.file_button_menu.add_command(label="SaveAs",command=self.save_file_as)
        self.file_button_menu.add_separator()
        self.file_button_menu.add_command(label="Exit", command=quit)

        self.edit_button_menu.add_command(label="Toggle WordWrap", command=self.toggle_word_wrap)
        self.edit_button_menu.add_command(label="Preferences", command=self.create_options_window)
        self.help_button_menu.add_command(label="About")
        self.config(menu=menu_bar)


    def on_key_press(self, event, f_menu_btn) -> None:    
        match f_menu_btn:
            case "New":
                self.new_file()
            case "Open":
                self.open_file()
            case "Save":
                self.save_file()
            case "Preferences":
                self.create_options_window()


    def toggle_word_wrap(self) -> None:
        if self.config.word_wrap == True:
            self.config.word_wrap = False
        else:
            self.config.word_wrap = True

        self.update_and_apply_config()


    def new_file(self) -> None:
        self.title(APP_NAME)
        self.text_area.delete(1.0, tk.END)

    
    def open_file(self) -> None:
        file_name = askopenfilename(
            filetypes=[
                ("Encrypted Files", "*.pnutx"),
                ("Text files", "*.txt"),
                ("Any file", "*")
            ]
        )

        if file_name != () and type(file_name) != str:
            showerror("Error: FileNotFound", "unable to open file")
            return
        
        content = read_file(file_name)
        
        if file_name.endswith(".pnutx"):
            content = self.handle_encryption_key(content, "decryption")
        
            if content == None:
                return None

        self.title(file_name)
        self.text_area.delete(1.0, tk.END)
        self.text_area.insert(tk.END, content)
        return
    

    def save_file(self) -> None:
        if self.title() == APP_NAME:
            self.save_file_as()

        file_name = self.title()
        content = self.text_area.get(1.0, tk.END).rstrip()

        if self.title().endswith(".pnutx"):
            content = self.handle_encryption_key(content, "encryption")
            
            if content == None: 
                return None

        success = write_file(file_name, content)
        
        if success == False:
            showerror("Error: File error", f"unable to save file {file_name}")
            return


    def handle_encryption_key(self, content: str, action: str) -> str:
        output = None
        
        match action:
            case "encryption":
                if self.config.xor_key != None:
                    output = encrypt_string(content, self.config.xor_key)
                else:
                    temp_key = askstring("Authentication Required", "Please Enter Your Key")
                    output = encrypt_string(content, temp_key)
            case "decryption":
                if self.config.xor_key != None:
                    output = decrypt_string(content, self.config.xor_key)
                else:
                    temp_key = askstring("Authentication Required", "Please Enter Your Key")
                    output = decrypt_string(content, temp_key)

        return output


    def save_file_as(self) -> None:
        file_name = asksaveasfilename(
            filetypes=[
                ("Encrypted File", "*.pnutx"),
                ("Text files", "*.txt"),
                ("Any file", "*")
            ]
        )

        if file_name != () and type(file_name) != str:
            showerror("Error: Failed to write file", "Unable to write file to disk")
            return
        
        content = self.text_area.get(1.0, tk.END).rstrip()

        if file_name.endswith(".pnutx"):
            content = self.handle_encryption_key(content, "encryption")

            if content == None:
                return None

        success = write_file(file_name, content)

        if success == False:
            showerror("Error: Failed to write file", "Unable to write file to disk")
            return
        
        self.title(file_name)


    def apply_config_settings(self) -> bool:
        if self.config == None:
            return False
        
        display = self.config.display
        bg_colour = self.config.bg_colour
        fg_colour = self.config.fg_colour
        text_size = self.config.text_size
        font_fam = self.config.font_fam
        word_wrap = self.config.word_wrap
        highlight_colour = self.config.highlight_colour
        cursor_colour = self.config.cursor_colour
        toolbar_colour = self.config.toolbar_colour

        if display != None:
            self.geometry(display)

        if bg_colour != None:
            self.text_area.config(background=bg_colour)

        if fg_colour != None:
            self.text_area.config(foreground=fg_colour)

        if text_size > 0 and font_fam != None:
            self.text_area.config(font=(font_fam, text_size))

        if word_wrap != None:
            wrap = tk.NONE

            if word_wrap == True:
                wrap = tk.WORD

            self.text_area.config(wrap=wrap)

        if highlight_colour != None:
            self.text_area.config(selectbackground=highlight_colour)

        if cursor_colour != None:
            self.text_area.config(insertbackground=cursor_colour)

        if toolbar_colour != None:
            self.menu_bar.config(background=toolbar_colour)
            self.edit_button_menu.config(background=toolbar_colour)
            self.file_button_menu.config(background=toolbar_colour)
            self.help_button_menu.config(background=toolbar_colour)

        return True


    def update_and_apply_config(self):
        update_config_file(self.config)
        self.apply_config_settings()


    def get_colour_code(self, btn: tk.Button, name: str) -> None:        
        print(btn["background"])
        
        (code, hex) = askcolor()
        btn.config(bg=hex)

        match name:
            case "bg":
                self.config.bg_colour = hex
            case "fg":
                self.config.fg_colour = hex
            case "cursor":
                self.config.cursor_colour = hex
            case "highlight":
                self.config.highlight_colour = hex
            case "toolbar":
                self.config.toolbar_colour = hex


    def set_text_size(self, nbr_box: tk.Spinbox) -> None:
        size = int(nbr_box.get())
        self.config.text_size = size


    def apply_config_colour_settings(self, btn: tk.Button, name: str) -> None:
        match name:
            case "bg":
                if self.config.bg_colour != None:
                    btn.config(bg=self.config.bg_colour)
            case "fg":
                if self.config.fg_colour != None:
                    btn.config(bg=self.config.fg_colour)
            case "cursor":
                if self.config.cursor_colour != None:
                    btn.config(bg=self.config.cursor_colour)
            case "highlight":
                if self.config.highlight_colour != None:
                    btn.config(bg=self.config.highlight_colour)
            case "toolbar":
                if self.config.toolbar_colour != None:
                    btn.config(bg=self.config.toolbar_colour)


    def create_options_window(self) -> None:
        root = tk.Toplevel()
        root.title("Preferences")

        frame = ttk.Frame(root, width="200", height="100", relief="ridge")
        bg_label = ttk.Label(frame, text="Background")
        bg_btn = tk.Button(frame, name="bg", command=lambda: self.get_colour_code(bg_btn, "bg"), width=10)

        fg_colour = ttk.Label(frame, text="Foreground")
        fg_btn = tk.Button(frame, name="fg", command=lambda: self.get_colour_code(fg_btn, "fg"), width=10)

        cur_colour = ttk.Label(frame, text="Cursor")
        cur_btn = tk.Button(frame, name="cur", command=lambda: self.get_colour_code(cur_btn, "cursor"), width=10)

        high_colour = ttk.Label(frame, text="Highlight")
        high_btn = tk.Button(frame, name="high", command=lambda: self.get_colour_code(high_btn, "highlight"), width=10)

        toolbar_colour = ttk.Label(frame, text="Toolbar Colour")
        toolbar_btn = tk.Button(frame, name="toolbar", command=lambda: self.get_colour_code(toolbar_btn, "toolbar"), width=10)

        text_size = ttk.Label(frame, text="Text Size")
        nbr_box = tk.Spinbox(frame, from_=0, to=100, command=lambda: self.set_text_size(nbr_box), width=10)
        nbr_value = tk.StringVar(frame)
        nbr_value.set(str(self.config.text_size))

        self.apply_config_colour_settings(bg_btn, "bg")
        self.apply_config_colour_settings(fg_btn, "fg")
        self.apply_config_colour_settings(cur_btn, "cursor")
        self.apply_config_colour_settings(high_btn, "highlight")
        self.apply_config_colour_settings(toolbar_btn, "toolbar")
        nbr_box.config(textvariable=nbr_value)

        btn_ok = tk.Button(frame, text="Ok", name="ok", command=lambda: self.apply_config_settings())
        btn_save = tk.Button(frame, text="Save", command=lambda: self.update_and_apply_config())
        btn_cancel = tk.Button(frame, text="Cancel", name="cancel", command=root.destroy)

        frame.grid(row=0)
        bg_label.grid(row=0, column=0)
        bg_btn.grid(row=0, column=1)
        fg_colour.grid(row=1, column=0)
        fg_btn.grid(row=1, column=1)
        cur_colour.grid(row=2, column=0)
        cur_btn.grid(row=2, column=1)
        high_colour.grid(row=3, column=0)
        high_btn.grid(row=3, column=1)
        toolbar_colour.grid(row=4, column=0)
        toolbar_btn.grid(row=4, column=1)
        text_size.grid(row=5, column=0)
        nbr_box.grid(row=5, column=1)

        btn_ok.grid(row=6, column=0)
        btn_save.grid(row=6, column=1)
        btn_cancel.grid(row=6, column=2)