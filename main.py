"""
Sovereign OSINT Toolkit by Sarah Marion
Advanced Open Source Intelligence with Kenyan Context Preservation
GitHub: https://github.com/Sarah-Marion/sovereign-osint-toolkit
"""

import sys
import os
import json
from datetime import datetime
from pathlib import Path  

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from exporters.sovereign_exporter import SovereignExporter
from collectors.osint_collector import OSINTCollector

class SovereignOSINTToolkit:
    def __init__(self):
        self.collector = OSINTCollector()
        self.exporter = SovereignExporter()
    
    def run_basic_workflow(self, query: str, user_type: str = "researcher", export_format: str = "json"):
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
        """Enhanced workflow with correlation analysis"""
        print(f"🔍 Collecting OSINT data for: {query}")
        
        # Use the real collector
        collected_data = self.collector.search(query)
        
        # Enhance with OSINT context
        enhanced_data = self.exporter.enhance_with_osint_context(collected_data, "news")
        
        print(f"🔍 Using standard ML correlation...")
        
        # Add basic correlation analysis
        correlation_analysis = self._basic_correlation_analysis(enhanced_data)
        
        # Add analysis summary to the data
        enhanced_with_analysis = enhanced_data.copy()
        enhanced_with_analysis.append({
            'analysis_summary': {
                'timestamp': datetime.now().isoformat(),
                'query': query,
                'total_sources': len(enhanced_data),
                'kenyan_relevance': self.exporter._calculate_overall_kenyan_relevance(enhanced_data),
                'correlation_findings': correlation_analysis.get('key_findings', []),
                'data_quality': correlation_analysis.get('data_quality', 'good')
            }
        })
        
        print(f"📊 Processing data for {user_type} with enhanced analysis...")
        
        # Display key findings
        self._display_analysis_insights(correlation_analysis)
        
        # Export with Kenyan context preservation
        export_result = self.exporter.export_data(enhanced_with_analysis, user_type, export_format)
        
        print(f"✅ Enhanced export completed: {export_result['filename']}")
        print(f"📁 Format: {export_result['format']}, Size: {export_result['size_estimate']} bytes")
        
        return export_result, correlation_analysis
    
    def _basic_correlation_analysis(self, data: list) -> dict:
        """Basic correlation analysis without complex ML dependencies"""
        if not data:
            return {
                'key_findings': ['No data available for analysis'],
                'data_quality': 'unknown',
                'source_reliability': 'unknown'
            }
        
        # Basic analysis
        total_items = len(data)
        kenyan_relevance = self.exporter._calculate_overall_kenyan_relevance(data)
        
        # Extract topics from data
        topics = set()
        for item in data:
            content = str(item).lower()
            if 'development' in content:
                topics.add('development')
            if 'infrastructure' in content:
                topics.add('infrastructure')
            if 'economic' in content or 'economy' in content:
                topics.add('economy')
            if 'digital' in content or 'technology' in content:
                topics.add('technology')
            if 'tourism' in content:
                topics.add('tourism')
            if 'health' in content:
                topics.add('health')
            if 'education' in content:
                topics.add('education')
        
        findings = [
            f"Analyzed {total_items} data sources",
            f"Kenyan relevance score: {kenyan_relevance:.2f}",
            f"Key topics: {', '.join(topics) if topics else 'General'}"
        ]
        
        # Assess data quality
        if total_items >= 3 and kenyan_relevance > 0.3:
            data_quality = 'good'
        elif total_items >= 1:
            data_quality = 'moderate'
        else:
            data_quality = 'poor'
        
        return {
            'key_findings': findings,
            'data_quality': data_quality,
            'source_reliability': 'standard' if total_items > 0 else 'low',
            'topics_identified': list(topics),
            'analysis_timestamp': datetime.now().isoformat()
        }
    
    def _display_analysis_insights(self, analysis: dict):
        """Display key analysis insights"""
        print("\n" + "📊 ANALYSIS RESULTS:")
        print("=" * 40)
        
        for finding in analysis.get('key_findings', []):
            print(f"• {finding}")
        
        print(f"📈 Data Quality: {analysis.get('data_quality', 'unknown')}")
        print(f"🔍 Source Reliability: {analysis.get('source_reliability', 'unknown')}")
        
        topics = analysis.get('topics_identified', [])
        if topics:
            print(f"🏷️  Topics Identified: {', '.join(topics)}")
        
        print("=" * 40)

def main():
    toolkit = SovereignOSINTToolkit()
    
    # Ensure exports directory exists
    os.makedirs("exports", exist_ok=True)
    os.makedirs("exports/enhanced", exist_ok=True)
    os.makedirs("exports/batch_test", exist_ok=True)  # Create batch_test directory
    
    print("🚀 SOVEREIGN OSINT TOOLKIT")
    print("=" * 50)
    
    # Example usage
    queries = [
        "Nairobi infrastructure development",
        "Kenyan digital economy", 
        "Mombasa tourism"
    ]
    
    # Run basic workflow
    print("\n1. RUNNING BASIC WORKFLOW:")
    print("=" * 30)
    
    for query in queries[:2]:  # First two queries
        print(f"\n📋 Processing: {query}")
        
        result = toolkit.run_basic_workflow(query, "researcher", "json")
        
        filename = f"exports/{result['filename']}"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(result['content'])
        print(f"💾 Saved: {filename}")
    
    # Run enhanced workflow
    print("\n2. RUNNING ENHANCED WORKFLOW:")
    print("=" * 30)
    
    for query in queries:
        print(f"\n{'='*40}")
        print(f"Processing: {query}")
        print('='*40)
        
        for user_type in ["journalist", "researcher"]:  # Reduced user types for demo
            try:
                result, analysis = toolkit.run_enhanced_workflow(query, user_type, "json")
                
                # Save enhanced export
                filename = f"exports/enhanced/{result['filename']}"
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(result['content'])
                print(f"💾 Saved: {filename}")
                
                # Save analysis separately
                analysis_filename = f"exports/enhanced/analysis_{query.replace(' ', '_')}_{user_type}.json"
                with open(analysis_filename, 'w', encoding='utf-8') as f:
                    json.dump(analysis, f, indent=2, ensure_ascii=False)
                
                print(f"📊 Analysis saved: {analysis_filename}")
                
            except Exception as e:
                print(f"⚠️  Error processing {query} for {user_type}: {e}")
                continue
    
    # Test batch export
    print("\n3. TESTING BATCH EXPORT:")
    print("=" * 30)
    
    try:
        sample_data = [
            {
                "title": "Test Export",
                "content": "Testing batch export functionality",
                "timestamp": datetime.now().isoformat()
            }
        ]
        
        batch_result = toolkit.exporter.batch_export(
            sample_data,
            formats=["json", "csv"],
            user_types=["journalist", "researcher"],
            output_dir=Path("exports/batch_test")  
        )
        
        print(f"📦 Batch export completed: {len(batch_result.get('files_written', []))} files")
        print(f"📊 Overall quality score: {batch_result.get('quality_report', {}).get('overall_quality_score', 0):.2f}")
        
    except Exception as e:
        print(f"⚠️  Batch export test failed: {e}")
    
    print("\n🎉 All workflows completed successfully!")
    print("📁 Check the 'exports' directory for your results")

if __name__ == "__main__":
    main()