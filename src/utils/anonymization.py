"""
Kenyan Data Anonymization Protocols
Meeting Data Protection Act, 2019 requirements
By Sarah Marion
"""

import re
import hashlib
from typing import Dict, List, Any

class KenyanAnonymization:
    """Anonymization techniques suitable for Kenyan data contexts"""
    
    def __init__(self):
        self.kenyan_identifiers = {
            "national_id_patterns": [r"\d{8}", r"\d{1}-\d{4}-\d{5}"],  # Kenyan ID formats
            "phone_patterns": [r"07\d{8}", r"\+2547\d{8}", r"01\d{7}"],  # Kenyan numbers
            "vehicle_plates": [r"K[A-Z]{2} \d{3}[A-Z]", r"K[A-Z] \d{5}[A-Z]"],  # Kenyan plates
            "location_specific": [
                "estate_names", "landmark_references", "local_chief_areas",
                "ward_names", "constituency_offices"
            ]
        }
        
        self.kenyan_context_preservation_rules = {
            "county_level": "Preserve county information for regional analysis",
            "age_brackets": "Use 10-year brackets instead of exact ages",
            "income_ranges": "Use percentile brackets rather than exact figures",
            "professional_categories": "Use broad categories instead of specific titles"
        }
    
    def anonymize_dataset(self, dataset: List[Dict], context: str) -> List[Dict]:
        """Anonymize dataset while preserving Kenyan contextual utility"""
        
        anonymized_data = []
        
        for record in dataset:
            anonymized_record = self._anonymize_record(record, context)
            anonymized_data.append(anonymized_record)
        
        return self._apply_kenyan_context_preservation(anonymized_data, context)
    
    def _anonymize_record(self, record: Dict, context: str) -> Dict:
        """Anonymize individual record using Kenyan-specific rules"""
        
        anonymized = record.copy()
        
        # Remove direct identifiers
        for field in record.keys():
            if self._is_direct_identifier(field, record[field]):
                anonymized[field] = self._hash_value(record[field])
            elif self._is_quasi_identifier(field, record[field], context):
                anonymized[field] = self._generalize_value(field, record[field])
        
        return anonymized
    
    def _is_direct_identifier(self, field: str, value: Any) -> bool:
        """Check if field contains direct identifying information"""
        
        if not isinstance(value, str):
            return False
            
        value_str = str(value)
        
        # Check for Kenyan national ID patterns
        for pattern in self.kenyan_identifiers["national_id_patterns"]:
            if re.search(pattern, value_str):
                return True
        
        # Check for Kenyan phone numbers
        for pattern in self.kenyan_identifiers["phone_patterns"]:
            if re.search(pattern, value_str.replace(" ", "")):
                return True
        
        direct_identifier_fields = [
            "id_number", "national_id", "phone", "mobile", "email",
            "registration_number", "passport_number"
        ]
        
        return field.lower() in direct_identifier_fields
    
    def _is_quasi_identifier(self, field: str, value: Any, context: str) -> bool:
        """Check if field could lead to re-identification when combined"""
        
        quasi_identifiers = {
            "demographic": ["age", "gender", "location", "occupation"],
            "kenyan_specific": ["tribe", "religion", "political_affiliation", "land_ownership"],
            "contextual": ["income", "education_level", "employment_status"]
        }
        
        field_lower = field.lower()
        
        # Always consider Kenyan-specific sensitive attributes as quasi-identifiers
        for category in quasi_identifiers.values():
            if field_lower in category:
                return True
        
        return False
    
    def _hash_value(self, value: Any) -> str:
        """Hash value for anonymization while maintaining referential integrity"""
        value_str = str(value).encode('utf-8')
        return hashlib.sha256(value_str).hexdigest()[:16]  # Truncated for readability
    
    def _generalize_value(self, field: str, value: Any) -> Any:
        """Generalize value to prevent re-identification"""
        
        field_lower = field.lower()
        
        if field_lower == "age" and isinstance(value, (int, float)):
            # Group ages into 10-year brackets
            bracket = (value // 10) * 10
            return f"{bracket}-{bracket+9}"
        
        elif field_lower == "income" and isinstance(value, (int, float)):
            # Group income into percentile brackets
            brackets = ["0-20K", "20K-50K", "50K-100K", "100K-200K", "200K+"]
            for bracket in brackets:
                if "+" in bracket:
                    min_val = int(bracket.replace("K+", "000"))
                    if value >= min_val:
                        return bracket
                else:
                    min_val, max_val = map(lambda x: int(x.replace("K", "000")), bracket.split("-"))
                    if min_val <= value <= max_val:
                        return bracket
        
        elif field_lower == "location" and isinstance(value, str):
            # Generalize to county level only
            county_mapping = {
                "nairobi": ["westlands", "dagoretti", "langata", "kasarani"],
                "mombasa": ["nyali", "kisauni", "likoni", "mvita"],
                "kisumu": ["kisumu east", "kisumu west", "kisumu central"]
            }
            
            for county, areas in county_mapping.items():
                if any(area in value.lower() for area in areas):
                    return county.title()
            
            return "Generalized_Location"
        
        return "Generalized_Value"
    
    def _apply_kenyan_context_preservation(self, data: List[Dict], context: str) -> List[Dict]:
        """Ensure anonymized data remains useful for Kenyan analysis"""
        
        # For Kenyan contexts, preserve certain aggregations that are meaningful
        if context == "development_analysis":
            # Preserve county-level development indicators
            for record in data:
                if "county" in record:
                    record["development_region"] = self._map_to_development_region(record["county"])
        
        elif context == "political_analysis":
            # Preserve regional political affiliations at appropriate level
            for record in data:
                if "county" in record:
                    record["political_zone"] = self._map_to_political_zone(record["county"])
        
        return data
    
    def _map_to_development_region(self, county: str) -> str:
        """Map county to development region for analysis"""
        development_regions = {
            "nairobi": "metropolitan",
            "mombasa": "coastal_region", 
            "kisumu": "lake_region",
            "mandera": "northern_frontier",
            "garissa": "northern_frontier"
        }
        return development_regions.get(county.lower(), "other_region")
    
    def _map_to_political_zone(self, county: str) -> str:
        """Map county to political zone for analysis"""
        political_zones = {
            "nairobi": "central_government",
            "mombasa": "coastal_politics",
            "kisumu": "western_kenya",
            "nakuru": "rift_valley",
            "meru": "eastern_kenya"
        }
        return political_zones.get(county.lower(), "general_zone")