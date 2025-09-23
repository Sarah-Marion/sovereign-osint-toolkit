"""
Sovereign OSINT Toolkit - Main Application
Integrated export system with Kenyan context preservation and ML analysis
"""

import sys
import os
from datetime import datetime

# Add the src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from exporters.sovereign_exporter import SovereignExporter
from collectors.osint_collector import OSINTCollector
from analyzers.sovereign_correlator import SovereignCorrelator

class SovereignOSINTToolkit:
    def __init__(self):
        self.collector = OSINTCollector()
        self.exporter = SovereignExporter()
        self.correlator = SovereignCorrelator()
    
    def run_workflow(self, query: str, user_type: str = "researcher", export_format: str = "json"):
        """Complete OSINT workflow: collection → processing → export"""
        print(f"🔍 Collecting OSINT data for: {query}")
        
        # Use the real collector
        collected_data = self.collector.search(query)
        
        # Enhance with OSINT context
        enhanced_data = self.exporter.enhance_with_osint_context(collected_data, "news")
        
        print(f"📊 Processing data for {user_type}...")
        
        # Export with Kenyan context preservation
        export_result = self.exporter.export_data(enhanced_data, user_type, export_format)
        
        print(f"✅ Export completed: {export_result['filename']}")
        print(f"📁 Format: {export_result['format']}, Size: {export_result['size_estimate']} bytes")
        
        return export_result
    
    def run_enhanced_workflow(self, query: str, user_type: str = "researcher", export_format: str = "json"):
        """Enhanced workflow with ML pattern detection and analysis"""
        print(f"🔍 Collecting OSINT data for: {query}")
        
        # Use the real collector
        collected_data = self.collector.search(query)
        
        # Enhance with OSINT context
        enhanced_data = self.exporter.enhance_with_osint_context(collected_data, "news")
        
        print(f"🧠 Running ML pattern detection...")
        
        # Perform ML correlation analysis
        ml_analysis = self.correlator.correlate_data(enhanced_data)
        
        # Add ML insights to the data
        ml_enhanced_data = enhanced_data.copy()
        ml_enhanced_data.append({
            'ml_analysis_summary': {
                'timestamp': datetime.now().isoformat(),
                'top_insights': ml_analysis['ml_patterns']['predictive_insights'],
                'anomalies_detected': len(ml_analysis['ml_patterns']['detected_anomalies']),
                'sentiment_trend': ml_analysis['ml_patterns']['sentiment_analysis']['sentiment_trend'],
                'confidence_score': ml_analysis['ml_patterns']['ml_confidence_score']
            }
        })
        
        print(f"📊 Processing data for {user_type} with ML insights...")
        
        # Display key ML findings
        self._display_ml_insights(ml_analysis)
        
        # Export with Kenyan context preservation and ML insights
        export_result = self.exporter.export_data(ml_enhanced_data, user_type, export_format)
        
        print(f"✅ Enhanced export completed: {export_result['filename']}")
        print(f"📁 Format: {export_result['format']}, Size: {export_result['size_estimate']} bytes")
        
        return export_result, ml_analysis
    
    def _display_ml_insights(self, ml_analysis: dict):
        """Display key machine learning insights"""
        patterns = ml_analysis['ml_patterns']
        
        print("\n" + "🧠 ML PATTERN DETECTION RESULTS:")
        print("=" * 50)
        
        # Topic clusters
        dominant_topic = list(patterns['topic_clusters']['topic_distribution'].keys())[0]
        dominant_region = list(patterns['topic_clusters']['regional_focus'].keys())[0]
        print(f"📈 Dominant Topic: {dominant_topic}")
        print(f"📍 Primary Region: {dominant_region}")
        
        # Sentiment analysis
        sentiment = patterns['sentiment_analysis']
        print(f"😊 Sentiment Trend: {sentiment['sentiment_trend']} (score: {sentiment['average_sentiment']})")
        
        # Anomalies
        anomalies = patterns['detected_anomalies']
        if anomalies:
            print(f"⚠️  Anomalies Detected: {len(anomalies)}")
            for anomaly in anomalies[:2]:  # Show top 2 anomalies
                print(f"   - {anomaly['description']}")
        else:
            print("✅ No significant anomalies detected")
        
        # Predictions
        predictions = patterns['predictive_insights']['predictions']
        if predictions:
            print(f"🔮 Predictive Insights:")
            for prediction in predictions:
                print(f"   - {prediction['prediction']} (confidence: {prediction['confidence']:.2f})")
        
        print("=" * 50)

def main():
    toolkit = SovereignOSINTToolkit()
    
    # Ensure exports directory exists
    os.makedirs("exports", exist_ok=True)
    os.makedirs("exports/ml_enhanced", exist_ok=True)
    
    print("🚀 SOVEREIGN OSINT TOOLKIT - ENHANCED WITH ML")
    print("=" * 60)
    
    # Example usage
    queries = [
        "Nairobi infrastructure development",
        "Kenyan digital economy", 
        "Mombasa tourism 2024"
    ]
    
    # Run basic workflow (original functionality)
    print("\n1. RUNNING BASIC WORKFLOW:")
    print("=" * 40)
    
    for query in queries[:1]:  # Just first query for basic demo
        print(f"\n📋 Processing: {query}")
        
        for user_type in ["researcher"]:  # Just researcher for basic demo
            result = toolkit.run_workflow(query, user_type, "json")
            
            filename = f"exports/{result['filename']}"
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(result['content'])
            print(f"💾 Saved: {filename}")
    
    # Run enhanced workflow with ML
    print("\n2. RUNNING ENHANCED ML WORKFLOW:")
    print("=" * 40)
    
    for query in queries:
        print(f"\n{'='*50}")
        print(f"Processing: {query}")
        print('='*50)
        
        for user_type in ["journalist", "researcher", "ngo", "developer"]:
            result, ml_analysis = toolkit.run_enhanced_workflow(query, user_type, "json")
            
            # Save enhanced export
            filename = f"exports/ml_enhanced/{result['filename']}"
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(result['content'])
            print(f"💾 Saved: {filename}")
            
            # Save ML analysis separately
            ml_filename = f"exports/ml_enhanced/ml_analysis_{query.replace(' ', '_')}_{user_type}.json"
            with open(ml_filename, 'w', encoding='utf-8') as f:
                # Convert numpy values to Python native for JSON serialization
                import json
                from decimal import Decimal
                
                def convert_numpy_types(obj):
                    if isinstance(obj, (np.integer, np.floating)):
                        return float(obj)
                    elif isinstance(obj, np.ndarray):
                        return obj.tolist()
                    elif isinstance(obj, dict):
                        return {k: convert_numpy_types(v) for k, v in obj.items()}
                    elif isinstance(obj, list):
                        return [convert_numpy_types(item) for item in obj]
                    return obj
                
                serializable_analysis = convert_numpy_types(ml_analysis)
                json.dump(serializable_analysis, f, indent=2, ensure_ascii=False)
            
            print(f"🧠 ML Analysis saved: {ml_filename}")
            
            # Test batch export for comprehensive coverage
            if user_type == "researcher":
                batch_result = toolkit.exporter.batch_export(
                    [{'title': query, 'content': f'Batch export test for {query}'}],
                    ["json", "csv", "html"]
                )
                print(f"📦 Batch export: {len(batch_result['exports'])} user types")

if __name__ == "__main__":
    main()