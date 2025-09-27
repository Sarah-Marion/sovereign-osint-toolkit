"""
Sovereign OSINT Toolkit - Machine Learning Pattern Detection
Lightweight ML integration for Kenyan context pattern recognition
By Sarah Marion
"""

import math
import statistics
from collections import defaultdict, Counter
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
import re
import json


class SovereignMLDetector:
    """Lightweight ML pattern detection for Kenyan OSINT data"""
    
    def __init__(self, config: Optional[Dict] = None):
        self.config = {
            "similarity_threshold": 0.7,
            "anomaly_std_threshold": 2.0,
            "cluster_min_size": 2,
            "kenyan_context_weight": 1.5,
            **({} if config is None else config)
        }
        
        # Kenyan-specific patterns and entities
        self.kenyan_entities = {
            'counties': ['nairobi', 'mombasa', 'kisumu', 'nakuru', 'eldoret', 'kakamega', 'kisii', 'nyeri'],
            'political_figures': ['ruto', 'raila', 'mudavadi', 'uhuru', 'odinga', 'kibaki', 'moi', 'rigathi'],
            'ethnic_communities': ['kalenjin', 'kikuyu', 'luo', 'luhya', 'kamba', 'kisii', 'meru', 'somali'],
            'economic_terms': ['kes', 'shilling', 'mpesa', 'safaricom', 'agriculture', 'tourism', 'economy', 'development'],
            'infrastructure': ['sgr', 'highway', 'port', 'airport', 'energy', 'water', 'road', 'construction']
        }

    def detect_patterns(self, data: List[Dict]) -> Dict[str, Any]:
        """Main pattern detection entry point"""
        
        patterns = {
            "clusters": self._cluster_related_events(data),
            "anomalies": self._detect_anomalies(data),
            "trends": self._analyze_trends(data),
            "entity_networks": self._build_entity_networks(data),
            "temporal_patterns": self._analyze_temporal_patterns(data)
        }
        
        # Calculate overall pattern significance
        patterns["pattern_significance"] = self._calculate_pattern_significance(patterns)
        
        return patterns

    def _cluster_related_events(self, data: List[Dict]) -> List[Dict]:
        """Cluster related events using lightweight similarity measures"""
        
        if len(data) < 2:
            return []
        
        clusters = []
        processed_indices = set()
        
        for i, item1 in enumerate(data):
            if i in processed_indices:
                continue
                
            cluster = [item1]
            processed_indices.add(i)
            
            for j, item2 in enumerate(data[i+1:], i+1):
                if j in processed_indices:
                    continue
                    
                similarity = self._calculate_similarity(item1, item2)
                if similarity >= self.config["similarity_threshold"]:
                    cluster.append(item2)
                    processed_indices.add(j)
            
            if len(cluster) >= self.config["cluster_min_size"]:
                clusters.append({
                    "events": cluster,
                    "cluster_score": self._calculate_cluster_score(cluster),
                    "common_themes": self._extract_common_themes(cluster),
                    "kenyan_relevance": self._calculate_cluster_kenyan_relevance(cluster)
                })
        
        return sorted(clusters, key=lambda x: x["cluster_score"], reverse=True)

    def _calculate_similarity(self, item1: Dict, item2: Dict) -> float:
        """Calculate similarity between two OSINT items using multiple factors"""
        
        similarities = []
        
        # Content similarity
        content_sim = self._text_similarity(
            self._extract_text(item1), 
            self._extract_text(item2)
        )
        similarities.append(content_sim * 0.4)
        
        # Entity similarity
        entity_sim = self._entity_similarity(item1, item2)
        similarities.append(entity_sim * 0.3)
        
        # Temporal similarity (closer in time = more similar)
        time_sim = self._temporal_similarity(item1, item2)
        similarities.append(time_sim * 0.2)
        
        # Geographic similarity
        geo_sim = self._geographic_similarity(item1, item2)
        similarities.append(geo_sim * 0.1)
        
        return sum(similarities)

    def _text_similarity(self, text1: str, text2: str) -> float:
        """Calculate text similarity using Jaccard similarity"""
        
        if not text1 or not text2:
            return 0.0
        
        # Simple word-based similarity
        words1 = set(re.findall(r'\w+', text1.lower()))
        words2 = set(re.findall(r'\w+', text2.lower()))
        
        if not words1 or not words2:
            return 0.0
        
        intersection = len(words1.intersection(words2))
        union = len(words1.union(words2))
        
        return intersection / union if union > 0 else 0.0

    def _entity_similarity(self, item1: Dict, item2: Dict) -> float:
        """Calculate similarity based on shared Kenyan entities"""
        
        entities1 = self._extract_kenyan_entities(item1)
        entities2 = self._extract_kenyan_entities(item2)
        
        if not entities1 or not entities2:
            return 0.0
        
        shared_entities = len(set(entities1).intersection(set(entities2)))
        max_entities = max(len(entities1), len(entities2))
        
        return shared_entities / max_entities

    def _extract_kenyan_entities(self, item: Dict) -> List[str]:
        """Extract Kenyan-specific entities from OSINT data"""
        
        text = self._extract_text(item).lower()
        entities = []
        
        for category, terms in self.kenyan_entities.items():
            for term in terms:
                if term in text:
                    entities.append(f"{category}:{term}")
        
        return entities

    def _temporal_similarity(self, item1: Dict, item2: Dict) -> float:
        """Calculate temporal similarity (closer in time = more similar)"""
        
        time1 = self._extract_timestamp(item1)
        time2 = self._extract_timestamp(item2)
        
        if not time1 or not time2:
            return 0.5  # Neutral similarity if timestamps missing
        
        time_diff = abs((time1 - time2).total_seconds())
        
        # Normalize: same day = 1.0, within week = 0.7, within month = 0.3
        if time_diff < 86400:  # 1 day
            return 1.0
        elif time_diff < 604800:  # 1 week
            return 0.7
        elif time_diff < 2592000:  # 1 month
            return 0.3
        else:
            return 0.1

    def _geographic_similarity(self, item1: Dict, item2: Dict) -> float:
        """Calculate geographic similarity based on Kenyan regions"""
        
        text1 = self._extract_text(item1).lower()
        text2 = self._extract_text(item2).lower()
        
        counties1 = [county for county in self.kenyan_entities['counties'] if county in text1]
        counties2 = [county for county in self.kenyan_entities['counties'] if county in text2]
        
        if not counties1 or not counties2:
            return 0.5  # Neutral if no geographic info
        
        # Same county = high similarity, different counties = low similarity
        return 1.0 if set(counties1) == set(counties2) else 0.2

    def _detect_anomalies(self, data: List[Dict]) -> List[Dict]:
        """Detect anomalous patterns in OSINT data"""
        
        if len(data) < 5:  # Need sufficient data for anomaly detection
            return []
        
        anomalies = []
        
        # Activity level anomalies
        activity_anomalies = self._detect_activity_anomalies(data)
        anomalies.extend(activity_anomalies)
        
        # Content anomalies
        content_anomalies = self._detect_content_anomalies(data)
        anomalies.extend(content_anomalies)
        
        # Temporal anomalies
        temporal_anomalies = self._detect_temporal_anomalies(data)
        anomalies.extend(temporal_anomalies)
        
        return anomalies

    def _detect_activity_anomalies(self, data: List[Dict]) -> List[Dict]:
        """Detect anomalies in activity levels"""
        
        # Group by time windows (hours)
        hourly_activity = defaultdict(int)
        for item in data:
            timestamp = self._extract_timestamp(item)
            if timestamp:
                hour_key = timestamp.replace(minute=0, second=0, microsecond=0)
                hourly_activity[hour_key] += 1
        
        if len(hourly_activity) < 3:
            return []
        
        activities = list(hourly_activity.values())
        mean_activity = statistics.mean(activities)
        std_activity = statistics.stdev(activities) if len(activities) > 1 else 0
        
        anomalies = []
        for hour, count in hourly_activity.items():
            if std_activity > 0 and abs(count - mean_activity) > self.config["anomaly_std_threshold"] * std_activity:
                anomalies.append({
                    "type": "activity_anomaly",
                    "timestamp": hour.isoformat(),
                    "activity_level": count,
                    "expected_range": f"{mean_activity:.1f} ± {std_activity:.1f}",
                    "anomaly_score": abs(count - mean_activity) / std_activity
                })
        
        return anomalies

    def _detect_content_anomalies(self, data: List[Dict]) -> List[Dict]:
        """Detect anomalies in content patterns"""
        
        # Analyze keyword frequencies
        all_keywords = []
        for item in data:
            text = self._extract_text(item)
            keywords = re.findall(r'\w+', text.lower())
            all_keywords.extend(keywords)
        
        keyword_freq = Counter(all_keywords)
        avg_freq = len(all_keywords) / len(data) if data else 0
        
        anomalies = []
        for item in data:
            text = self._extract_text(item)
            keywords = re.findall(r'\w+', text.lower())
            
            # Check for unusual keyword density
            keyword_density = len(keywords) / max(len(text.split()), 1)
            if keyword_density > 0.3:  # Unusually high keyword density
                anomalies.append({
                    "type": "keyword_density_anomaly",
                    "item": item.get('title', 'Unknown'),
                    "density": keyword_density,
                    "anomaly_score": min(keyword_density * 3, 1.0)
                })
        
        return anomalies

    def _analyze_trends(self, data: List[Dict]) -> Dict[str, Any]:
        """Analyze trends in OSINT data"""
        
        if len(data) < 3:
            return {"activity_trend": "insufficient_data", "topic_trends": {}, "analysis_period": {}}
        
        # Temporal trends
        daily_counts = defaultdict(int)
        for item in data:
            timestamp = self._extract_timestamp(item)
            if timestamp:
                date_key = timestamp.date()
                daily_counts[date_key] += 1
        
        # Simple trend analysis (increasing/decreasing)
        dates = sorted(daily_counts.keys())
        counts = [daily_counts[date] for date in dates]
        
        if len(counts) >= 3:
            trend = self._calculate_trend(counts)
        else:
            trend = "insufficient_data"
        
        # Topic trends
        topic_trends = self._analyze_topic_trends(data)
        
        return {
            "activity_trend": trend,
            "topic_trends": topic_trends,
            "analysis_period": {
                "start": min(dates).isoformat() if dates else None,
                "end": max(dates).isoformat() if dates else None,
                "total_days": len(dates)
            }
        }

    def _calculate_trend(self, values: List[float]) -> str:
        """Calculate trend direction using simple linear fit"""
        
        if len(values) < 2:
            return "stable"
        
        x = list(range(len(values)))
        y = values
        
        # Simple linear trend calculation
        n = len(x)
        sum_x = sum(x)
        sum_y = sum(y)
        sum_xy = sum(x[i] * y[i] for i in range(n))
        sum_x2 = sum(xi * xi for xi in x)
        
        try:
            slope = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x * sum_x)
        except ZeroDivisionError:
            return "stable"
        
        if slope > 0.1:
            return "increasing"
        elif slope < -0.1:
            return "decreasing"
        else:
            return "stable"

    def _analyze_topic_trends(self, data: List[Dict]) -> Dict[str, Any]:
        """Analyze topic trends over time"""
        # Simplified topic trend analysis
        topic_counts = Counter()
        for item in data:
            text = self._extract_text(item).lower()
            for topic in ['development', 'infrastructure', 'education', 'health', 'agriculture']:
                if topic in text:
                    topic_counts[topic] += 1
        
        return dict(topic_counts)

    def _build_entity_networks(self, data: List[Dict]) -> Dict[str, Any]:
        """Build networks of related entities"""
        
        entity_cooccurrence = defaultdict(lambda: defaultdict(int))
        
        for item in data:
            entities = self._extract_kenyan_entities(item)
            for i, entity1 in enumerate(entities):
                for entity2 in entities[i+1:]:
                    entity_cooccurrence[entity1][entity2] += 1
                    entity_cooccurrence[entity2][entity1] += 1
        
        # Find strong relationships
        strong_relationships = []
        for entity1, relationships in entity_cooccurrence.items():
            for entity2, count in relationships.items():
                if count >= 2:  # Minimum co-occurrence threshold
                    strong_relationships.append({
                        "entity1": entity1,
                        "entity2": entity2,
                        "strength": count,
                        "normalized_strength": count / len(data)
                    })
        
        return {
            "relationships": strong_relationships,
            "central_entities": self._find_central_entities(entity_cooccurrence),
            "network_density": len(strong_relationships) / max(len(data), 1)
        }

    def _find_central_entities(self, cooccurrence: Dict) -> List[Dict]:
        """Find the most central entities in the network"""
        
        centrality_scores = []
        for entity, relationships in cooccurrence.items():
            degree_centrality = len(relationships)
            weighted_centrality = sum(relationships.values())
            
            centrality_scores.append({
                "entity": entity,
                "degree_centrality": degree_centrality,
                "weighted_centrality": weighted_centrality,
                "combined_score": degree_centrality * math.log(weighted_centrality + 1)
            })
        
        return sorted(centrality_scores, key=lambda x: x["combined_score"], reverse=True)[:10]

    # Helper methods
    def _extract_text(self, item: Dict) -> str:
        """Extract text content from OSINT item"""
        text_parts = []
        for field in ['title', 'content', 'text', 'description']:
            if field in item and item[field]:
                text_parts.append(str(item[field]))
        return ' '.join(text_parts)

    def _extract_timestamp(self, item: Dict) -> Optional[datetime]:
        """Extract and parse timestamp from OSINT item"""
        timestamp = item.get('timestamp') or item.get('created_at') or item.get('date')
        if not timestamp:
            return None
        
        try:
            if isinstance(timestamp, datetime):
                return timestamp
            elif isinstance(timestamp, str):
                # Simple ISO format parsing
                return datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
        except:
            return None
        
        return None

    def _calculate_cluster_score(self, cluster: List[Dict]) -> float:
        """Calculate quality score for a cluster"""
        if len(cluster) < 2:
            return 0.0
        
        # Score based on cluster size and cohesion
        size_score = min(len(cluster) / 10.0, 1.0)  # Normalize cluster size
        
        # Calculate average similarity within cluster
        similarity_sum = 0
        pair_count = 0
        for i in range(len(cluster)):
            for j in range(i+1, len(cluster)):
                similarity_sum += self._calculate_similarity(cluster[i], cluster[j])
                pair_count += 1
        
        cohesion_score = similarity_sum / pair_count if pair_count > 0 else 0
        
        return (size_score * 0.3) + (cohesion_score * 0.7)

    def _extract_common_themes(self, cluster: List[Dict]) -> List[str]:
        """Extract common themes from a cluster of events"""
        all_text = ' '.join([self._extract_text(item) for item in cluster])
        words = re.findall(r'\w+', all_text.lower())
        
        # Filter common words and get most frequent
        common_words = [word for word in words if len(word) > 3 and word not in ['this', 'that', 'with', 'from']]
        word_freq = Counter(common_words)
        
        return [word for word, count in word_freq.most_common(5)]

    def _calculate_cluster_kenyan_relevance(self, cluster: List[Dict]) -> float:
        """Calculate Kenyan relevance score for a cluster"""
        total_relevance = 0.0
        for item in cluster:
            text = self._extract_text(item).lower()
            kenyan_indicators = sum(1 for entity_list in self.kenyan_entities.values() 
                                  for entity in entity_list if entity in text)
            total_relevance += min(kenyan_indicators / 5.0, 1.0)
        
        return total_relevance / len(cluster)

    def _analyze_temporal_patterns(self, data: List[Dict]) -> Dict[str, Any]:
        """Analyze temporal patterns in the data"""
        if len(data) < 3:
            return {"patterns": [], "confidence": 0.0}
        
        timestamps = [self._extract_timestamp(item) for item in data]
        timestamps = [ts for ts in timestamps if ts is not None]
        
        if not timestamps:
            return {"patterns": [], "confidence": 0.0}
        
        timestamps.sort()
        
        # Calculate time intervals between events
        intervals = []
        for i in range(1, len(timestamps)):
            interval = (timestamps[i] - timestamps[i-1]).total_seconds() / 3600  # hours
            intervals.append(interval)
        
        return {
            "average_interval_hours": statistics.mean(intervals) if intervals else 0,
            "interval_std_dev": statistics.stdev(intervals) if len(intervals) > 1 else 0,
            "total_timespan_hours": (max(timestamps) - min(timestamps)).total_seconds() / 3600,
            "events_per_day": len(timestamps) / max((max(timestamps) - min(timestamps)).days, 1)
        }

    def _calculate_pattern_significance(self, patterns: Dict) -> float:
        """Calculate overall significance of detected patterns"""
        significance_scores = []
        
        # Cluster significance
        if patterns["clusters"]:
            avg_cluster_score = sum(cluster["cluster_score"] for cluster in patterns["clusters"]) / len(patterns["clusters"])
            significance_scores.append(avg_cluster_score * 0.4)
        
        # Anomaly significance
        if patterns["anomalies"]:
            anomaly_score = min(len(patterns["anomalies"]) / 10.0, 1.0)  # Normalize anomaly count
            significance_scores.append(anomaly_score * 0.3)
        
        # Trend significance - FIXED: Check if trend exists and is not insufficient_data
        trends = patterns.get("trends", {})
        activity_trend = trends.get("activity_trend", "insufficient_data")
        if activity_trend != "insufficient_data":
            significance_scores.append(0.2)
        
        # Network significance
        networks = patterns.get("entity_networks", {})
        if networks.get("relationships"):
            network_density = networks.get("network_density", 0)
            significance_scores.append(network_density * 0.1)
        
        return sum(significance_scores) if significance_scores else 0.0


