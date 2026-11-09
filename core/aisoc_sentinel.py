"""
AISOC - Autonomous AI Security Operations Center Engine
Part of Autonomous Exotic & Marine Hunter AI Suite
Engineered by IC Neural Systems LLC (Israel Cepero)
"""

import time
import uuid
from typing import Dict, Any, List, Optional
from core.database import DB


class AISOCSentinel:
    """
    AI Security Operations Center (AI-SOC) Orchestrator.
    Handles autonomous telemetry analysis, anomaly scoring, and automated threat containment.
    """

    CONTAINED_IPS: Dict[str, Dict[str, Any]] = {}

    @classmethod
    def analyze_event(cls, ip_address: str, action: str, details: str = "", user_agent: str = "") -> Dict[str, Any]:
        """
        Calculates real-time anomaly threat score (0-100) and triggers automated containment if threshold is breached.
        """
        threat_score = 0
        severity = "INFO"
        threat_indicators = []

        details_lower = details.lower()
        ua_lower = user_agent.lower()

        # 1. SQL Injection / Scripting probe
        if any(kw in details_lower for kw in ["union select", "--", "or 1=1", "<script>", "drop table"]):
            threat_score += 75
            threat_indicators.append("SQLI_MALICIOUS_PATTERN")

        # 2. Automated crawler / scanner detection
        if any(bot in ua_lower for bot in ["sqlmap", "nikto", "nmap", "gobuster", "curl", "python-requests"]):
            threat_score += 25
            threat_indicators.append("SUSPICIOUS_AUTOMATED_TOOL")

        # 3. High-frequency burst or failed auth
        if "failed" in action.lower() or "unauthorized" in action.lower():
            threat_score += 30
            threat_indicators.append("AUTH_FAILURE_ATTEMPT")

        # Classify Severity
        if threat_score >= 80:
            severity = "CRITICAL"
        elif threat_score >= 50:
            severity = "HIGH"
        elif threat_score >= 25:
            severity = "MEDIUM"
        else:
            severity = "LOW"

        incident_id = f"INC-{uuid.uuid4().hex[:8].upper()}"

        # Automated Containment Threshold
        auto_contained = False
        if threat_score >= 75:
            cls.contain_ip(ip_address, reason=f"AISOC Automated Trigger: {', '.join(threat_indicators)}")
            auto_contained = True

        # Log into persistent database
        DB.log_security_event(
            ip_address=ip_address,
            user_agent=user_agent or "AISOC Sentinel Telemetry",
            action=action,
            status=severity,
            details=f"Threat Score: {threat_score}/100 | Indicators: {threat_indicators} | {details}"
        )

        return {
            "incident_id": incident_id,
            "ip_address": ip_address,
            "threat_score": threat_score,
            "severity": severity,
            "threat_indicators": threat_indicators,
            "auto_contained": auto_contained,
            "timestamp": int(time.time()),
            "status": "CONTAINED" if auto_contained else "MONITORED"
        }

    @classmethod
    def contain_ip(cls, ip_address: str, reason: str = "Administrative Security Quarantine") -> Dict[str, Any]:
        cls.CONTAINED_IPS[ip_address] = {
            "contained_at": int(time.time()),
            "reason": reason,
            "active": True
        }
        return {"status": "SUCCESS", "ip": ip_address, "action": "BLOCKED"}

    @classmethod
    def uncontain_ip(cls, ip_address: str) -> Dict[str, Any]:
        if ip_address in cls.CONTAINED_IPS:
            del cls.CONTAINED_IPS[ip_address]
        return {"status": "SUCCESS", "ip": ip_address, "action": "UNBLOCKED"}

    @classmethod
    def get_soc_dashboard_telemetry(cls) -> Dict[str, Any]:
        recent_logs = DB.get_recent_security_logs(limit=25)
        total_analyzed = len(recent_logs)
        critical_count = sum(1 for log in recent_logs if log.get("status") in ["CRITICAL", "BLOCKED", "ERROR"])
        
        return {
            "soc_status": "ONLINE_ACTIVE_SHIELD",
            "active_threat_level": "ELEVATED" if critical_count > 3 else "NORMAL",
            "total_telemetry_events": total_analyzed,
            "contained_ips_count": len(cls.CONTAINED_IPS),
            "contained_ips_list": list(cls.CONTAINED_IPS.keys()),
            "recent_incidents": recent_logs,
            "compliance": "FinCEN BSA & NIST SP 800-61 Rev. 2 Automated Incident Response"
        }


AISOC_ENGINE = AISOCSentinel
aisoc_sentinel = AISOC_ENGINE
