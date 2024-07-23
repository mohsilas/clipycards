import re # regex (•᷄- •᷅ ;) 
import csv
import queue
import platform
import threading
import debugging
import pyperclip
from os import path
import tkinter as tk # 'cause ctk doesn't support opt menu.
from backend import *
from themes import Theme
from openai import NoneType
import customtkinter as ctk
from tkinter import messagebox as msgbox

db = debugging.Debug()
wait_animation = [] # default animation is loaded from config
i0, i1, i2 = 0, 1, 2 # animation keyframes indexes

config_file_path = path.join(path.expanduser('~'), "clipycards.config")
log_file_path = path.join(path.expanduser('~'), "clipycards.log")

class BridgeSharedHandles:
    def __init__(self) -> None:
        self.study_topic_context = ""
        self.frontend_theme = ""
        self.frontend_cards_export_format_separator = " | "
        self.backend_thread_running_event = threading.Event()
        self.backend_thread_new_card_is_generating_event = threading.Event()
        self.backend_thread_created_card_is_ready_event = threading.Event()
        self.backend_api_connection_error_event = threading.Event()
        self.backend_thread_stop_event = threading.Event()
        self.new_card_data_queue = queue.Queue()
        self.clipboard_data_queue = queue.Queue()
        
        self.backend_api_connection_error_event.clear()

    def thread_handles_joining_init(self): # refactor to reduce signals...
        self.backend_thread_created_card_is_ready_event.clear()
        self.backend_thread_running_event.set()
        self.backend_thread_stop_event.set()
        self.clipboard_data_queue.put("BACKEND_SIGTERM")

# ---------------------------------------------------------------- main window gui -------------------------------------------------------

