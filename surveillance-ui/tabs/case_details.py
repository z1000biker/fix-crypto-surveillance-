from tkinter import ttk
import tkinter as tk

class CaseDetailsTab:
    def __init__(self, parent):
        self.frame = parent
        self.setup_ui()

    def setup_ui(self):
        self.text_area = tk.Text(self.frame, state="disabled", wrap="word", font=("Consolas", 10))
        self.text_area.pack(fill="both", expand=True, padx=10, pady=10)

    def show_case(self, case_details):
        self.text_area.config(state="normal")
        self.text_area.delete(1.0, "end")
        self.text_area.insert("end", case_details)
        self.text_area.config(state="disabled")