# Integration with existing correlator
class EnhancedSovereignCorrelator:
    """Enhanced correlator with ML pattern detection integration"""
    
    def __init__(self, ml_detector: SovereignMLDetector):
        self.ml_detector = ml_detector
    
    def correlate_with_patterns(self, data: List[Dict]) -> Dict[str, Any]:
        """Enhanced correlation with pattern detection"""
        
        # Basic correlation (existing functionality)
        basic_correlation = self._basic_correlation(data)
        
        # ML pattern detection
        patterns = self.ml_detector.detect_patterns(data)
        
        return {
            "basic_correlation": basic_correlation,
            "ml_patterns": patterns,
            "integrated_insights": self._integrate_insights(basic_correlation, patterns)
        }
    
    def _basic_correlation(self, data: List[Dict]) -> Dict[str, Any]:
        """Basic correlation logic (simulating existing functionality)"""
        return {
            "correlated_events": len(data),
            "confidence_score": 0.8,
            "correlation_type": "temporal_and_entity"
        }
    
    def _integrate_insights(self, basic_corr: Dict, patterns: Dict) -> Dict[str, Any]:
        """Integrate basic correlation with ML patterns"""
        
        # FIXED: Safe access to trend data
        activity_trend = patterns.get("trends", {}).get("activity_trend", "unknown")
        
        return {
            "overall_confidence": (basic_corr["confidence_score"] + patterns["pattern_significance"]) / 2,
            "key_insights": [
                f"Detected {len(patterns.get('clusters', []))} event clusters",
                f"Found {len(patterns.get('anomalies', []))} anomalies",
                f"Activity trend: {activity_trend}"
            ],
            "recommended_actions": self._generate_recommendations(patterns)
        }
    
    def _generate_recommendations(self, patterns: Dict) -> List[str]:
        """Generate actionable recommendations based on patterns"""
        recommendations = []
        
        if patterns.get("clusters"):
            recommendations.append("Investigate event clusters for coordinated activities")
        
        if patterns.get("anomalies"):
            recommendations.append("Review anomalies for potential significant events")
        
        trends = patterns.get("trends", {})
        if trends.get("activity_trend") == "increasing":
            recommendations.append("Monitor increasing activity levels closely")
        
        return recommendations


# Example usage
if __name__ == "__main__":
    # Test the ML detector
    ml_detector = SovereignMLDetector()
    
    sample_data = [
        {
            "title": "Nairobi infrastructure project announced",
            "content": "New highway construction in Nairobi County starting next month",
            "timestamp": "2024-01-15T10:00:00Z",
            "source": "government"
        },
        {
            "title": "Mombasa port expansion delays",
            "content": "Port of Mombasa expansion facing construction delays",
            "timestamp": "2024-01-16T14:30:00Z", 
            "source": "news"
        },
        {
            "title": "Kisumu agricultural development", 
            "content": "New farming initiatives in Kisumu County to boost agriculture",
            "timestamp": "2024-01-17T09:15:00Z",
            "source": "ngo"
        }
    ]
    
    patterns = ml_detector.detect_patterns(sample_data)
    print("Pattern Detection Results:")
    print(f"Clusters found: {len(patterns['clusters'])}")
    print(f"Anomalies detected: {len(patterns['anomalies'])}")
    print(f"Trend: {patterns['trends']['activity_trend']}")
    print(f"Overall significance: {patterns['pattern_significance']:.2f}")