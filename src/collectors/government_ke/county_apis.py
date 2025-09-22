"""
County-specific government data collectors
Understanding that Kenya's 47 counties have different data landscapes
"""

class CountyDataCollector:
    """Collector tailored to county government structures"""
    
    def __init__(self):
        self.county_capabilities = {
            "nairobi": {
                "api_available": True,
                "data_quality": "high",
                "sensitive_areas": ["land_rates", "housing_projects"]
            },
            "mombasa": {
                "api_available": True,
                "data_quality": "medium", 
                "sensitive_areas": ["port_operations", "tourism_data"]
            },
            "mandera": {
                "api_available": False,
                "data_quality": "low",
                "sensitive_areas": ["security_operations", "border_issues"]
            }
        }
    
    def collect_county_development_data(self, county_name: str):
        """Collect development data with conflict sensitivity"""
        if county_name in ["mandera", "wajir", "garissa"]:
            # Special ethical considerations for Northern counties
            return self._collect_with_security_sensitivity(county_name)
        return self._standard_county_collection(county_name)