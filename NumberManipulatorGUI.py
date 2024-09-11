import tkinter as tk
from tkinter import *
import ctypes
from help_utils import *
from areaCodes import stateByAreaCode
from dedupe import deDupe, feed_next_number, full_list_to_clipboard
from badnumdel import badNumDel
from my_google import googleSearch, displaySearchResults
import keyboard
import threading
import sys

googleResults = []
potential_phone_nums = []

def main():

    def on_resize(root, google_frame, automin):
        # Ensure the window has been updated
        root.update_idletasks()
        
        # Get the width and height
        width = root.winfo_width()
        height = root.winfo_height()
        
        # Set threshold sizes
        width_threshold = 200
        height_threshold = 400

        if width < width_threshold or height < height_threshold:
            # Hide certain widgets
            google_frame.grid_remove()
            automin.grid_remove()
        else:
            # Show widgets
            google_frame.grid()
            automin.grid()



    def on_return(event):
        global googleResults, potential_phone_nums

        # widget that triggered the event
        widget = event.widget

        if widget == inEntryDelete and inEntryDelete.get("1.0", "end-1c").strip():
            badNumDel(inEntryDelete, onOff, root)
        elif widget == inEntryDeDup and inEntryDeDup.get("1.0", "end-1c").strip():
            deDupe(inEntryDeDup, possibleStatesLbl, onOff, root)
        elif widget == inEntryAreaCode and inEntryAreaCode.get("1.0", "end-1c").strip():
            stateByAreaCode(inEntryAreaCode)
        elif widget == inGoogleText and inGoogleText.get("1.0", "end-1c").strip():
            googleResults, potential_phone_nums = googleSearch(inGoogleText)
        return 'break'



    def setup_global_hotkey():
        keyboard.add_hotkey('ctrl+f', feed_next_number)
        keyboard.add_hotkey('ctrl+shift+f', full_list_to_clipboard)
        # Bigger problem than I thought
        # keyboard.add_hotkey('ctrl+shift+s', extract_phone_numbers(get_active_chrome_tab_url()))


    # Help window
    def show_instructions():
        help_window = tk.Toplevel(root)
        create_instructions_notebook(help_window)

    def show_hotkeys():
        hotkey_window = tk.Toplevel(root)
        create_hotkeys_notebook(hotkey_window)

    # background thread to listen for hot keys
    hotkey_thread = threading.Thread(target=setup_global_hotkey, daemon=True)
    hotkey_thread.start()


    # Create the main window
    root = tk.Tk()
    root.title("Number Crusher")
    root.bind("<Configure>", lambda event: on_resize(root, google_frame, autoMin))
    # ------------------------OLD BINDINGS----------------------

    # # binding for number feed
    # root.bind('<Control-f>', feed_next_number)

    # # binding for control + f + a to feed all numbers
    # root.bind('<Control-Shift-F>', full_list_to_clipboard)
    # ------------------------OLD BINDINGS----------------------


    # Create a menu bar
    menu_bar = tk.Menu(root)

    # Create a "Help" menu
    help_menu = tk.Menu(menu_bar)
    help_menu.add_command(label="Instructions", command=show_instructions)
    help_menu.add_command(label="HotKeys", command=show_hotkeys)
    menu_bar.add_cascade(label="Help", menu=help_menu)

    # Configure the root window to use the menu bar
    root.config(menu=menu_bar)

    # Create a frame to hold the Google search input and button
    google_frame = tk.Frame(root)
    inGoogleLbl = tk.Label(google_frame, text="Google")
    inGoogleText = tk.Text(google_frame, height=1, width=30)
    inGoogleText.bind("<Return>", on_return)
    outGoogleBtn = tk.Button(google_frame, text=" See Results", command=lambda: displaySearchResults(root, googleResults, potential_phone_nums))
    inGoogleLbl.grid(row=0, column=0, padx=10, pady=2, sticky="w")
    inGoogleText.grid(row=0, column=1, padx=10, pady=5, sticky="w")
    outGoogleBtn.grid(row=1, column=0, columnspan=2, padx=(10,10), pady=5, sticky="e")

    # frame for area code and auto minimize check box
    areaCodeAndMinFrame = tk.Frame(root)

    # Text input field for Area Code Checker
    inLabelAreaCode = tk.Label(areaCodeAndMinFrame, text="Check Area Code")
    inEntryAreaCode = tk.Text(areaCodeAndMinFrame, height=1, width=10)
    inEntryAreaCode.bind("<Return>", on_return)
    outLabelAreaCode = tk.Label(areaCodeAndMinFrame)


    # Text input field for DeDupe
    inLabelDeDup = tk.Label(root, text="DeDupe")
    #inLabelDeDup.pack(padx=5, pady=2)

    inEntryDeDup = tk.Text(root, height=10)
    inEntryDeDup.bind("<Return>", on_return)

    #Label to display all possible states with area codes from DeDup
    possibleStatesLbl = tk.Label(root)


    # Text input field for bad number Deleter
    inLabelDelete = tk.Label(root, text="Clean Numbers")


    inEntryDelete = tk.Text(root, height=10)
    inEntryDelete.bind("<Return>", on_return)



    # Create a frame to contain the button
    evalBtnFrame = tk.Frame(root)
    evalBtn = tk.Button(evalBtnFrame, text="Crush!", height=1, width=30, command=lambda: inEntryDelete.event_generate('<Return>'))
    evalBtn.grid(row=0, column=0, padx=10, pady=2, sticky="w")

    # make a check box to turn auto minimizing on and off
    onOff = tk.IntVar()
    autoMin = tk.Checkbutton(evalBtnFrame, text="Auto Minimize ON/OFF", variable=onOff, onvalue=1, offvalue=0)
    autoMin.grid(row=0, column=1, padx=10, pady=2, sticky="w")

    # inLabelAreaCode
    # inEntryAreaCode 
    # outLabelAreaCode 

    # Layout in frame using grid
    inLabelAreaCode.grid(row=0, column=0, padx=10, pady=2, sticky="w")
    inEntryAreaCode.grid(row=0, column=1, padx=10, pady=3, sticky="w")
    #autoMin.grid(row=0, column=2, columnspan=1, padx=(0, 30), pady=(0, 30), sticky="w")
    outLabelAreaCode.grid(row=1, column=0, columnspan=1, padx=5, pady=3, sticky="e")


    inLabelDeDup.grid(row=2, column=0, padx=10, pady=2, sticky="w")
    inEntryDeDup.grid(row=3, column=0, columnspan=3, padx=10, pady=3, sticky="ew")
    possibleStatesLbl.grid(row=4, column=0, columnspan=3, padx=10, pady=3, sticky="ew")

    inLabelDelete.grid(row=5, column=0, padx=10, pady=2, sticky="w")
    inEntryDelete.grid(row=6, column=0, padx=10, columnspan=3, pady=3, sticky="ew")

    #Frame to hold the area code and auto minimize check box
    areaCodeAndMinFrame.grid(row=1, column=0, columnspan=3, pady=3, sticky="ew")
    evalBtnFrame.grid(row=7, column=0, columnspan=3, pady=3)
    google_frame.grid(row=0, column=0, columnspan=3, pady=3, sticky="ew")


    # Configure column and row weights for resizing
    areaCodeAndMinFrame.grid_columnconfigure(1, weight=1)
    root.grid_columnconfigure(0, weight=1)
    root.grid_columnconfigure(1, weight=1)
    root.grid_rowconfigure(1, weight=1)
    root.grid_rowconfigure(2, weight=1)
    root.grid_rowconfigure(3, weight=1)
    root.grid_rowconfigure(4, weight=1)
    root.grid_rowconfigure(5, weight=1)
    root.grid_rowconfigure(6, weight=1)


    # auto minimized the console window
    ctypes.windll.user32.ShowWindow(
        ctypes.windll.kernel32.GetConsoleWindow(), 6
    )  # 6 = SW_MINIMIZE
    # info on .ShowWindow here:
    # https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-showwindow?redirectedfrom=MSDN


    root.mainloop()

if __name__ == "__main__":
    if sys.argv[-1] == "run_as_script":
        main()
    else:
        import subprocess
        subprocess.Popen([sys.executable, __file__, "run_as_script"], creationflags=subprocess.CREATE_NO_WINDOW)