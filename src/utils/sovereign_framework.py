"""
Sovereign Framework Implementation for OSINT
Based on Sarah Marion's ethical framework for decolonial data practices
"""
from .kenyan_context import KenyanContextValidator


class EthicalViolation(Exception):
    """Raised when Sovereign Framework is violated"""
    pass

class SovereignEthicalFramework:
    """
    Main ethical framework implementing Sarah Marion's Sovereign Principles
    Sovereignty, Guardianship, Reciprocity
    """
    
    def __init__(self):
        self.kenyan_context = KenyanContextValidator()  # This should work now
        self.boundaries = self._load_ethical_boundaries()
    
    def _load_ethical_boundaries(self) -> dict:
        """Load absolute prohibitions from config"""
        import json
        import os
        config_path = os.path.join(os.path.dirname(__file__), '..', '..', 'config', 'ethical_boundaries.json')
        with open(config_path, 'r') as f:
            return json.load(f)

class KenyanContextValidator:
    """Ensures operations respect Kenyan cultural and political context"""
    
    def __init__(self):
        self.sensitive_topics = [
            "tribal politics", "land disputes", "historical injustices",
            "election violence", "marginalized communities"
        ]
    
    def validate_topic_sensitivity(self, topic: str, methodology: str) -> bool:
        """Check if topic requires special ethical considerations"""
        topic_lower = topic.lower()
        
        for sensitive_topic in self.sensitive_topics:
            if sensitive_topic in topic_lower:
                if methodology not in ["academic_research", "public_interest_journalism"]:
                    raise EthicalViolation(
                        f"Topic '{topic}' requires approved methodology. "
                        f"Current methodology '{methodology}' not permitted."
                    )
        return True

class SovereignEthicalFramework:
    """
    Main ethical framework implementing Sarah Marion's Sovereign Framework
    Sovereignty, Guardianship, Reciprocity
    """
    
    def __init__(self):
        self.kenyan_context = KenyanContextValidator()
        self.boundaries = self._load_ethical_boundaries()
    
    def _load_ethical_boundaries(self) -> dict:
        """Load absolute prohibitions from config"""
        import json
        with open('config/ethical_boundaries.json', 'r') as f:
            return json.load(f)
    
    def pre_operation_check(self, target: str, purpose: str, methodology: str) -> dict:
        """
        Comprehensive ethical validation before any OSINT operation
        Returns approval decision with conditions
        """
        validation_report = {
            "approved": False,
            "conditions": [],
            "warnings": [],
            "required_consent_level": "none"
        }
        
        # Check absolute prohibitions first
        for prohibited_action in self.boundaries["never_do"]:
            if self._detects_prohibited_pattern(target, purpose, prohibited_action):
                raise EthicalViolation(
                    f"Operation violates Sovereign Framework: {prohibited_action}"
                )
        
        # Kenyan context validation
        try:
            self.kenyan_context.validate_topic_sensitivity(target, methodology)
            validation_report["approved"] = True
        except EthicalViolation as e:
            validation_report["warnings"].append(str(e))
            validation_report["approved"] = False
        
        # Set consent requirements based on sensitivity
        if "personal_data" in methodology:
            validation_report["required_consent_level"] = "explicit"
        elif "public_figure" in target:
            validation_report["required_consent_level"] = "implicit"
        
        return validation_report
    
    def _detects_prohibited_pattern(self, target: str, purpose: str, prohibition: str) -> bool:
        """Detect if operation matches prohibited patterns"""
        prohibited_patterns = {
            "personal_harassment": ["doxxing", "intimidation", "targeted harassment"],
            "financial_exploitation": ["financial gain", "fraud", "scam"],
            "government_subversion": ["overthrow", "undermine", "illegal protest"]
        }
        
        if prohibition in prohibited_patterns:
            for pattern in prohibited_patterns[prohibition]:
                if pattern in purpose.lower() or pattern in target.lower():
                    return True
        return False