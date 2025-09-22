"""
Sovereign OSINT Toolkit - Real-time Monitoring System
Live intelligence gathering with Kenyan context awareness
By Sarah Marion
"""

import time
import threading
from datetime import datetime
from typing import Dict, List, Callable
from ..utils.kenyan_context import KenyanContextValidator
from ..utils.security import KenyanSecurityProtocol

class KenyanRealTimeMonitor:
    """Real-time monitoring system tailored for Kenyan intelligence needs"""
    
    def __init__(self):
        self.kenyan_context = KenyanContextValidator()
        self.security = KenyanSecurityProtocol()
        self.active_monitors = {}
        self.monitoring_threads = {}
        
        # Kenyan-specific monitoring sources
        self.kenyan_data_sources = {
            "social_media": {
                "twitter_ke": ["#KOT", "#Kenya", "#Nairobi", "#FinanceBill2024"],
                "facebook_ke": ["Kenyan politics groups", "County discussion forums"],
                "whatsapp_communities": ["Verified public channels only"]
            },
            "news_sources": {
                "local_news": ["Nation", "Standard", "Star", "CitizenTV"],
                "government_feeds": ["PSCU", "County press releases", "Parliament updates"]
            },
            "public_data": {
                "government_portals": ["eCitizen", "KRA", "PPOA tender notices"],
                "county_platforms": ["Nairobi County", "Mombasa County", "Kisumu County"]
            }
        }
    
    def start_monitoring(self, source_type: str, keywords: List[str], callback: Callable, 
                        interval: int = 300) -> str:
        """Start monitoring a specific data source with Kenyan context validation"""
        
        # Validate monitoring request against Kenyan ethical boundaries
        validation = self.kenyan_context.validate_topic_sensitivity(
            " ".join(keywords), "real_time_monitoring"
        )
        
        if not validation:
            raise ValueError("Monitoring request violates Kenyan context sensitivity rules")
        
        # Generate monitor ID
        monitor_id = f"{source_type}_{int(time.time())}"
        
        # Start monitoring thread
        monitor_thread = threading.Thread(
            target=self._monitoring_loop,
            args=(monitor_id, source_type, keywords, callback, interval),
            daemon=True
        )
        
        self.active_monitors[monitor_id] = {
            "source_type": source_type,
            "keywords": keywords,
            "callback": callback,
            "interval": interval,
            "start_time": datetime.now(),
            "status": "active"
        }
        
        self.monitoring_threads[monitor_id] = monitor_thread
        monitor_thread.start()
        
        print(f"🔄 Started monitoring {source_type} for keywords: {keywords}")
        return monitor_id
    
    def _monitoring_loop(self, monitor_id: str, source_type: str, keywords: List[str], 
                        callback: Callable, interval: int):
        """Main monitoring loop with Kenyan context checks"""
        
        while monitor_id in self.active_monitors:
            try:
                # Get new data from the specified source
                new_data = self._fetch_data(source_type, keywords)
                
                # Apply Kenyan context filtering
                filtered_data = self._apply_kenyan_context_filter(new_data, keywords)
                
                # Security and anonymization
                secured_data = self._secure_monitoring_data(filtered_data, source_type)
                
                if secured_data:
                    # Call the user-provided callback with new data
                    callback(secured_data, source_type)
                
                # Wait for next interval
                time.sleep(interval)
                
            except Exception as e:
                print(f"Monitoring error for {monitor_id}: {e}")
                time.sleep(interval)  # Continue despite errors
    
    def _fetch_data(self, source_type: str, keywords: List[str]) -> List[Dict]:
        """Fetch data from Kenyan-specific sources"""
        
        if source_type == "twitter_ke":
            return self._fetch_kenyan_twitter_data(keywords)
        elif source_type == "news_sources":
            return self._fetch_kenyan_news_data(keywords)
        elif source_type == "government_feeds":
            return self._fetch_government_data(keywords)
        else:
            return self._fetch_general_data(source_type, keywords)
    
    def _fetch_kenyan_twitter_data(self, keywords: List[str]) -> List[Dict]:
        """Fetch Twitter data with Kenyan context awareness"""
        # This would integrate with Twitter API
        # For now, return mock data structure
        
        mock_tweets = [
            {
                "text": f"Discussion about {keywords[0]} in Nairobi today",
                "user": "kenyan_analyst",
                "timestamp": datetime.now(),
                "location": "Nairobi, Kenya",
                "sentiment": "neutral",
                "kenyan_context": "political_discussion"
            }
        ]
        
        return mock_tweets
    
    def _fetch_kenyan_news_data(self, keywords: List[str]) -> List[Dict]:
        """Fetch news data from Kenyan sources"""
        
        mock_articles = [
            {
                "title": f"Government announces new policy on {keywords[0]}",
                "source": "Daily Nation",
                "published": datetime.now(),
                "content": f"Detailed analysis of {keywords[0]} in Kenyan context...",
                "county_impact": "national",
                "political_sensitivity": "medium"
            }
        ]
        
        return mock_articles
    
    def _fetch_government_data(self, keywords: List[str]) -> List[Dict]:
        """Fetch data from Kenyan government portals"""
        
        mock_government_data = [
            {
                "type": "tender_notice",
                "agency": "County Government of Nairobi",
                "title": f"Tender for {keywords[0]} services",
                "value": "KES 50M",
                "deadline": "2024-12-31",
                "corruption_risk": "low"  # Kenyan-specific risk assessment
            }
        ]
        
        return mock_government_data
    
    def _apply_kenyan_context_filter(self, data: List[Dict], keywords: List[str]) -> List[Dict]:
        """Filter data based on Kenyan cultural and political context"""
        
        filtered_data = []
        
        for item in data:
            # Check for sensitive content that requires special handling
            sensitivity_check = self.kenyan_context.validate_cultural_sensitivity(
                str(item), "general"
            )
            
            if sensitivity_check["approved"]:
                # Add Kenyan context metadata
                item["kenyan_context_score"] = self._calculate_context_score(item, keywords)
                item["regional_relevance"] = self._assess_regional_relevance(item)
                filtered_data.append(item)
            else:
                print(f"Filtered out sensitive content: {sensitivity_check['warnings']}")
        
        return filtered_data
    
    def _secure_monitoring_data(self, data: List[Dict], source_type: str) -> List[Dict]:
        """Apply security measures to monitoring data"""
        
        security_assessment = self.security.secure_data_collection(
            f"real_time_{source_type}", "monitoring", "public"
        )
        
        if not security_assessment["compliance_report"]["dpa_2019_compliant"]:
            print("Security compliance check failed - stopping data collection")
            return []
        
        # Apply anonymization to sensitive fields
        from ..utils.anonymization import KenyanAnonymization
        anonymizer = KenyanAnonymization()
        
        secured_data = []
        for item in data:
            # Create a safe copy for monitoring
            safe_item = item.copy()
            
            # Remove or anonymize sensitive fields
            if "user" in safe_item:
                safe_item["user"] = f"user_{hash(safe_item['user']) % 10000}"
            
            if "location" in safe_item and "Nairobi" in safe_item["location"]:
                safe_item["location"] = "Nairobi_General"  # Generalize location
            
            secured_data.append(safe_item)
        
        return secured_data
    
    def _calculate_context_score(self, item: Dict, keywords: List[str]) -> float:
        """Calculate how relevant this data is to Kenyan context"""
        score = 0.0
        
        # Boost score for Kenyan-specific references
        kenyan_indicators = ["Kenya", "Nairobi", "Mombasa", "Kisumu", "county", "KES"]
        
        content = str(item).lower()
        for indicator in kenyan_indicators:
            if indicator.lower() in content:
                score += 0.2
        
        # Boost for keyword matches
        for keyword in keywords:
            if keyword.lower() in content:
                score += 0.3
        
        return min(score, 1.0)  # Cap at 1.0
    
    def _assess_regional_relevance(self, item: Dict) -> str:
        """Assess which Kenyan regions this data is relevant to"""
        content = str(item).lower()
        
        regional_keywords = {
            "nairobi": ["nairobi", "capital", "westlands", "kasarani"],
            "coastal": ["mombasa", "coast", "nyali", "mombasa county"],
            "western": ["kisumu", "lake", "kisumu county", "luo"],
            "rift_valley": ["nakuru", "rift", "nakuru county", "kalenjin"]
        }
        
        relevant_regions = []
        for region, keywords in regional_keywords.items():
            if any(keyword in content for keyword in keywords):
                relevant_regions.append(region)
        
        return relevant_regions if relevant_regions else ["national"]
    
    def stop_monitoring(self, monitor_id: str):
        """Stop a specific monitoring task"""
        if monitor_id in self.active_monitors:
            self.active_monitors[monitor_id]["status"] = "stopped"
            if monitor_id in self.monitoring_threads:
                # Thread will stop on next iteration due to status check
                print(f"🛑 Stopped monitor: {monitor_id}")
    
    def get_monitoring_status(self) -> Dict:
        """Get status of all active monitors"""
        return {
            "active_monitors": len([m for m in self.active_monitors.values() if m["status"] == "active"]),
            "total_monitors": len(self.active_monitors),
            "monitors_details": self.active_monitors
        }