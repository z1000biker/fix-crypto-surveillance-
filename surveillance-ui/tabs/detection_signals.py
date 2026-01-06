from tkinter import ttk

class DetectionSignalsTab:
    def __init__(self, parent):
        self.frame = parent
        self.setup_ui()

    def setup_ui(self):
        columns = ("time_window", "participant", "type", "desc", "severity")
        self.tree = ttk.Treeview(self.frame, columns=columns, show="headings")
        
        for col in columns:
            self.tree.heading(col, text=col.capitalize())
        
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Tag configuration for severity
        self.tree.tag_configure("HIGH", background="#ffcccc")
        self.tree.tag_configure("MEDIUM", background="#ffebcc")
        self.tree.tag_configure("LOW", background="#ffffcc")

    def add_signal(self, signal):
        values = (
            signal.get("time_window", ""),
            signal.get("participant", ""),
            signal.get("type", ""),
            signal.get("desc", ""),
            signal.get("severity", "")
        )
        self.tree.insert("", 0, values=values, tags=(signal.get("severity", "LOW"),))
