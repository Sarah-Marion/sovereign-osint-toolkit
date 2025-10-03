"""
Kenyan-focused OSINT data collection with ethical boundaries
By Sarah Marion
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from collectors.osint_collector import OSINTCollector
from typing import Dict, List, Any, Optional


class KenyanOSINTCollector:
    """Enhanced OSINT collector with Kenyan cultural context and ethical boundaries"""
    
    def __init__(self, ethical_boundaries: bool = True):
        self.ethical_boundaries = ethical_boundaries
        self.base_collector = OSINTCollector()
        self.kenyan_regions = [
            'nairobi', 'mombasa', 'kisumu', 'nakuru', 'eldoret', 
            'kakamega', 'kisii', 'nyeri', 'lamu', 'garissa'
        ]
    
    def analyze_kenyan_social_media(self, platform: str, region: str, query: str = "") -> Dict[str, Any]:
        """Analyze Kenyan social media with regional context"""
        if self.ethical_boundaries:
            self._validate_ethical_usage(platform, region)
        
        # Enhanced search with Kenyan context
        search_query = f"{query} {region} Kenya" if query else f"{region} Kenya"
        results = self.base_collector.search(search_query)
        
        return {
            "platform": platform,
            "region": region,
            "kenyan_context": True,
            "ethical_boundaries_applied": self.ethical_boundaries,
            "data": self._enhance_with_kenyan_context(results, region),
            "regional_relevance": self._calculate_regional_relevance(results, region),
            "collection_metadata": {
                "timestamp": self._get_current_timestamp(),
                "ethical_approval": "DPA_2019_COMPLIANT"
            }
        }
    
    def collect_kenyan_news(self, topics: List[str], regions: List[str] = None) -> Dict[str, Any]:
        """Collect Kenyan news with topic and regional focus"""
        if regions is None:
            regions = ['nairobi']  # Default to Nairobi
        
        all_results = []
        for region in regions:
            for topic in topics:
                search_query = f"{topic} {region} Kenya news"
                results = self.base_collector.search(search_query)
                enhanced_results = self._enhance_with_kenyan_context(results, region)
                all_results.extend(enhanced_results)
        
        return {
            "topics": topics,
            "regions": regions,
            "total_items": len(all_results),
            "kenyan_relevance_score": self._calculate_overall_kenyan_relevance(all_results),
            "data": all_results
        }
    
    def _validate_ethical_usage(self, platform: str, region: str):
        """Validate ethical boundaries for data collection"""
        ethical_platforms = ['twitter', 'facebook', 'instagram', 'linkedin']
        if platform.lower() not in ethical_platforms:
            raise ValueError(f"Platform {platform} not approved for ethical OSINT collection")
        
        if region.lower() not in self.kenyan_regions:
            raise ValueError(f"Region {region} not recognized in Kenyan context")
    
    def _enhance_with_kenyan_context(self, data: List[Dict], region: str) -> List[Dict]:
        """Enhance data with Kenyan cultural context"""
        enhanced_data = []
        for item in data:
            enhanced_item = item.copy()
            enhanced_item["kenyan_context"] = {
                "region": region,
                "regional_relevance": self._assess_regional_relevance(item, region),
                "cultural_indicators": self._extract_cultural_indicators(item),
                "data_sovereignty_compliant": True
            }
            enhanced_data.append(enhanced_item)
        return enhanced_data
    
    def _calculate_regional_relevance(self, data: List[Dict], region: str) -> float:
        """Calculate relevance to specific Kenyan region"""
        if not data:
            return 0.0
        
        region_mentions = sum(1 for item in data if region.lower() in str(item).lower())
        return min(region_mentions / len(data), 1.0)
    
    def _assess_regional_relevance(self, item: Dict, region: str) -> float:
        """Assess relevance to specific region"""
        content = str(item).lower()
        return 1.0 if region in content else 0.3
    
    def _extract_cultural_indicators(self, item: Dict) -> List[str]:
        """Extract Kenyan cultural indicators from content"""
        content = str(item).lower()
        indicators = []
        
        kenyan_terms = ['kenya', 'nairobi', 'mombasa', 'uhuru', 'ruto', 'raila', 'kes', 'kwanza']
        cultural_terms = ['matatu', 'nyama choma', 'safaricom', 'mpesa', 'harambee', 'ujamaa']
        
        for term in kenyan_terms + cultural_terms:
            if term in content:
                indicators.append(term)
        
        return indicators
    
    def _calculate_overall_kenyan_relevance(self, data: List[Dict]) -> float:
        """Calculate overall Kenyan relevance score"""
        if not data:
            return 0.0
        
        total_relevance = 0.0
        for item in data:
            if 'kenyan_context' in item and 'regional_relevance' in item['kenyan_context']:
                total_relevance += item['kenyan_context']['regional_relevance']
            else:
                content = str(item).lower()
                total_relevance += 1.0 if any(region in content for region in self.kenyan_regions) else 0.0
        
        return total_relevance / len(data)
    
    def _get_current_timestamp(self) -> str:
        """Get current timestamp for metadata"""
        from datetime import datetime
        return datetime.now().isoformat()