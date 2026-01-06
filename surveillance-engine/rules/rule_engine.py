import yaml
import os
from typing import List, Dict, Any

class RuleEngine:
    def __init__(self, rules_dir: str):
        self.rules = []
        self.load_rules(rules_dir)

    def load_rules(self, rules_dir: str):
        if not os.path.exists(rules_dir):
            return
            
        for filename in os.listdir(rules_dir):
            if filename.endswith(".yaml") or filename.endswith(".yml"):
                with open(os.path.join(rules_dir, filename), "r") as f:
                    rule_def = yaml.safe_load(f)
                    self.rules.append(rule_def)

    def evaluate(self, metrics: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Evaluates all loaded rules against a participant's metrics.
        Returns a list of triggered alerts.
        """
        alerts = []
        for rule in self.rules:
            if self._check_rule(rule, metrics):
                alerts.append({
                    "rule_id": rule.get("id"),
                    "type": rule.get("alert_type"),
                    "severity": rule.get("severity"),
                    "description": rule.get("description")
                })
        return alerts

    def _check_rule(self, rule: Dict, metrics: Dict) -> bool:
        """
        Interprets the DSL 'when' conditions.
        Supported operators: >, <, >=, <=, ==
        """
        conditions = rule.get("when", {})
        for metric_name, condition in conditions.items():
            if metric_name not in metrics:
                continue
                
            value = metrics[metric_name]
            
            # Simple DSL parsing (e.g. "> 0.7")
            try:
                op, threshold = condition.split()
                threshold = float(threshold)
                
                if op == ">" and not (value > threshold): return False
                if op == "<" and not (value < threshold): return False
                if op == ">=" and not (value >= threshold): return False
                if op == "<=" and not (value <= threshold): return False
                if op == "==" and not (value == threshold): return False
            except:
                # Fallback or error logging
                return False
                
        return True
