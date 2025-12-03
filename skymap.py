import tkinter as tk
from tkinter import scrolledtext, messagebox
import subprocess
import threading
import shlex
import webbrowser
import re

# --- Theming Constants ---
BG_COLOR = "#212121" 
SCROLL_BG = "#e3dac9" 
INK_COLOR = "#2f261d" 
TEXT_COLOR = "#f2f2f2"
ACCENT_COLOR = "#cba135"
LINK_COLOR = "#00008B" # Dark Blue for clickable magic links

class SkyrimNmapGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("The Elder Scans: Legendary Edition")
        self.root.geometry("750x700")
        self.root.configure(bg=BG_COLOR)
        
        # Store current target for link generation
        self.current_scan_target = ""

        # --- Title ---
        tk.Label(
            root, 
            text="THU'UM SCANNER", 
            font=("Times New Roman", 22, "bold"),
            bg=BG_COLOR, 
            fg=TEXT_COLOR
        ).pack(pady=15)

        # --- Input Frame ---
        self.input_frame = tk.Frame(root, bg=BG_COLOR)
        self.input_frame.pack(pady=5)

        tk.Label(self.input_frame, text="Target:", font=("Arial", 12), bg=BG_COLOR, fg=TEXT_COLOR).pack(side=tk.LEFT, padx=5)
        
        self.target_entry = tk.Entry(self.input_frame, font=("Courier New", 12), width=20)
        self.target_entry.pack(side=tk.LEFT, padx=5)
        self.target_entry.insert(0, "127.0.0.1")

        # --- Options Frame ---
        self.options_frame = tk.LabelFrame(
            root, 
            text=" Active Runes ", 
            font=("Times New Roman", 10),
            bg=BG_COLOR, 
            fg=ACCENT_COLOR,
            bd=2,
            relief="groove"
        )
        self.options_frame.pack(pady=10, padx=20, fill="x")

        self.var_sv = tk.BooleanVar()
        self.var_sc = tk.BooleanVar()
        self.var_os = tk.BooleanVar()

        chk_options = {
            "bg": BG_COLOR, "fg": TEXT_COLOR, "selectcolor": "#444",
            "activebackground": BG_COLOR, "activeforeground": ACCENT_COLOR,
            "font": ("Arial", 10)
        }

        tk.Checkbutton(self.options_frame, text="Version (-sV)", variable=self.var_sv, **chk_options).pack(side=tk.LEFT, padx=10)
        tk.Checkbutton(self.options_frame, text="Scripts (-sC)", variable=self.var_sc, **chk_options).pack(side=tk.LEFT, padx=10)
        tk.Checkbutton(self.options_frame, text="OS Detect (-O)", variable=self.var_os, **chk_options).pack(side=tk.LEFT, padx=10)

        tk.Label(self.options_frame, text="Custom Spells:", bg=BG_COLOR, fg=ACCENT_COLOR).pack(side=tk.LEFT, padx=(20, 5))
        self.custom_entry = tk.Entry(self.options_frame, font=("Courier New", 10), width=15, bg="#333", fg="white", insertbackground="white")
        self.custom_entry.pack(side=tk.LEFT, padx=5)

        # --- Cast Button ---
        self.scan_button = tk.Button(
            root, 
            text="CAST SCAN", 
            font=("Arial", 11, "bold"),
            command=self.start_scan_thread,
            bg="#444", 
            fg=TEXT_COLOR,
            activebackground=ACCENT_COLOR,
            activeforeground="#000",
            relief="groove",
            bd=2,
            width=20
        )
        self.scan_button.pack(pady=5)

        # --- The Scroll ---
        self.scroll_frame = tk.Frame(root, bg="#5c4d3c", bd=5, relief="ridge")
        self.scroll_frame.pack(pady=15, padx=20, fill=tk.BOTH, expand=True)

        self.output_area = scrolledtext.ScrolledText(
            self.scroll_frame, 
            width=70, 
            height=20, 
            font=("Courier New", 11, "bold"),
            bg=SCROLL_BG, 
            fg=INK_COLOR,
            bd=0,
            cursor="arrow"
        )
        self.output_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        
        # Configure the "Hyperlink" style tag
        self.output_area.tag_config("hyperlink", foreground=LINK_COLOR, underline=1)
        # Bind the click event to the function
        self.output_area.tag_bind("hyperlink", "<Button-1>", self.on_link_click)
        # Change cursor to hand when hovering over link
        self.output_area.tag_bind("hyperlink", "<Enter>", lambda e: self.output_area.config(cursor="hand2"))
        self.output_area.tag_bind("hyperlink", "<Leave>", lambda e: self.output_area.config(cursor="arrow"))

        self.print_to_scroll("Select your runes and cast the spell...\n")

    def print_to_scroll(self, text):
        self.output_area.insert(tk.END, text)
        self.output_area.see(tk.END)
        self.highlight_links() # Scan for new links every time text is added

    def highlight_links(self):
        """Finds patterns and turns them into clickable links"""
        # 1. Regex for Nmap Ports (e.g. 80/tcp, 8080/tcp)
        port_pattern = r"(\d+)/tcp"
        
        # 2. Regex for full URLs (http://...)
        url_pattern = r"(http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+)"

        # Search and tag Ports
        start_index = "1.0"
        while True:
            count = tk.IntVar()
            # Search for pattern
            pos = self.output_area.search(port_pattern, start_index, stopindex=tk.END, count=count, regexp=True)
            if not pos: break
            
            # Calculate end position of the match
            end_index = f"{pos}+{count.get()}c"
            
            # Add the 'hyperlink' tag to this text range
            self.output_area.tag_add("hyperlink", pos, end_index)
            
            # Store the specific URL for this tag instance using a unique tag
            # We construct a unique tag name like "url_http://10.10.10.1:80"
            matched_text = self.output_area.get(pos, end_index)
            port_num = matched_text.split('/')[0]
            target_url = f"http://{self.current_scan_target}:{port_num}"
            
            # Add a hidden tag that contains the URL data
            self.output_area.tag_add(f"url_{target_url}", pos, end_index)
            
            start_index = end_index

        # Search and tag URLs (raw links found by scripts)
        start_index = "1.0"
        while True:
            count = tk.IntVar()
            pos = self.output_area.search(url_pattern, start_index, stopindex=tk.END, count=count, regexp=True)
            if not pos: break
            end_index = f"{pos}+{count.get()}c"
            
            self.output_area.tag_add("hyperlink", pos, end_index)
            
            matched_url = self.output_area.get(pos, end_index)
            self.output_area.tag_add(f"url_{matched_url}", pos, end_index)
            
            start_index = end_index

    def on_link_click(self, event):
        # Get the index of the character clicked
        index = self.output_area.index(f"@{event.x},{event.y}")
        
        # Get all tags at that index
        tags = self.output_area.tag_names(index)
        
        # Find the tag that starts with 'url_'
        for tag in tags:
            if tag.startswith("url_"):
                url = tag[4:] # Strip 'url_' prefix
                print(f"Opening: {url}") # Debug print to terminal
                try:
                    # Try to get Firefox specifically
                    try:
                        webbrowser.get('firefox').open_new_tab(url)
                    except webbrowser.Error:
                        # Fallback to default browser if 'firefox' keyword fails
                        webbrowser.open_new_tab(url)
                except Exception as e:
                    messagebox.showerror("Magic Failed", f"Could not open browser:\n{e}")
                break

    def start_scan_thread(self):
        target = self.target_entry.get()
        if not target:
            messagebox.showwarning("Missing Reagent", "You must provide a Target IP!")
            return

        self.current_scan_target = target # Save for link generation
        self.scan_button.config(state=tk.DISABLED, text="CHANNELLING...")
        self.output_area.delete('1.0', tk.END)
        self.print_to_scroll(f"--- Focusing Magicka on {target} ---\n")

        scan_thread = threading.Thread(target=self.run_nmap, args=(target,))
        scan_thread.daemon = True
        scan_thread.start()

    def run_nmap(self, target):
        # Removed -F, defaults to top 1000 ports now
        command = ["nmap"] 
        
        if self.var_sv.get():
            command.append("-sV")
        if self.var_sc.get():
            command.append("-sC")
        if self.var_os.get():
            command.append("-O")
        
        # Add Verbose so user sees ports as they pop up (better for clicking)
        command.append("-v") 

        custom_args = self.custom_entry.get().strip()
        if custom_args:
            command.extend(shlex.split(custom_args))
            
        command.append(target)

        self.root.after(0, self.print_to_scroll, f"Invoking: {' '.join(command)}\n\n")

        try:
            process = subprocess.Popen(
                command, 
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE, 
                text=True
            )

            while True:
                output = process.stdout.readline()
                if output == '' and process.poll() is not None:
                    break
                if output:
                    self.root.after(0, self.print_to_scroll, output)
            
            self.root.after(0, self.scan_finished)

        except Exception as e:
            self.root.after(0, self.print_to_scroll, f"\n[!] Fizzled: {str(e)}")
            self.root.after(0, self.scan_finished)

    def scan_finished(self):
        self.print_to_scroll("\n--- Ritual Complete ---")
        self.scan_button.config(state=tk.NORMAL, text="CAST SCAN")

if __name__ == "__main__":
    root = tk.Tk()
    app = SkyrimNmapGUI(root)
    root.mainloop()
