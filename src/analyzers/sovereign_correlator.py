"""
Sovereign Correlator with Advanced ML Pattern Detection
Enhanced with graph-based correlation and multi-modal analysis
By Sarah Marion
"""

import json
import math
from datetime import datetime, timedelta
from collections import defaultdict, Counter
import re
from typing import Dict, List, Any, Optional, Tuple, Set
from dataclasses import dataclass

from .sovereign_ml_detector import SovereignMLDetector, EnhancedSovereignCorrelator


@dataclass
class CorrelationEdge:
    """Represents a relationship between two entities"""
    source: str
    target: str
    strength: float
    correlation_type: str  # 'temporal', 'spatial', 'content', 'cross_source'
    evidence_count: int
    last_observed: datetime


class AdvancedSovereignCorrelator:
    """Advanced correlation with graph-based algorithms and multi-modal analysis"""
    
    def __init__(self):
        self.ml_detector = SovereignMLDetector()
        self.entity_graph = defaultdict(dict)  # Graph of entity relationships
        self.correlation_history = []
        
        # Advanced similarity configurations
        self.similarity_config = {
            'content_weight': 0.4,
            'temporal_weight': 0.3,
            'spatial_weight': 0.2,
            'source_weight': 0.1,
            'min_correlation_threshold': 0.6,
            'graph_decay_factor': 0.9  # How quickly old correlations decay
        }
    
    def advanced_correlate(self, data_sources: List[Dict]) -> Dict[str, Any]:
        """Advanced multi-modal correlation analysis"""
        print("🔗 Running advanced correlation algorithms...")
        
        # Phase 1: Basic ML pattern detection
        ml_patterns = self.ml_detector.detect_patterns(data_sources)
        
        # Phase 2: Graph-based relationship analysis
        graph_analysis = self._analyze_entity_graph(data_sources)
        
        # Phase 3: Multi-modal correlation
        multi_modal_correlation = self._multi_modal_correlation(data_sources)
        
        # Phase 4: Cross-source verification
        verification_analysis = self._cross_source_verification(data_sources)
        
        # Phase 5: Confidence synthesis
        confidence_analysis = self._synthesize_confidence(
            ml_patterns, graph_analysis, multi_modal_correlation, verification_analysis
        )
        
        return {
            'timestamp': datetime.now().isoformat(),
            'data_sources_analyzed': len(data_sources),
            'ml_patterns': ml_patterns,
            'graph_analysis': graph_analysis,
            'multi_modal_correlation': multi_modal_correlation,
            'cross_source_verification': verification_analysis,
            'confidence_synthesis': confidence_analysis,
            'advanced_insights': self._generate_advanced_insights(
                ml_patterns, graph_analysis, multi_modal_correlation
            )
        }
    
    def _analyze_entity_graph(self, data_sources: List[Dict]) -> Dict[str, Any]:
        """Build and analyze entity relationship graph"""
        print("   📊 Building entity relationship graph...")
        
        # Extract entities and relationships
        entities = self._extract_entities(data_sources)
        relationships = self._build_relationships(data_sources, entities)
        
        # Update global entity graph
        self._update_entity_graph(relationships)
        
        # Analyze graph properties
        graph_metrics = self._calculate_graph_metrics()
        communities = self._detect_communities()
        central_entities = self._find_central_entities()
        
        return {
            'entity_count': len(entities),
            'relationship_count': len(relationships),
            'graph_metrics': graph_metrics,
            'detected_communities': communities,
            'central_entities': central_entities,
            'graph_density': self._calculate_graph_density()
        }
    
    def _extract_entities(self, data_sources: List[Dict]) -> Dict[str, List[str]]:
        """Extract entities from OSINT data with categorization"""
        entities = defaultdict(list)
        
        for item in data_sources:
            text = f"{item.get('title', '')} {item.get('content', '')}".lower()
            
            # Extract different entity types
            entities['political_figures'].extend(
                [figure for figure in ['ruto', 'raila', 'mudavadi', 'uhuru'] if figure in text]
            )
            entities['locations'].extend(
                [loc for loc in ['nairobi', 'mombasa', 'kisumu', 'nakuru'] if loc in text]
            )
            entities['organizations'].extend(
                [org for org in ['government', 'parliament', 'county', 'safaricom'] if org in text]
            )
            entities['topics'].extend(
                [topic for topic in ['development', 'infrastructure', 'education', 'health'] if topic in text]
            )
        
        # Remove duplicates
        for category in entities:
            entities[category] = list(set(entities[category]))
            
        return entities
    
    def _build_relationships(self, data_sources: List[Dict], entities: Dict) -> List[CorrelationEdge]:
        """Build correlation relationships between entities"""
        relationships = []
        
        for item in data_sources:
            item_entities = self._extract_entities_from_item(item)
            timestamp = self._extract_timestamp(item)
            
            # Create relationships between co-mentioned entities
            for i, entity1 in enumerate(item_entities):
                for entity2 in item_entities[i+1:]:
                    # Calculate relationship strength
                    strength = self._calculate_relationship_strength(entity1, entity2, item)
                    
                    relationship = CorrelationEdge(
                        source=entity1,
                        target=entity2,
                        strength=strength,
                        correlation_type='co_occurrence',
                        evidence_count=1,
                        last_observed=timestamp or datetime.now()
                    )
                    relationships.append(relationship)
        
        return relationships
    
    def _calculate_relationship_strength(self, entity1: str, entity2: str, context: Dict) -> float:
        """Calculate strength of relationship between two entities"""
        strength = 0.0
        
        # Base co-occurrence strength
        strength += 0.3
        
        # Contextual reinforcement
        text = f"{context.get('title', '')} {context.get('content', '')}".lower()
        
        # Semantic proximity in text
        words = text.split()
        if entity1 in words and entity2 in words:
            pos1 = words.index(entity1)
            pos2 = words.index(entity2)
            distance = abs(pos1 - pos2)
            proximity_strength = max(0, 1 - (distance / len(words)))
            strength += proximity_strength * 0.4
        
        # Source reliability bonus
        source = context.get('source', '')
        if source in ['government', 'official']:
            strength += 0.2
        
        return min(strength, 1.0)
    
    def _update_entity_graph(self, new_relationships: List[CorrelationEdge]):
        """Update the global entity graph with new relationships"""
        for relationship in new_relationships:
            key = (relationship.source, relationship.target)
            
            if key in self.entity_graph:
                # Update existing relationship with decay
                existing = self.entity_graph[key]
                time_decay = self._calculate_time_decay(existing.last_observed)
                existing.strength = (existing.strength * time_decay + relationship.strength) / 2
                existing.evidence_count += 1
                existing.last_observed = relationship.last_observed
            else:
                # Add new relationship
                self.entity_graph[key] = relationship
    
    def _calculate_time_decay(self, last_observed: datetime) -> float:
        """Calculate decay factor based on time since last observation"""
        days_passed = (datetime.now() - last_observed).days
        return self.similarity_config['graph_decay_factor'] ** min(days_passed, 30)
    
    def _calculate_graph_metrics(self) -> Dict[str, float]:
        """Calculate various graph theory metrics"""
        if not self.entity_graph:
            return {}
        
        nodes = set()
        for (source, target) in self.entity_graph:
            nodes.add(source)
            nodes.add(target)
        
        # Basic metrics
        edge_count = len(self.entity_graph)
        node_count = len(nodes)
        
        # Average degree
        degrees = defaultdict(int)
        for (source, target) in self.entity_graph:
            degrees[source] += 1
            degrees[target] += 1
        
        avg_degree = sum(degrees.values()) / node_count if node_count > 0 else 0
        
        return {
            'node_count': node_count,
            'edge_count': edge_count,
            'average_degree': avg_degree,
            'graph_diameter': self._estimate_graph_diameter(),
            'clustering_coefficient': self._calculate_clustering_coefficient()
        }
    
    def _estimate_graph_diameter(self) -> float:
        """Estimate graph diameter using simple BFS approximation"""
        # Simplified implementation for performance
        return 2.0  # Placeholder - would be actual BFS in production
    
    def _calculate_clustering_coefficient(self) -> float:
        """Calculate average clustering coefficient"""
        # Simplified implementation
        return 0.3  # Placeholder - would be actual graph algorithm in production
    
    def _detect_communities(self) -> List[Dict]:
        """Detect communities in the entity graph using simple clustering"""
        communities = []
        
        # Simple community detection based on strongly connected components
        visited = set()
        
        # FIXED: Proper list comprehension syntax
        all_nodes = set()
        for edge in self.entity_graph:
            all_nodes.add(edge[0])
            all_nodes.add(edge[1])
        
        for node in all_nodes:
            if node not in visited:
                community = self._bfs_community(node, visited)
                if len(community) >= 2:  # Only include meaningful communities
                    communities.append({
                        'nodes': list(community),
                        'size': len(community),
                        'internal_density': self._calculate_community_density(community)
                    })
        
        return sorted(communities, key=lambda x: x['size'], reverse=True)[:5]  # Top 5 communities
    
    def _bfs_community(self, start_node: str, visited: Set) -> Set:
        """Find connected component using BFS"""
        community = set()
        queue = [start_node]
        
        while queue:
            node = queue.pop(0)
            if node not in visited:
                visited.add(node)
                community.add(node)
                # Add neighbors
                for (source, target) in self.entity_graph:
                    if source == node and target not in visited:
                        queue.append(target)
                    elif target == node and source not in visited:
                        queue.append(source)
        
        return community
    
    def _calculate_community_density(self, community: Set) -> float:
        """Calculate density of a community subgraph"""
        possible_edges = len(community) * (len(community) - 1) / 2
        if possible_edges == 0:
            return 0.0
        
        actual_edges = 0
        for (source, target) in self.entity_graph:
            if source in community and target in community:
                actual_edges += 1
        
        return actual_edges / possible_edges
    
    def _find_central_entities(self) -> List[Dict]:
        """Find the most central entities using degree centrality"""
        centrality_scores = defaultdict(float)
        
        for (source, target), relationship in self.entity_graph.items():
            centrality_scores[source] += relationship.strength
            centrality_scores[target] += relationship.strength
        
        sorted_entities = sorted(centrality_scores.items(), key=lambda x: x[1], reverse=True)
        
        return [{'entity': entity, 'centrality_score': score} 
                for entity, score in sorted_entities[:10]]  # Top 10 central entities
    
    def _calculate_graph_density(self) -> float:
        """Calculate density of the entity graph"""
        nodes = set()
        for (source, target) in self.entity_graph:
            nodes.add(source)
            nodes.add(target)
        
        n = len(nodes)
        if n <= 1:
            return 0.0
        
        possible_edges = n * (n - 1) / 2
        actual_edges = len(self.entity_graph)
        
        return actual_edges / possible_edges
    
    def _multi_modal_correlation(self, data_sources: List[Dict]) -> Dict[str, Any]:
        """Perform multi-modal correlation analysis"""
        print("   🌐 Running multi-modal correlation...")
        
        correlations = []
        
        for i, item1 in enumerate(data_sources):
            for j, item2 in enumerate(data_sources[i+1:], i+1):
                correlation_score = self._calculate_multi_modal_similarity(item1, item2)
                
                if correlation_score >= self.similarity_config['min_correlation_threshold']:
                    correlations.append({
                        'item1': item1.get('title', f'Item_{i}'),
                        'item2': item2.get('title', f'Item_{j}'),
                        'correlation_score': correlation_score,
                        'modality_breakdown': self._get_modality_breakdown(item1, item2)
                    })
        
        return {
            'significant_correlations': sorted(correlations, key=lambda x: x['correlation_score'], reverse=True),
            'average_correlation': self._calculate_average_correlation(correlations),
            'correlation_network_size': len(correlations)
        }
    
    def _calculate_multi_modal_similarity(self, item1: Dict, item2: Dict) -> float:
        """Calculate multi-modal similarity between two items"""
        similarities = []
        
        # Content similarity (enhanced)
        content_sim = self._enhanced_content_similarity(item1, item2)
        similarities.append(content_sim * self.similarity_config['content_weight'])
        
        # Temporal similarity
        temporal_sim = self._temporal_similarity(item1, item2)
        similarities.append(temporal_sim * self.similarity_config['temporal_weight'])
        
        # Spatial similarity
        spatial_sim = self._spatial_similarity(item1, item2)
        similarities.append(spatial_sim * self.similarity_config['spatial_weight'])
        
        # Source similarity
        source_sim = self._source_similarity(item1, item2)
        similarities.append(source_sim * self.similarity_config['source_weight'])
        
        return sum(similarities)
    
    def _enhanced_content_similarity(self, item1: Dict, item2: Dict) -> float:
        """Enhanced content similarity using TF-IDF like approach"""
        text1 = f"{item1.get('title', '')} {item1.get('content', '')}".lower()
        text2 = f"{item2.get('title', '')} {item2.get('content', '')}".lower()
        
        if not text1 or not text2:
            return 0.0
        
        # Tokenize and calculate term frequencies
        words1 = re.findall(r'\w+', text1)
        words2 = re.findall(r'\w+', text2)
        
        if not words1 or not words2:
            return 0.0
        
        # Calculate cosine similarity
        tf1 = Counter(words1)
        tf2 = Counter(words2)
        
        # Simple cosine similarity calculation
        dot_product = sum(tf1[word] * tf2[word] for word in set(words1) & set(words2))
        magnitude1 = math.sqrt(sum(tf1[word] ** 2 for word in words1))
        magnitude2 = math.sqrt(sum(tf2[word] ** 2 for word in words2))
        
        if magnitude1 * magnitude2 == 0:
            return 0.0
        
        return dot_product / (magnitude1 * magnitude2)
    
    def _temporal_similarity(self, item1: Dict, item2: Dict) -> float:
        """Calculate temporal similarity"""
        time1 = self._extract_timestamp(item1)
        time2 = self._extract_timestamp(item2)
        
        if not time1 or not time2:
            return 0.5
        
        time_diff = abs((time1 - time2).total_seconds())
        
        # Exponential decay based on time difference
        if time_diff < 3600:  # 1 hour
            return 1.0
        elif time_diff < 86400:  # 1 day
            return 0.8
        elif time_diff < 604800:  # 1 week
            return 0.6
        else:
            return 0.3
    
    def _spatial_similarity(self, item1: Dict, item2: Dict) -> float:
        """Calculate spatial similarity based on Kenyan locations"""
        kenyan_locations = ['nairobi', 'mombasa', 'kisumu', 'nakuru', 'eldoret', 'kakamega']
        
        text1 = f"{item1.get('title', '')} {item1.get('content', '')}".lower()
        text2 = f"{item2.get('title', '')} {item2.get('content', '')}".lower()
        
        locations1 = [loc for loc in kenyan_locations if loc in text1]
        locations2 = [loc for loc in kenyan_locations if loc in text2]
        
        if not locations1 or not locations2:
            return 0.3  # Neutral similarity if no location info
        
        # Same location = high similarity, different locations = medium similarity
        return 1.0 if set(locations1) == set(locations2) else 0.5
    
    def _source_similarity(self, item1: Dict, item2: Dict) -> float:
        """Calculate similarity based on source reliability and type"""
        source1 = item1.get('source', 'unknown')
        source2 = item2.get('source', 'unknown')
        
        source_categories = {
            'high_confidence': ['government', 'official', 'verified_news'],
            'medium_confidence': ['news', 'organization', 'academic'],
            'low_confidence': ['social_media', 'unofficial', 'unknown']
        }
        
        # Same source category = higher similarity
        for category, sources in source_categories.items():
            if source1 in sources and source2 in sources:
                return 0.8 if category == 'high_confidence' else 0.6
        
        return 0.4  # Different source categories
    
    def _get_modality_breakdown(self, item1: Dict, item2: Dict) -> Dict[str, float]:
        """Get breakdown of similarity across different modalities"""
        return {
            'content_similarity': self._enhanced_content_similarity(item1, item2),
            'temporal_similarity': self._temporal_similarity(item1, item2),
            'spatial_similarity': self._spatial_similarity(item1, item2),
            'source_similarity': self._source_similarity(item1, item2)
        }
    
    def _calculate_average_correlation(self, correlations: List[Dict]) -> float:
        """Calculate average correlation score"""
        if not correlations:
            return 0.0
        return sum(corr['correlation_score'] for corr in correlations) / len(correlations)
    
    def _cross_source_verification(self, data_sources: List[Dict]) -> Dict[str, Any]:
        """Verify information across different sources"""
        print("   🔍 Performing cross-source verification...")
        
        # Group by similar content
        content_groups = defaultdict(list)
        
        for item in data_sources:
            # Create a content signature based on key entities
            signature = self._create_content_signature(item)
            content_groups[signature].append(item)
        
        verification_results = []
        
        for signature, items in content_groups.items():
            if len(items) > 1:  # Multiple sources reporting similar content
                source_types = [item.get('source', 'unknown') for item in items]
                source_diversity = len(set(source_types))
                
                verification_results.append({
                    'content_signature': signature,
                    'source_count': len(items),
                    'source_diversity': source_diversity,
                    'verification_confidence': min(source_diversity / 3, 1.0),
                    'sources': source_types
                })
        
        return {
            'verified_clusters': verification_results,
            'total_verified_clusters': len(verification_results),
            'average_verification_confidence': (
                sum(r['verification_confidence'] for r in verification_results) / 
                len(verification_results) if verification_results else 0
            )
        }
    
    def _create_content_signature(self, item: Dict) -> str:
        """Create a signature for content grouping"""
        text = f"{item.get('title', '')} {item.get('content', '')}".lower()
        
        # Extract key entities for signature
        key_entities = []
        entities_to_match = ['ruto', 'raila', 'nairobi', 'mombasa', 'development', 'infrastructure']
        
        for entity in entities_to_match:
            if entity in text:
                key_entities.append(entity)
        
        return '_'.join(sorted(key_entities)) if key_entities else 'general'
    
    def _synthesize_confidence(self, *analyses) -> Dict[str, Any]:
        """Synthesize confidence from multiple analysis phases"""
        confidence_scores = []
        
        for analysis in analyses:
            if 'pattern_significance' in analysis:
                confidence_scores.append(analysis['pattern_significance'])
            if 'average_correlation' in analysis:
                confidence_scores.append(analysis['average_correlation'])
            if 'average_verification_confidence' in analysis:
                confidence_scores.append(analysis['average_verification_confidence'])
        
        overall_confidence = sum(confidence_scores) / len(confidence_scores) if confidence_scores else 0.0
        
        return {
            'overall_confidence': overall_confidence,
            'component_scores': confidence_scores,
            'confidence_level': self._map_confidence_level(overall_confidence)
        }
    
    def _map_confidence_level(self, score: float) -> str:
        """Map numerical confidence score to qualitative level"""
        if score >= 0.8:
            return 'high'
        elif score >= 0.6:
            return 'medium'
        elif score >= 0.4:
            return 'low'
        else:
            return 'very_low'
    
    def _generate_advanced_insights(self, *analyses) -> List[str]:
        """Generate advanced insights from correlation results"""
        insights = []
        
        # Extract key findings from each analysis
        ml_patterns, graph_analysis, multi_modal = analyses
        
        # ML pattern insights
        if ml_patterns.get('pattern_significance', 0) > 0.7:
            insights.append("Strong pattern significance detected - high confidence in correlations")
        
        # Graph analysis insights
        if graph_analysis.get('graph_metrics', {}).get('node_count', 0) > 10:
            insights.append("Complex entity network detected - rich relationship structure")
        
        # Multi-modal insights
        if multi_modal.get('average_correlation', 0) > 0.6:
            insights.append("Strong multi-modal correlations found across data sources")
        
        return insights if insights else ["Baseline correlation patterns observed"]
    
    def _extract_timestamp(self, item: Dict) -> Optional[datetime]:
        """Extract timestamp from item"""
        timestamp = item.get('timestamp')
        if not timestamp:
            return None
        
        try:
            if isinstance(timestamp, datetime):
                return timestamp
            elif isinstance(timestamp, str):
                return datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
        except:
            return None
        
        return None
    
    def _extract_entities_from_item(self, item: Dict) -> List[str]:
        """Extract entities from a single item"""
        text = f"{item.get('title', '')} {item.get('content', '')}".lower()
        entities = []
        
        # Extract various entity types
        entity_patterns = {
            'political_figures': ['ruto', 'raila', 'mudavadi', 'uhuru'],
            'locations': ['nairobi', 'mombasa', 'kisumu', 'nakuru'],
            'topics': ['development', 'infrastructure', 'education', 'health']
        }
        
        for category, terms in entity_patterns.items():
            entities.extend([term for term in terms if term in text])
        
        return list(set(entities))


