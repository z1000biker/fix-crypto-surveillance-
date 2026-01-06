from tkinter import ttk
import tkinter as tk

class CasesTab:
    def __init__(self, parent, app=None):
        self.frame = parent
        self.app = app
        self.setup_ui()

    def setup_ui(self):
        columns = ("case_id", "participant", "instrument", "status", "priority", "created")
        self.tree = ttk.Treeview(self.frame, columns=columns, show="headings")
        
        for col in columns:
            self.tree.heading(col, text=col.capitalize())
            
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)
        
        btn_frame = ttk.Frame(self.frame)
        btn_frame.pack(fill="x", padx=10, pady=5)
        
        self.btn_open = ttk.Button(btn_frame, text="Open Case", command=self.on_open)
        self.btn_open.pack(side="left", padx=5)
        
        self.btn_investigate = ttk.Button(btn_frame, text="Start Investigation", command=self.on_investigate)
        self.btn_investigate.pack(side="left", padx=5)
        
        self.btn_close = ttk.Button(btn_frame, text="Close Case", command=self.on_close)
        self.btn_close.pack(side="left", padx=5)

    def add_case(self, case):
        # Store case data for later retrieval
        if not hasattr(self, 'cases'):
            self.cases = {}
        
        case_id = case.get("id", "")
        self.cases[case_id] = case
        
        values = (
            case_id,
            case.get("participant", ""),
            case.get("instrument", ""),
            case.get("status", ""),
            case.get("priority", ""),
            case.get("created", "")
        )
        self.tree.insert("", 0, values=values)

    def on_open(self):
        print("Open Case clicked")

    def on_investigate(self):
        selection = self.tree.selection()
        if not selection:
            return
        
        item = self.tree.item(selection[0])
        case_id = item['values'][0]
        
        if hasattr(self, 'cases') and case_id in self.cases:
            case = self.cases[case_id]
            rule_type = case.get('rule_type', 'UNKNOWN')
            
            # Format rule-specific details
            if rule_type == "SPOOFING":
                violation_desc = "Large orders were placed and then cancelled to manipulate market perception."
            elif rule_type == "WASH_TRADING":
                violation_desc = "Matched buy/sell orders detected, indicating artificial volume creation."
            elif "ANOMALY" in rule_type:
                violation_desc = "Machine learning model detected unusual trading patterns."
            else:
                violation_desc = "Trading pattern deviates from normal behavior."
            
            details = f"""CASE INVESTIGATION
{'=' * 60}

Case ID: {case.get('id', 'N/A')}
Participant: {case.get('participant', 'N/A')}
Instrument: {case.get('instrument', 'N/A')}
Status: {case.get('status', 'N/A')}
Priority: {case.get('priority', 'N/A')}
ML Score: {case.get('score', 'N/A')}

VIOLATION TYPE: {rule_type}

DESCRIPTION:
{violation_desc}

RECOMMENDATION:
This case requires manual review. The violation type indicates potential
market manipulation that needs investigation.

NEXT STEPS:
1. Review all trades from this participant for the flagged instrument
2. Check for similar patterns across other participants  
3. Document findings and escalate to compliance if confirmed
4. Consider account restriction if pattern continues
"""
            if self.app and hasattr(self.app, 'case_details_view'):
                self.app.case_details_view.show_case(details)
                # Switch to Case Details tab
                self.app.notebook.select(3)

    def on_close(self):
        print("Close clicked")

