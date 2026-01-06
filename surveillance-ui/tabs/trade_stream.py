from tkinter import ttk

class TradeStreamTab:
    def __init__(self, parent):
        self.frame = parent
        self.setup_ui()

    def setup_ui(self):
        columns = ("time", "venue", "instrument", "side", "price", "qty", "participant")
        self.tree = ttk.Treeview(self.frame, columns=columns, show="headings")
        
        for col in columns:
            self.tree.heading(col, text=col.capitalize())
            self.tree.column(col, width=100)
            
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

    def add_trade(self, trade):
        # trade is expected to be a dict or object with matching fields
        values = (
            trade.get("time", ""),
            trade.get("venue", ""),
            trade.get("instrument", ""),
            trade.get("side", ""),
            trade.get("price", ""),
            trade.get("qty", ""),
            trade.get("participant", "")
        )
        self.tree.insert("", 0, values=values)
