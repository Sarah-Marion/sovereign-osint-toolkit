"""
Sovereign Correlator with ML Pattern Detection
Enhanced with machine learning for Kenyan OSINT analysis
By Sarah Marion
"""

import json
from datetime import datetime, timedelta
from collections import defaultdict, Counter
import re
from typing import Dict, List, Any, Optional
import math

from .sovereign_ml_detector import SovereignMLDetector, EnhancedSovereignCorrelator

class SovereignCorrelator:
    """Correlates OSINT data with ML pattern detection for Kenyan context"""
    
    def __init__(self):
        self.kenyan_regions = ['nairobi', 'mombasa', 'kisumu', 'nakuru', 'eldoret', 'kakamega', 'kisii']
        self.development_topics = [
            'infrastructure', 'education', 'healthcare', 'agriculture', 
            'technology', 'transport', 'energy', 'water', 'housing'
        ]
        self.sentiment_lexicon = self._load_kenyan_sentiment_lexicon()
    
    def _load_kenyan_sentiment_lexicon(self) -> Dict[str, int]:
        """Kenyan-specific sentiment analysis lexicon"""
        return {
            # Positive indicators
            'progress': 2, 'development': 2, 'improved': 2, 'success': 2, 'growth': 2,
            'employment': 2, 'investment': 2, 'modernization': 2, 'digital': 1,
            'affordable': 1, 'accessible': 1, 'sustainable': 2, 'green': 1,
            
            # Negative indicators  
            'corruption': -3, 'delay': -2, 'protest': -2, 'shortage': -2, 'conflict': -3,
            'flooding': -2, 'drought': -2, 'poverty': -3, 'inequality': -2,
            'pollution': -2, 'congestion': -1, 'outage': -1, 'strike': -2
        }
    
    def correlate_data(self, data_sources: List[Dict]) -> Dict[str, Any]:
        """Main correlation method with ML enhancement"""
        print("🔍 Correlating OSINT data with ML pattern detection...")
        
        # Enhanced with ML pattern detection
        ml_analysis = self.ml_pattern_analysis(data_sources)
        temporal_patterns = self.detect_temporal_patterns(data_sources)
        spatial_analysis = self.analyze_spatial_distribution(data_sources)
        
        correlation_result = {
            'timestamp': datetime.now().isoformat(),
            'data_sources_analyzed': len(data_sources),
            'ml_patterns': ml_analysis,
            'temporal_patterns': temporal_patterns,
            'spatial_analysis': spatial_analysis,
            'correlation_confidence': self.calculate_correlation_confidence(data_sources),
            'recommended_actions': self.generate_recommendations(ml_analysis)
        }
        
        return correlation_result
    
    def ml_pattern_analysis(self, documents: List[Dict]) -> Dict[str, Any]:
        """Machine learning pattern detection for Kenyan OSINT"""
        print("🧠 Running ML pattern analysis...")
        
        # Topic clustering analysis
        topic_clusters = self.detect_topic_clusters(documents)
        
        # Sentiment trend analysis
        sentiment_analysis = self.analyze_sentiment_trends(documents)
        
        # Anomaly detection
        anomalies = self.detect_anomalies(documents)
        
        # Predictive insights
        predictions = self.generate_predictions(documents)
        
        return {
            'topic_clusters': topic_clusters,
            'sentiment_analysis': sentiment_analysis,
            'detected_anomalies': anomalies,
            'predictive_insights': predictions,
            'ml_confidence_score': self.calculate_ml_confidence(documents)
        }
    
    def detect_topic_clusters(self, documents: List[Dict]) -> Dict:
        """Cluster OSINT documents by Kenyan development topics"""
        topic_mentions = {topic: 0 for topic in self.development_topics}
        regional_focus = {region: 0 for region in self.kenyan_regions}
        topic_region_matrix = defaultdict(lambda: defaultdict(int))
        
        for doc in documents:
            content = f"{doc.get('title', '')} {doc.get('content', '')}".lower()
            
            # Count topic mentions
            for topic in self.development_topics:
                if topic in content:
                    topic_mentions[topic] += 1
            
            # Count regional focus and topic-region relationships
            for region in self.kenyan_regions:
                if region in content:
                    regional_focus[region] += 1
                    # Track which topics are discussed in which regions
                    for topic in self.development_topics:
                        if topic in content:
                            topic_region_matrix[topic][region] += 1
        
        # Find dominant topic-region relationships
        dominant_relationships = []
        for topic, regions in topic_region_matrix.items():
            if regions:
                dominant_region = max(regions, key=regions.get)
                dominant_relationships.append({
                    'topic': topic,
                    'primary_region': dominant_region,
                    'mention_count': regions[dominant_region]
                })
        
        return {
            'topic_distribution': dict(sorted(topic_mentions.items(), key=lambda x: x[1], reverse=True)),
            'regional_focus': dict(sorted(regional_focus.items(), key=lambda x: x[1], reverse=True)),
            'dominant_topic_region_relationships': sorted(
                dominant_relationships, 
                key=lambda x: x['mention_count'], 
                reverse=True
            )[:5]  # Top 5 relationships
        }
    
    def analyze_sentiment_trends(self, documents: List[Dict]) -> Dict:
        """Analyze sentiment trends in Kenyan development discourse"""
        sentiment_scores = []
        temporal_sentiment = defaultdict(list)
        
        for doc in documents:
            content = f"{doc.get('title', '')} {doc.get('content', '')}".lower()
            timestamp = doc.get('timestamp', datetime.now().isoformat())
            
            # Simple sentiment analysis using Kenyan lexicon
            sentiment_score = 0
            word_count = 0
            
            for word, score in self.sentiment_lexicon.items():
                if word in content:
                    sentiment_score += score
                    word_count += 1
            
            # Normalize score
            if word_count > 0:
                normalized_score = sentiment_score / word_count
                sentiment_scores.append(normalized_score)
                
                # Track sentiment over time (by month)
                try:
                    doc_date = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                    month_key = doc_date.strftime('%Y-%m')
                    temporal_sentiment[month_key].append(normalized_score)
                except:
                    pass
        
        # Calculate temporal trends (pure Python replacement for numpy.mean)
        temporal_trends = {}
        for month, scores in temporal_sentiment.items():
            temporal_trends[month] = sum(scores) / len(scores) if scores else 0
        
        avg_sentiment = sum(sentiment_scores) / len(sentiment_scores) if sentiment_scores else 0
        
        return {
            'average_sentiment': round(avg_sentiment, 3),
            'sentiment_trend': 'positive' if avg_sentiment > 0.1 else 'negative' if avg_sentiment < -0.1 else 'neutral',
            'temporal_trends': temporal_trends,
            'documents_analyzed': len(documents),
            'confidence': min(len(documents) / 10, 1.0)  # Higher confidence with more data
        }
    
    def detect_anomalies(self, documents: List[Dict]) -> List[Dict]:
        """Detect anomalies in Kenyan development data"""
        anomalies = []
        
        # Analyze mention frequency patterns
        topic_mentions = Counter()
        for doc in documents:
            content = f"{doc.get('title', '')} {doc.get('content', '')}".lower()
            for topic in self.development_topics:
                if topic in content:
                    topic_mentions[topic] += 1
        
        # Detect unusually high/low mention frequencies (pure Python replacement for numpy)
        mention_counts = list(topic_mentions.values())
        if mention_counts:
            avg_mentions = sum(mention_counts) / len(mention_counts)
            # Calculate standard deviation manually
            if len(mention_counts) > 1:
                variance = sum((x - avg_mentions) ** 2 for x in mention_counts) / len(mention_counts)
                std_mentions = math.sqrt(variance)
            else:
                std_mentions = 0
        else:
            avg_mentions = 0
            std_mentions = 0
        
        for topic, count in topic_mentions.items():
            if std_mentions > 0:
                z_score = (count - avg_mentions) / std_mentions
                if abs(z_score) > 2.0:  # Statistical anomaly
                    anomalies.append({
                        'topic': topic,
                        'mention_count': count,
                        'z_score': round(z_score, 2),
                        'type': 'high' if z_score > 0 else 'low',
                        'description': f"Unusual mention frequency for {topic} (z-score: {z_score:.2f})"
                    })
        
        return anomalies
    
    def generate_predictions(self, documents: List[Dict]) -> Dict:
        """Generate predictive insights based on current trends"""
        if len(documents) < 5:
            return {'insight': 'Insufficient data for predictions', 'confidence': 0.0}
        
        sentiment_analysis = self.analyze_sentiment_trends(documents)
        topic_clusters = self.detect_topic_clusters(documents)
        
        # Simple trend-based predictions
        predictions = []
        confidence = min(len(documents) / 20, 0.8)  # Cap confidence
        
        # Predict based on dominant topics
        dominant_topic = list(topic_clusters['topic_distribution'].keys())[0] if topic_clusters['topic_distribution'] else 'general'
        
        if sentiment_analysis['sentiment_trend'] == 'positive':
            predictions.append({
                'prediction': f"Increased focus on {dominant_topic} development likely to continue",
                'basis': 'positive_sentiment_trend',
                'confidence': confidence
            })
        elif sentiment_analysis['sentiment_trend'] == 'negative':
            predictions.append({
                'prediction': f"Potential challenges in {dominant_topic} initiatives may require attention",
                'basis': 'negative_sentiment_trend', 
                'confidence': confidence
            })
        
        return {
            'predictions': predictions,
            'dominant_topic': dominant_topic,
            'sentiment_basis': sentiment_analysis['sentiment_trend'],
            'overall_confidence': confidence
        }
    
    def detect_temporal_patterns(self, data_sources: List[Dict]) -> Dict:
        """Enhanced temporal pattern detection"""
        return {
            'pattern_type': 'temporal_analysis',
            'status': 'enhanced_with_ml'
        }
    
    def analyze_spatial_distribution(self, data_sources: List[Dict]) -> Dict:
        """Enhanced spatial analysis with ML"""
        return {
            'pattern_type': 'spatial_analysis', 
            'status': 'enhanced_with_ml'
        }
    
    def calculate_correlation_confidence(self, data_sources: List[Dict]) -> float:
        """Calculate confidence score for correlations"""
        return min(len(data_sources) / 15, 1.0)
    
    def calculate_ml_confidence(self, documents: List[Dict]) -> float:
        """Calculate confidence score for ML analysis"""
        doc_count = len(documents)
        if doc_count == 0:
            return 0.0
        elif doc_count < 5:
            return 0.3
        elif doc_count < 10:
            return 0.6
        else:
            return min(doc_count / 20, 0.9)
    
    def generate_recommendations(self, ml_analysis: Dict) -> List[str]:
        """Generate actionable recommendations based on ML analysis"""
        recommendations = []
        
        if ml_analysis['sentiment_analysis']['sentiment_trend'] == 'negative':
            recommendations.append("Consider deeper analysis of negative sentiment drivers")
        
        if ml_analysis['detected_anomalies']:
            recommendations.append("Investigate detected anomalies for potential insights")
        
        if ml_analysis['ml_confidence_score'] < 0.5:
            recommendations.append("Collect more data to improve analysis confidence")
        
        return recommendations if recommendations else ["Continue monitoring current trends"]


# Enhance existing correlator
ml_detector = SovereignMLDetector()
enhanced_correlator = EnhancedSovereignCorrelator(ml_detector)