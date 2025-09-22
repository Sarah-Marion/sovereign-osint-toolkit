"""
Kenyan Context Validator for Sovereign OSINT Toolkit
Cultural, political, and linguistic context awareness for Kenyan intelligence operations
By Sarah Marion
"""

class KenyanContextValidator:
    """Ensures OSINT operations respect Kenyan cultural and political context"""
    
    def __init__(self):
        self.sensitive_topics = [
            "tribal politics", "land disputes", "historical injustices",
            "election violence", "marginalized communities", "resource allocation",
            "devolution conflicts", "historical land injustices"
        ]
        
        self.kenyan_linguistic_features = {
            "languages": ["Swahili", "English", "Sheng", "Local vernaculars"],
            "communication_styles": ["indirect", "respectful", "context-dependent"],
            "sensitive_terminology": ["majimbo", "ungwana", "historical grievances"]
        }
    
    def validate_topic_sensitivity(self, topic: str, methodology: str) -> bool:
        """Check if topic requires special ethical considerations for Kenyan context"""
        topic_lower = topic.lower()
        
        for sensitive_topic in self.sensitive_topics:
            if sensitive_topic in topic_lower:
                if methodology not in ["academic_research", "public_interest_journalism"]:
                    raise ValueError(
                        f"Topic '{topic}' requires approved methodology for Kenyan context. "
                        f"Current methodology '{methodology}' not permitted for sensitive topics."
                    )
        return True
    
    def validate_cultural_sensitivity(self, content: str, region: str = "general") -> dict:
        """Validate content for cultural appropriateness in specific Kenyan regions"""
        validation_result = {
            "approved": True,
            "warnings": [],
            "recommendations": []
        }
        
        # Region-specific cultural considerations
        regional_sensitivities = {
            "coastal": ["mijikenda_communities", "swahili_culture", "islamic_influences"],
            "central": ["kikuyu_business_networks", "agricultural_issues", "urban_rural_dynamics"],
            "rift_valley": ["land_issues", "pastoralist_communities", "ethnic_diversity"],
            "nairobi": ["urban_poor", "political_elites", "international_influences"]
        }
        
        # Check for potentially insensitive language
        insensitive_patterns = [
            "tribal stereotypes", "regional generalizations", 
            "historical simplifications", "cultural appropriations"
        ]
        
        content_lower = content.lower()
        for pattern in insensitive_patterns:
            if any(term in content_lower for term in pattern.split()):
                validation_result["warnings"].append(f"Potential {pattern} detected")
        
        return validation_result
    
    def get_region_context(self, county: str) -> dict:
        """Get specific cultural and political context for a Kenyan county"""
        county_contexts = {
            "nairobi": {
                "political_significance": "Capital city, national politics",
                "sensitivities": ["urban inequality", "housing rights", "political demonstrations"],
                "communication_norms": ["formal in business", "mixed Swahili/English", "fast-paced"]
            },
            "kisumu": {
                "political_significance": "Luo heartland, opposition stronghold",
                "sensitivities": ["lake resources", "fishing rights", "regional development"],
                "communication_norms": ["Dholuo influences", "respect for elders", "community-focused"]
            },
            "mombasa": {
                "political_significance": "Coastal economy, port city",
                "sensitivities": ["tourism economy", "islamic values", "land ownership"],
                "communication_norms": ["Swahili primary", "indirect communication", "hospitality emphasis"]
            }
        }
        
        return county_contexts.get(county.lower(), {
            "political_significance": "General Kenyan context",
            "sensitivities": self.sensitive_topics,
            "communication_norms": ["Respectful", "Context-aware", "Community-oriented"]
        })