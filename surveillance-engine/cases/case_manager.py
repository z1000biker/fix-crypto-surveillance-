import uuid
from datetime import datetime
from enum import Enum
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Optional

class CaseStatus(str, Enum):
    OPEN = "OPEN"
    INVESTIGATE = "INVESTIGATE"
    CLOSED = "CLOSED"

@dataclass
class CaseEvent:
    timestamp: str
    actor: str
    action: str
    details: Dict

@dataclass
class SurveillanceCase:
    case_id: str
    participant_id: str
    instrument: str
    status: str # CaseStatus
    priority: str
    ml_score: float
    created_at: str
    events: List[CaseEvent] = field(default_factory=list)
    resolution: Optional[str] = None
    alerts: List[Dict] = field(default_factory=list)

class CaseManager:
    def __init__(self):
        self.cases: Dict[str, SurveillanceCase] = {}

    def open_case(self, participant_id: str, instrument: str, alerts: List[Dict], ml_score: float, priority: str) -> SurveillanceCase:
        case_id = str(uuid.uuid4())
        
        case = SurveillanceCase(
            case_id=case_id,
            participant_id=participant_id,
            instrument=instrument,
            status=CaseStatus.OPEN.value,
            priority=priority,
            ml_score=ml_score,
            created_at=datetime.utcnow().isoformat(),
            alerts=alerts
        )
        
        case.events.append(CaseEvent(
            timestamp=datetime.utcnow().isoformat(),
            actor="SYSTEM",
            action="CASE_OPENED",
            details={"alert_count": len(alerts), "trigger_score": ml_score}
        ))
        
        self.cases[case_id] = case
        return case

    def start_investigation(self, case_id: str, analyst_id: str):
        case = self.cases.get(case_id)
        if not case:
            raise ValueError("Case not found")
            
        case.status = CaseStatus.INVESTIGATE.value
        case.events.append(CaseEvent(
            timestamp=datetime.utcnow().isoformat(),
            actor=analyst_id,
            action="INVESTIGATION_STARTED",
            details={}
        ))

    def close_case(self, case_id: str, analyst_id: str, resolution: str):
        case = self.cases.get(case_id)
        if not case:
            raise ValueError("Case not found")
            
        case.status = CaseStatus.CLOSED.value
        case.resolution = resolution
        case.events.append(CaseEvent(
            timestamp=datetime.utcnow().isoformat(),
            actor=analyst_id,
            action="CASE_CLOSED",
            details={"resolution": resolution}
        ))