class GuiAppMain(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.gui_new_topic_dialog_window_prevent_flag = False
        self.card_index = 0
        self.cards_data_list = []

        ctk.set_appearance_mode(style["sys-mode"])
        #ctk.set_default_color_theme("dark-blue")

        self.title("Clipycards")
        self.geometry("820x800") #wxh
        self.minsize(820, 600)

        main_frame = ctk.CTkFrame(self, fg_color=style["main-fg-color"])
        main_frame.pack(fill="both", expand=True)

        # Title Label
        self.title_label = ctk.CTkLabel(main_frame, text="", font=(style["title-font"][0], style["title-font"][1]), text_color=style["title-text-color"], fg_color=style["title-fg-color"], corner_radius=style["title-corner-radius"])
        self.title_label.pack(pady=10)
        # Scrollable Frame for the list of text entries
        self.list_frame = ctk.CTkScrollableFrame(main_frame, fg_color=style["main-fg-color"], corner_radius=style["mframe-corner-radius"], border_width=style["mframe-border-width"], border_color=style["mframe-border-color"], scrollbar_fg_color=style["mframe-scrlbar-fg-color"], scrollbar_button_hover_color=style["mframe-scrlbar-hover-color"], scrollbar_button_color=style["mframe-scrlbar-btn-color"])
        self.list_frame.pack(fill="both", expand=True, padx=10, pady=10)
        # Frame for control btns
        footer_frame = ctk.CTkFrame(main_frame, fg_color=style["footer-fg-color"], corner_radius=style["footer-corner-radius"], border_width=style["footer-border-width"], border_color=style["footer-border-color"])
        footer_frame.pack(fill="x", padx=10, pady=10)

        export_button = ctk.CTkButton(footer_frame, text="Export", fg_color=style["btn-export-fg-color"], text_color=style["btn-export-txt-color"], hover_color=style["btn-export-hover-color"], width=25, height=30, corner_radius=style["btn-export-corner-radius"], border_color=style["btn-export-border-color"], border_width=style["btn-export-border-width"], command=frontend_cards_export)
        export_button.pack(side="left", padx=10)

        # Create a frame with grey border for the dropdown menu
        dropdown_frame = ctk.CTkFrame(footer_frame, fg_color=style["optsmenu-btn-padding-color"], corner_radius=style["optsmenu-corner-radius"], border_width=style["optsmenu-border-width"], border_color=style["optsmenu-border-color"])
        dropdown_frame.pack(side="left", padx=10, pady=2)

        self.file_type_optionmenu = ctk.CTkOptionMenu(dropdown_frame, values=["Text (.txt)", "Sheet (.csv)"], height=27, dropdown_fg_color=style["optsmenu-fg-color"], fg_color=style["optsmenu-fg-color"], text_color=style["optsmenu-text-color"], button_color=style["optsmenu-btn-color"], button_hover_color=style["optsmenu-btn-hover-color"], corner_radius=style["optsmenu-corner-radius"], width=30)
        self.file_type_optionmenu.pack(padx=2, pady=2)

        self.pause_button = ctk.CTkButton(footer_frame, text="Pause", text_color=style["btn-pause-txt-color"], fg_color=style["btn-pause-fg-color"], hover_color=style["btn-pause-hover-color"], width=25, height=30, corner_radius=style["btn-pause-corner-radius"], border_width=style["btn-pause-border-width"], border_color=style["btn-pause-border-color"], command=frontend_backend_thread_pause)
        self.pause_button.pack(side="right", padx=10)

        new_topic_button = ctk.CTkButton(footer_frame, text="+ New Context", text_color=style["btn-ncontext-txt-color"], fg_color=style["btn-ncontext-fg-color"], hover_color=style["btn-ncontext-hover-color"], width=30, height=30, border_width=style["btn-ncontext-border-width"], corner_radius=style["btn-ncontext-corner-radius"], border_color=style["btn-ncontext-border-color"], command=frontend_topic_context_create)
        new_topic_button.pack(side="right", padx=10)

    def frontend_new_card_object_create(self, card_data):
        card_data_text = card_data[0]
        card_prompt = card_data[1]
        colors_list = style["cards-alt-colors"]
        alt_colors = colors_list[self.card_index % 2]
        entry_frame = ctk.CTkFrame(self.list_frame, fg_color=alt_colors, corner_radius=style["cards-corner-radius"])
        entry_frame.pack(fill="x", pady=5)

        text_label_frame = ctk.CTkFrame(entry_frame, fg_color=alt_colors)
        text_label_frame.pack(side="left", padx=10, expand=False, fill="x")

        text_label = ctk.CTkLabel(text_label_frame, text=card_data_text, font=(style["cards-font"][0], style["cards-font"][1]), anchor="w", fg_color=alt_colors, text_color=style["cards-txt-color"], wraplength=650, justify="left")
        text_label.pack(side="left", fill="x", expand=False, pady=style["cards-txt-pady"], padx=style["cards-txt-padx"])

        button_frame = ctk.CTkFrame(entry_frame, fg_color=alt_colors)
        button_frame.pack(side="right", padx=10)

        options_button = ctk.CTkButton(button_frame, text=style["card-btn-opts-icon"], font=(style["cards-btn-icon-font"][0], style["cards-btn-icon-font"][1]), width=30, height=30, fg_color=alt_colors, text_color=style["card-btns-txt-color"], hover_color=style["card-btns-hover-color"])
        options_button.pack(side="left", padx=5)
        options_button.configure(command=lambda event=None, idx=self.card_index: frontend_card_options_menu_show(idx, options_button))

        self.cards_data_list.append([entry_frame, text_label_frame, text_label, button_frame, options_button, card_prompt])
        self.card_index += 1

# ---------------------------------------------------------------- secondary windows gui -------------------------------------------------------

class LargeTextInputDialog(ctk.CTkToplevel):
    def __init__(self, master=None, msg="Clipycards requires context.\nPls provide some info or the title of your study session.", geo = "600x530", w=580, h=390, clear_cards=0, win_title="Study Topic",**kwargs):
        super().__init__(master, **kwargs)
        self.title(win_title)
        self.geometry(geo)
        self.resizable(False, False)
        self.configure(fg_color=style["subwn-fg-color"])
        self.result = None

        white_frame = ctk.CTkFrame(self, fg_color=style["subwn-fg-color"])
        white_frame.pack(fill="both", expand=True)

        self.label = ctk.CTkLabel(white_frame, text=msg, text_color=style["subwn-txt-color"], fg_color=style["title-fg-color"])
        self.label.pack(pady=10)
        self.text = ctk.CTkTextbox(white_frame, width=w, height=h, fg_color=style["subwn-tarea-fg"], border_width=1, border_color="grey", scrollbar_button_color=style["subwn-tarea-fg"])
        self.text.pack(pady=10, padx=10)
        self.button_frame = ctk.CTkFrame(white_frame, fg_color=style["subwn-fg-color"])
        self.button_frame.pack(pady=10)

        self.cancel_button = ctk.CTkButton(self.button_frame, text="Cancel", command=self.on_cancel, fg_color=style["subwn-cancel-btn-color"], text_color=style["subwn-btn-txt-color"], hover_color=style["subwn-btns-hover-color"])
        self.cancel_button.pack(side="left", padx=5)

        if clear_cards:
            self.submit_button = ctk.CTkButton(self.button_frame, text="Clear Cards", command=menu_bar_cards_delete_all, fg_color=style["subwn-btn-color"], text_color=style["subwn-btn-txt-color"], hover_color=style["subwn-btns-hover-color"])
            self.submit_button.pack(side="left", padx=5)

        self.submit_button = ctk.CTkButton(self.button_frame, text="Submit", command=self.on_submit, fg_color=style["subwn-btn-color"], text_color=style["subwn-btn-txt-color"], hover_color=style["subwn-btns-hover-color"])
        self.submit_button.pack(side="left", padx=5)

    def on_submit(self):
        self.result = self.text.get("1.0", "end-1c").strip()
        self.destroy()

    def on_cancel(self):
        self.result = None
        self.destroy()

# --------------------------------------------------------------------- frontend / buttons -----------------------------------------------------------
def menu_bar_cards_delete_all(): # LargeTextInputDialog clear_cards btn
    for i in range(app.card_index):
        if not app.cards_data_list[i] == None:
            frontend_card_delete(i)
    app.cards_data_list = []
    app.card_index = 0
# ---------------------------------- footer buttons
def frontend_cards_export(): # it looks ugly, but it's readable. ¯\_(ツ)_/¯
    if not app.cards_data_list:
        msgbox.showwarning("Export Error", "can't export an empty cards list.")
        return
    dir_path =  ctk.filedialog.askdirectory()
    if app.file_type_optionmenu.get() == "Sheet (.csv)":
        export_dir_csv = path.join(dir_path, f"{session_title}.csv")
        file_content = []
        for card in app.cards_data_list:
            if card != None:
                file_content.append(str(card[2].cget("text")).split(bridge_shared_handles.frontend_cards_export_format_separator))
        with open(export_dir_csv, "a+") as fo:
            csvfo = csv.writer(fo)
            csvfo.writerows(file_content)
    else:
        #print("Exporting .txt")
        export_dir_txt = path.join(dir_path, f"{session_title}.txt")
        file_content = ""
        for card in app.cards_data_list: 
            if card != None:
                file_content += card[2].cget("text") + "\n\n"
        #print("exported file content\n", file_content)
        with open(export_dir_txt, "x") as fo:
            fo.write(file_content)
            #print("saved to file: ", export_dir_txt)
   
def frontend_topic_context_create():
    global last_clipboard_content
    if not app.gui_new_topic_dialog_window_prevent_flag:
        app.gui_new_topic_dialog_window_prevent_flag = True
        dialog = LargeTextInputDialog(app, clear_cards=1)
        app.wait_window(dialog)
        if not dialog.result:
            app.gui_new_topic_dialog_window_prevent_flag = False
            return # if the dialog is empty, the function simply stops here by returning nothing
        bridge_shared_handles.study_topic_context = dialog.result
        session_title = backend_study_context_title_generate(bridge_shared_handles.study_topic_context)
        app.title_label.configure(text=session_title)
        last_clipboard_content = pyperclip.paste()
        app.gui_new_topic_dialog_window_prevent_flag = False

def frontend_backend_thread_pause():
    if bridge_shared_handles.backend_api_connection_error_event.is_set():
        if backend_internet_is_connected():
            bridge_shared_handles.backend_api_connection_error_event.clear()

    if bridge_shared_handles.backend_thread_running_event.is_set():
        bridge_shared_handles.backend_thread_running_event.clear()
        app.pause_button.configure(text="Resume")
        #print("backend thread Paused")
    elif not bridge_shared_handles.backend_thread_running_event.is_set() and not bridge_shared_handles.backend_api_connection_error_event.is_set():
        bridge_shared_handles.backend_thread_running_event.set()
        app.pause_button.configure(text="Pause")
        #print("backend thread Resumed")

# ----------------------------------- cards buttons
def frontend_card_options_menu_show(idx, button):
    menu = tk.Menu(app, tearoff=0)
    menu.add_command(label="regenerate Card", command=lambda: frontend_backend_regenerate_card(idx))
    menu.add_command(label="Edit Card", command=lambda: frontend_card_edit(idx))
    menu.add_command(label="Edit Prompt", command=lambda: frontend_prompt_edit(idx))
    menu.add_command(label="Delete", command=lambda: frontend_card_delete(idx))
    try:
        menu.tk_popup(button.winfo_rootx(), button.winfo_rooty() + button.winfo_height())
    finally:
        menu.grab_release()

def frontend_card_edit(idx):
    card_edit_window_dialog = LargeTextInputDialog(app, msg="Edit The Card's Content", geo="600x500", h=350,w=580, win_title="Edit Card")
    card_edit_window_dialog.text.insert("0.0", app.cards_data_list[idx][2].cget("text"))
    app.wait_window(card_edit_window_dialog)
    if card_edit_window_dialog.result:
        app.cards_data_list[idx][2].configure(text=card_edit_window_dialog.result)
        #print("edited card: ", card_edit_window_dialog.result)
    else:
        pass
    
def frontend_prompt_edit(idx):
    #print(f"Edit prompt of the card with index: {idx}")
    prompt_edit_window_dialog = LargeTextInputDialog(app, msg="Edit Card's Prompt To Regenerate A New One", geo="600x700", h=580,w=580, win_title="Edit Prompt")
    prompt_edit_window_dialog.text.insert("0.0", app.cards_data_list[idx][-1])
    app.wait_window(prompt_edit_window_dialog)
    edited_prompt = prompt_edit_window_dialog.result
    if edited_prompt:
        try:
            previous_text = app.cards_data_list[idx][2].cget("text")
            app.cards_data_list[idx][2].configure(text="Regenerating Card...")
            app.update()
            app.cards_data_list[idx][2].configure(text=backend_api_response_get(edited_prompt, sys_role_enabled=0))
        except Exception as e:
            msgbox.showwarning("Generation Error", f"Can't regenerate the card. Please check {log_file_path} for more info")
            app.cards_data_list[idx][2].configure(text=previous_text)
            db.log_err(__name__, e, f"Can't update the prompt")
        app.cards_data_list[idx][-1] = edited_prompt
    else:
        pass
    #print("edited card: ", edited_prompt)

def frontend_card_delete(idx):
    card = app.cards_data_list[idx]
    _ = card.pop() # 'cause card_prompt (last element in cards_data_list) is str without .destroy()
    for widget in card:
        widget.destroy()
    app.cards_data_list[idx] = None
    #print(f"Card at index {idx} deleted | {app.cards_data_list[idx]}")

def frontend_backend_regenerate_card(idx):
    previous_text = app.cards_data_list[idx][2].cget("text")
    app.cards_data_list[idx][2].configure(text="Regenerating Card...")
    app.update()  # Force update of the GUI
    card_prompt = app.cards_data_list[idx][-1]
    try:
        app.cards_data_list[idx][2].configure(text=backend_api_response_get(card_prompt, sys_role_enabled=0))
        app.pause_button.configure(text="Pause")
    except Exception as e:
            msgbox.showwarning("Generation Error", f"Can't regenerate the card. Please check {log_file_path} for more info")
            app.cards_data_list[idx][2].configure(text=previous_text)
            app.update()
            db.log_err(__name__, e, f"Can't regenerate card")
        
# --------------------------------------------------------------- bridge functions / small funcs----------------------------------------------------
# bridge queues data >> backend processes data async-ly >> bridge updates ui

def bridge_clipboard_listener_loop():
    global last_clipboard_content
    if bridge_shared_handles.backend_thread_running_event.is_set():
        current_clipboard_content = pyperclip.paste()
        if current_clipboard_content != last_clipboard_content:
            bridge_shared_handles.clipboard_data_queue.put(add_bullets(current_clipboard_content))
            last_clipboard_content = current_clipboard_content
    app.after(500, bridge_clipboard_listener_loop)


def bridge_card_generated_listener_loop():
    global i0, i1, i2
    animation_buffer_len = len(wait_animation) - 3
    if bridge_shared_handles.backend_thread_new_card_is_generating_event.is_set():
        app.pause_button.configure(text=f"{wait_animation[i0]}{wait_animation[i1]}{wait_animation[i2]}")
        i0 = i0 + 1 if i0 < animation_buffer_len else 1
        i1 = i0 + 1
        i2 = i0 + 2
    if bridge_shared_handles.backend_thread_created_card_is_ready_event.is_set():
        if not bridge_shared_handles.new_card_data_queue.empty():
            app.frontend_new_card_object_create(bridge_shared_handles.new_card_data_queue.get())
            bridge_shared_handles.backend_thread_created_card_is_ready_event.clear()
            app.pause_button.configure(text="Pause")
    if bridge_shared_handles.backend_api_connection_error_event.is_set():
        app.pause_button.configure(text="Resume")
        bridge_shared_handles.backend_api_connection_error_event.clear()
    app.after(200, bridge_card_generated_listener_loop)


def bridge_backend_thread_join():
    bridge_shared_handles.thread_handles_joining_init() # handles thread events to prevent waiting
    backend_thread.join()
    #print("backend thread stopped")
    exit()


def add_bullets(text): # for when the user copies a text with bullets
    lines = text.split('\n')
    result = []
    bullet_pattern = re.compile(r'^\s*[•\-*]\s')
    
    for i, line in enumerate(lines):
        stripped = line.strip()
        if not stripped:  # Empty line
            result.append(line)
            continue
        if bullet_pattern.match(line) or i == 0:  # Line already has a bullet or is the first line
            result.append(line)
            continue
        indent = len(line) - len(line.lstrip())
        bullets = '  ' * (indent // 2) + '• '
        result.append(' ' * indent + bullets + stripped)
    return '\n'.join(result)


def menu_bar_about():
    msgbox.showinfo("About", "ClipyCards version 0.1.0\nCopyright © 2024 MohSilas, GNU General Public License.\nWebsite: clipycards.com")

def menu_bar_quit():
    bridge_shared_handles.thread_handles_joining_init()
    exit()
# --------------------------------------------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------- main ----------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------------------

bridge_shared_handles = BridgeSharedHandles() # allow backend and frontend signalling through events, queues, and vars
theme = Theme()
style = theme.load_from_config()
wait_animation = style["wait-animation"]

try:
    app = GuiAppMain()
except Exception as e:
    msgbox.showerror("Init Error", f"There was an error starting Clipycards. Check {log_file_path} for debug info.")
    db.log_crit(__name__, e, "GuiAppMain init error")
    exit()

app.withdraw() # hide until validations and getting topic context

if not backend_config_file_validate(app, LargeTextInputDialog, theme.config):
    msg = "Your config file at " + config_file_path + " is missing some keys.\nPls check clipycards.log in the same location for help"
    msgbox.showwarning("config error", msg)
    exit()

if not backend_internet_is_connected():
    msg = f"You seem to be offline. Please check you internet connection and try again.\nIf you're already online, check {log_file_path} for help."
    msgbox.showwarning("Connection failed", msg)
    exit()

dialog_study_topic_context_create = LargeTextInputDialog(app)
app.wait_window(dialog_study_topic_context_create)
if not dialog_study_topic_context_create.result:
    exit()

bridge_shared_handles.study_topic_context = dialog_study_topic_context_create.result
backend_api_object_create() # creates an Openai or Anthropic client based on the configs
session_title = backend_study_context_title_generate(bridge_shared_handles.study_topic_context)
app.title_label.configure(text=session_title)
app.deiconify()

last_clipboard_content = pyperclip.paste()
bridge_clipboard_listener_loop()
bridge_card_generated_listener_loop()

# threading stuff for the api
bridge_shared_handles.backend_thread_running_event.set()
backend_thread = threading.Thread(target=backend_thread_main, args=(bridge_shared_handles, 0))
backend_thread.start()

if platform.system() == "Darwin": # You can't hide tk's ugly default app menu on mac without implementing a new GUI lib.
    # Create a menu bar 
    menu_bar = tk.Menu(app)
    # Create the About menu
    about_menu = tk.Menu(menu_bar, tearoff=0)
    about_menu.add_command(label="About", command=menu_bar_about)
    about_menu.add_command(label="Quit", command=menu_bar_quit)
    menu_bar.add_cascade(label="ClipyCards", menu=about_menu)

    # Configure the menu bar in the application
    app.config(menu=menu_bar)
    #app.config(menu="")
else:
    app.config(menu="") # hides default tk menu on windows and linux


app.protocol("WM_DELETE_WINDOW", bridge_backend_thread_join) #joins the backend_thread when closing the app
app.mainloop()