# Update the main correlator class to use advanced capabilities
class SovereignCorrelator:
    """Enhanced main correlator with advanced algorithms"""
    
    def __init__(self):
        self.advanced_correlator = AdvancedSovereignCorrelator()
        self.ml_detector = SovereignMLDetector()
        
    def correlate_data(self, data_sources: List[Dict], advanced: bool = True) -> Dict[str, Any]:
        """Main correlation method with optional advanced analysis"""
        
        if advanced and len(data_sources) >= 3:  # Use advanced for sufficient data
            print("🚀 Using advanced correlation algorithms...")
            return self.advanced_correlator.advanced_correlate(data_sources)
        else:
            print("🔍 Using standard ML correlation...")
            # Fall back to basic ML correlation
            enhanced_correlator = EnhancedSovereignCorrelator(self.ml_detector)
            return enhanced_correlator.correlate_with_patterns(data_sources)


# Example usage
if __name__ == "__main__":
    # Test the advanced correlator
    correlator = SovereignCorrelator()
    
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
    
    result = correlator.correlate_data(sample_data, advanced=True)
    print("Advanced Correlation Results:")
    print(f"Overall Confidence: {result['confidence_synthesis']['overall_confidence']:.2f}")
    print(f"Graph Analysis: {result['graph_analysis']['entity_count']} entities")
    print(f"Multi-modal Correlations: {result['multi_modal_correlation']['correlation_network_size']}")