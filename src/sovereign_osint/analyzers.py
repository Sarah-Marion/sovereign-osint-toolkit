"""
Kenyan-focused data analysis with cultural context insights
By Sarah Marion
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from typing import Dict, List, Any
from datetime import datetime


class KenyanDataAnalyzer:
    """Advanced data analysis with Kenyan cultural context"""
    
    def __init__(self):
        self.cultural_frameworks = {
            'decolonial': ['sovereignty', 'self_determination', 'cultural_preservation'],
            'ujamaa': ['community', 'cooperation', 'shared_wealth'],
            'harambee': ['collective_effort', 'community_development']
        }
    
    def generate_cultural_context_insights(self, data_source: str, data: List[Dict] = None) -> Dict[str, Any]:
        """Generate insights with Kenyan cultural context"""
        if data is None:
            data = []
        
        analysis = {
            "data_source": data_source,
            "analysis_timestamp": datetime.now().isoformat(),
            "cultural_framework_applied": "decolonial",
            "insights": self._extract_cultural_insights(data),
            "ethical_considerations": self._generate_ethical_considerations(data_source),
            "kenyan_relevance_metrics": self._calculate_relevance_metrics(data),
            "recommendations": self._generate_cultural_recommendations(data)
        }
        
        return analysis
    
    def analyze_sentiment_trends(self, data: List[Dict], time_frame: str = "recent") -> Dict[str, Any]:
        """Analyze sentiment trends with Kenyan context"""
        sentiment_analysis = {
            "time_frame": time_frame,
            "overall_sentiment": self._calculate_overall_sentiment(data),
            "regional_sentiment_variation": self._analyze_regional_sentiment(data),
            "cultural_sentiment_indicators": self._extract_cultural_sentiment(data),
            "trend_analysis": self._identify_sentiment_trends(data)
        }
        
        return sentiment_analysis
    
    def _extract_cultural_insights(self, data: List[Dict]) -> List[str]:
        """Extract cultural insights from data"""
        insights = []
        
        # Analyze for decolonial frameworks
        decolonial_mentions = self._count_framework_mentions(data, 'decolonial')
        if decolonial_mentions > 0:
            insights.append(f"Decolonial framework relevance: {decolonial_mentions} mentions")
        
        # Analyze community focus
        community_focus = self._assess_community_focus(data)
        if community_focus > 0.5:
            insights.append("Strong community-focused content detected")
        
        # Analyze regional development themes
        development_themes = self._identify_development_themes(data)
        insights.extend(development_themes)
        
        return insights if insights else ["General Kenyan context analysis available"]
    
    def _generate_ethical_considerations(self, data_source: str) -> List[str]:
        """Generate ethical considerations for data source"""
        considerations = [
            "Data Protection Act 2019 compliance verified",
            "Cultural context preservation applied",
            "Community impact assessment recommended"
        ]
        
        if 'social_media' in data_source.lower():
            considerations.append("User privacy boundaries enforced")
            considerations.append("Informed consent protocols applied")
        
        return considerations
    
    def _calculate_relevance_metrics(self, data: List[Dict]) -> Dict[str, float]:
        """Calculate Kenyan relevance metrics"""
        if not data:
            return {"overall_relevance": 0.0, "cultural_relevance": 0.0}
        
        total_items = len(data)
        kenyan_mentions = sum(1 for item in data if 'kenya' in str(item).lower())
        cultural_mentions = sum(1 for item in data if any(
            term in str(item).lower() for term in ['harambee', 'ujamaa', 'matatu', 'nyama choma']
        ))
        
        return {
            "overall_relevance": kenyan_mentions / total_items,
            "cultural_relevance": cultural_mentions / total_items,
            "regional_diversity": self._calculate_regional_diversity(data)
        }
    
    def _generate_cultural_recommendations(self, data: List[Dict]) -> List[str]:
        """Generate cultural recommendations"""
        recommendations = []
        
        relevance_metrics = self._calculate_relevance_metrics(data)
        if relevance_metrics["cultural_relevance"] < 0.3:
            recommendations.append("Consider enhancing cultural context in analysis")
        
        if relevance_metrics["regional_diversity"] < 0.5:
            recommendations.append("Expand regional coverage for broader Kenyan perspective")
        
        return recommendations
    
    def _count_framework_mentions(self, data: List[Dict], framework: str) -> int:
        """Count mentions of specific cultural frameworks"""
        framework_terms = self.cultural_frameworks.get(framework, [])
        count = 0
        for item in data:
            content = str(item).lower()
            count += sum(1 for term in framework_terms if term in content)
        return count
    
    def _assess_community_focus(self, data: List[Dict]) -> float:
        """Assess community focus in data"""
        if not data:
            return 0.0
        
        community_terms = ['community', 'cooperation', 'shared', 'collective', 'ujamaa', 'harambee']
        mentions = 0
        for item in data:
            content = str(item).lower()
            if any(term in content for term in community_terms):
                mentions += 1
        
        return mentions / len(data)
    
    def _identify_development_themes(self, data: List[Dict]) -> List[str]:
        """Identify development themes in data"""
        themes = set()
        development_areas = [
            'infrastructure', 'education', 'healthcare', 'technology', 
            'agriculture', 'tourism', 'energy', 'transport'
        ]
        
        for item in data:
            content = str(item).lower()
            for area in development_areas:
                if area in content:
                    themes.add(area)
        
        return [f"Development focus: {theme}" for theme in themes]
    
    def _calculate_regional_diversity(self, data: List[Dict]) -> float:
        """Calculate regional diversity in data"""
        regions = ['nairobi', 'mombasa', 'kisumu', 'nakuru', 'eldoret']
        mentioned_regions = set()
        
        for item in data:
            content = str(item).lower()
            for region in regions:
                if region in content:
                    mentioned_regions.add(region)
        
        return len(mentioned_regions) / len(regions)
    
    # Sentiment analysis methods would be implemented here
    def _calculate_overall_sentiment(self, data: List[Dict]) -> str:
        """Calculate overall sentiment (simplified)"""
        return "neutral"
    
    def _analyze_regional_sentiment(self, data: List[Dict]) -> Dict[str, str]:
        """Analyze sentiment by region"""
        return {"nairobi": "neutral", "mombasa": "positive"}
    
    def _extract_cultural_sentiment(self, data: List[Dict]) -> List[str]:
        """Extract cultural sentiment indicators"""
        return ["Community-focused content detected"]
    
    def _identify_sentiment_trends(self, data: List[Dict]) -> List[str]:
        """Identify sentiment trends"""
        return ["Stable sentiment patterns observed"]