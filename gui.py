import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog
import requests
import json
import io  


try:
    from PIL import Image, ImageTk
    import cairosvg
    SVG_SUPPORT = True
except ImportError:
    SVG_SUPPORT = False
    print("Warning: Pillow or CairoSVG not found. Icons will not be loaded.")

from analyzer import run_full_analysis
from error_analyzer import run_error_analysis


def load_svg_icon(path, size=(20, 20)):
    if not SVG_SUPPORT:
        return None
    try:
       
        png_data = cairosvg.svg2png(url=path, output_width=size[0], output_height=size[1])
        
       
        image = Image.open(io.BytesIO(png_data))
        
        
        return ImageTk.PhotoImage(image)
    except (FileNotFoundError, Exception) as e:
        print(f"Warning: Could not load icon at {path}. Error: {e}")
        return None

class DebuggerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("eSim AI Debugging Tool")
        self.geometry("900x700")

        self._setup_styles()

        sidebar_frame = ttk.Frame(self, width=220, style="Sidebar.TFrame")
        sidebar_frame.pack(side="left", fill="y", padx=(10, 0), pady=10)
        sidebar_frame.pack_propagate(False)

        ttk.Label(sidebar_frame, text="Analysis Tools", font=("Segoe UI", 14, "bold"), style="Sidebar.TLabel").pack(pady=(10, 15), padx=15, anchor="w")

        
        self.netlist_icon = load_svg_icon("icons/netlist_icon.svg")
        self.log_icon = load_svg_icon("icons/log_icon.svg")

        btn_netlist = ttk.Button(sidebar_frame, text="  Analyze Netlist", image=self.netlist_icon, compound="left", command=self.analyze_netlist_file, style="Sidebar.TButton")
        btn_netlist.pack(fill="x", padx=15, pady=5)

        btn_log = ttk.Button(sidebar_frame, text="  Analyze Log File", image=self.log_icon, compound="left", command=self.analyze_log_file, style="Sidebar.TButton")
        btn_log.pack(fill="x", padx=15, pady=5)

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        
        self.analysis_tab = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(self.analysis_tab, text="Analysis Report")
        self.report_text = scrolledtext.ScrolledText(self.analysis_tab, wrap=tk.WORD, state="disabled", font=("Consolas", 10), bg="#2B2B2B", fg="#D3D3D3", insertbackground="white", borderwidth=0, highlightthickness=0)
        self.report_text.pack(fill="both", expand=True)

        self.chat_tab = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(self.chat_tab, text="AI Chatbot")
        
        self.chat_history = scrolledtext.ScrolledText(self.chat_tab, wrap=tk.WORD, state="disabled", font=("Segoe UI", 10), bg="#2B2B2B", fg="#D3D3D3", insertbackground="white", borderwidth=0, highlightthickness=0)
        self.chat_history.pack(fill="both", expand=True, pady=(0, 10))

        chat_input_frame = ttk.Frame(self.chat_tab)
        chat_input_frame.pack(fill="x")
        self.chat_input = ttk.Entry(chat_input_frame, font=("Segoe UI", 10))
        self.chat_input.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.chat_input.bind("<Return>", self.send_chat_message)
        self.btn_send = ttk.Button(chat_input_frame, text="Send", command=self.send_chat_message)
        self.btn_send.pack(side="left")

    def _setup_styles(self):
        BG_COLOR = "#1C1C1C"
        SIDEBAR_BG = "#252526"
        CONTENT_BG = "#1E1E1E"
        FG_COLOR = "#CCCCCC"
        BTN_BG = "#333333"
        BTN_FG = "#FFFFFF"
        BTN_HOVER = "#454545"
        ACCENT_COLOR = "#007ACC"
        
        self.configure(bg=BG_COLOR)
        style = ttk.Style(self)
        style.theme_use('clam')

        style.configure(".", background=BG_COLOR, foreground=FG_COLOR, font=("Segoe UI", 10))
        style.configure("TFrame", background=CONTENT_BG)
        style.configure("Sidebar.TFrame", background=SIDEBAR_BG)
        style.configure("Sidebar.TLabel", background=SIDEBAR_BG, foreground=FG_COLOR)
        
        style.configure("TButton", background=BTN_BG, foreground=BTN_FG, borderwidth=0, padding=8, font=("Segoe UI", 10))
        style.map("TButton", background=[('active', ACCENT_COLOR), ('hover', BTN_HOVER)])

        style.configure("Sidebar.TButton", padding=10, anchor="w", font=("Segoe UI", 11))

        style.configure("TEntry", fieldbackground="#2D2D2D", foreground=FG_COLOR, borderwidth=1, insertcolor="white")

        style.configure("TNotebook", background=BG_COLOR, borderwidth=0)
        style.configure("TNotebook.Tab", background=BTN_BG, foreground=FG_COLOR, padding=[12, 6], borderwidth=0, font=("Segoe UI", 10, "bold"))
        style.map("TNotebook.Tab", background=[("selected", ACCENT_COLOR)], foreground=[("selected", BTN_FG)])

    def analyze_netlist_file(self):
        filepath = filedialog.askopenfilename()
        if not filepath: return
        report = run_full_analysis(filepath)
        self._display_report(report)
        self.notebook.select(self.analysis_tab)

    def analyze_log_file(self):
        filepath = filedialog.askopenfilename()
        if not filepath: return
        report = run_error_analysis(filepath)
        self.notebook.select(self.analysis_tab)
        self._display_report(report)

    def send_chat_message(self, event=None):
        user_message = self.chat_input.get()
        if not user_message.strip(): return
        self._append_to_chat(f"You: {user_message}\n")
        self.chat_input.delete(0, tk.END)
        self.update_idletasks()
        try:
            payload = {"model": "qwen:4b", "prompt": user_message, "stream": False}
            response = requests.post("http://localhost:11434/api/generate", json=payload)
            response.raise_for_status()
            ai_answer = response.json().get("response", "No response from model.")
            self._append_to_chat(f"AI: {ai_answer}\n\n")
        except requests.exceptions.RequestException as e:
            self._append_to_chat(f"Error: Could not connect to Ollama. Make sure it's running.\nDetails: {e}\n\n")

    def _display_report(self, report_text):
        self.report_text.config(state="normal")
        self.report_text.delete(1.0, tk.END)
        self.report_text.insert(tk.END, report_text)
        self.report_text.config(state="disabled")

    def _append_to_chat(self, text):
        self.chat_history.config(state="normal")
        self.chat_history.insert(tk.END, text)
        self.chat_history.yview(tk.END)
        self.chat_history.config(state="disabled")

if __name__ == "__main__":
    app = DebuggerApp()
    app.mainloop()
