from googlesearch import search
import tkinter as tk
from tkinter import ttk
import webbrowser
from numberScraper import extract_phone_numbers

def googleSearch(inGoogleText):
    global googleResults, potential_phone_nums
    # Clear out the list of results before starting a new search
    googleResults = []
    phone_nums = []
    input = inGoogleText.get("1.0", "end-1c")
    if input != "":
        query = input
        for j in search(query, num=2, stop=5, pause=0.2):
            phone_nums.append(extract_phone_numbers(j))
            googleResults.append(j)

        # clear out the input
        inGoogleText.delete("1.0", "end")
    return googleResults, phone_nums


def displaySearchResults(root, googleResults, phone_nums_all_urls):
    if googleResults or phone_nums_all_urls:
        # Create a new window
        new_window = tk.Toplevel(root)
        new_window.title("Results")

        # Create a PanedWindow
        paned_window = ttk.PanedWindow(new_window, orient=tk.HORIZONTAL)
        paned_window.pack(fill=tk.BOTH, expand=True)

        # Left pane for search results
        left_frame = ttk.Frame(paned_window)
        paned_window.add(left_frame, weight=1)

        phone_label = ttk.Label(left_frame, text="Top 5 URLs")
        phone_label.pack(pady=(10, 5))

        results_text = tk.Text(left_frame, width=50, height=20, wrap=tk.WORD)
        results_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        if googleResults:
            for result in googleResults:
                results_text.insert(tk.END, result + "\n\n", "hyperlink")
                tag_name = f"hyperlink-{result}"
                results_text.tag_add(tag_name, "end-3l", "end-1c")
                results_text.tag_config(tag_name, foreground="blue", underline=1)
                results_text.tag_bind(tag_name, "<Button-1>", lambda e, url=result: open_url(url))

        results_text.config(state=tk.DISABLED)

        # Right pane for phone numbers
        if phone_nums_all_urls:
            right_frame = ttk.Frame(paned_window)
            paned_window.add(right_frame, weight=1)

            phone_label = ttk.Label(right_frame, text="Phone Numbers from URLs:")
            phone_label.pack(pady=(10, 5))

            phone_text = tk.Text(right_frame, width=30, height=20, wrap=tk.WORD)
            phone_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

            
            for phone_nums in phone_nums_all_urls:
                for num in phone_nums:
                    phone_text.insert(tk.END, num[1] + "-" + num[2] + "-" + num[3] + "\n") 

            phone_text.config(state=tk.DISABLED)

def open_url(url):
    webbrowser.open(url)