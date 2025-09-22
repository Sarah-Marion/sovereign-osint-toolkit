"""
Informed Consent Management for Kenyan OSINT Operations
Based on Data Protection Act, 2019 requirements
"""

class ConsentManager:
    """Manages consent protocols for different data types and use cases"""
    
    def __init__(self):
        self.consent_levels = {
            "explicit": ["personal_data", "sensitive_topics", "vulnerable_groups"],
            "implicit": ["public_figures", "corporate_entities", "government_data"],
            "none": ["publicly_available", "statistical_aggregates", "historical_data"]
        }
    
    def get_consent_requirement(self, data_type: str, use_case: str) -> str:
        """Determine required consent level based on Kenyan context"""
        
        # Kenyan legal requirements take precedence
        if data_type in ["health_records", "financial_data", "minor_data"]:
            return "explicit"
        
        # Public interest journalism has different standards
        if use_case == "public_interest_journalism":
            if data_type in ["government_corruption", "public_safety"]:
                return "implicit"
        
        return self.consent_levels.get(data_type, "explicit")
    
    def generate_consent_template(self, data_subject: str, purpose: str) -> dict:
        """Generate culturally appropriate consent templates"""
        template = {
            "purpose_clear": f"We are collecting information about {data_subject} for {purpose}",
            "benefits_explained": "This research will contribute to...",
            "risks_disclosed": "Potential risks include...",
            "withdrawal_right": "You may withdraw consent at any time",
            "contact_local": "Contact our Nairobi office at...",
            "language_options": ["Swahili", "English", "Local dialect where available"]
        }
        return template