"""
🚀 Sovereign OSINT Toolkit by Sarah Marion
Advanced Open Source Intelligence with Kenyan Context Preservation
📍 Security-Focused Full-Stack Developer | Kenyan OSINT Specialist
🔗 GitHub: https://github.com/Sarah-Marion/sovereign-osint-toolkit  
🔗 Portfolio: https://www.sarahmarion.com/

COMPREHENSIVE ARCHITECTURE:
• Kenyan cultural context validation
• Data Protection Act 2019 compliance  
• Multi-format exports for different user types
• Source reliability scoring
• Batch processing with quality metrics
• Ethical boundaries and cultural frameworks
"""

import sys
import os
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any

def display_banner():
    print("""
    ╔═══════════════════════════════════════════════════════════════════╗
    ║                                                                   ║
    ║   🚀 SOVEREIGN OSINT TOOLKIT by Sarah Marion                      ║
    ║   🔒 Security-Focused Full-Stack Developer                        ║
    ║   📍 Advanced Kenyan-Focused Intelligence Platform                ║
    ║                                                                   ║
    ║   GitHub: https://github.com/Sarah-Marion/sovereign-osint-toolkit ║
    ║   Portfolio: https://www.sarahmarion.com/                         ║
    ║   Blog: https://blog.sarahmarion.com/                             ║
    ║                                                                   ║
    ╚═══════════════════════════════════════════════════════════════════╝
    """)

# Add the src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from exporters.sovereign_exporter import SovereignExporter
from collectors.osint_collector import OSINTCollector

# Import the comprehensive architecture (if available)
try:
    from sovereign_osint import KenyanOSINTCollector, KenyanDataAnalyzer, KenyanGeospatialAnalyzer
    COMPREHENSIVE_ARCHITECTURE = True
except ImportError:
    COMPREHENSIVE_ARCHITECTURE = False
    print("⚠️  Comprehensive architecture not available - using basic workflow")


class SovereignOSINTToolkit:
    def __init__(self, use_comprehensive: bool = False):
        """Initialize toolkit with optional comprehensive architecture"""
        self.use_comprehensive = use_comprehensive and COMPREHENSIVE_ARCHITECTURE
        
        # Core components (always available)
        self.basic_collector = OSINTCollector()
        self.exporter = SovereignExporter()
        
        # Comprehensive architecture components (if available)
        if self.use_comprehensive:
            self.kenyan_collector = KenyanOSINTCollector(ethical_boundaries=True)
            self.data_analyzer = KenyanDataAnalyzer()
            self.geospatial_analyzer = KenyanGeospatialAnalyzer()
            print("✅ Comprehensive Kenyan OSINT architecture loaded")
        else:
            print("✅ Basic OSINT workflow loaded")
    
    def run_basic_workflow(self, query: str, user_type: str = "researcher", export_format: str = "json"):
        """Complete OSINT workflow: collection → processing → export"""
        print(f"🔍 Collecting OSINT data for: {query}")
        
        # Use the basic collector
        collected_data = self.basic_collector.search(query)
        
        # Enhance with OSINT context
        enhanced_data = self.exporter.enhance_with_osint_context(collected_data, "news")
        
        print(f"📊 Processing data for {user_type}...")
        
        # Export with Kenyan context preservation
        export_result = self.exporter.export_data(enhanced_data, user_type, export_format)
        
        print(f"✅ Export completed: {export_result['filename']}")
        print(f"📁 Format: {export_result['format']}, Size: {export_result['size_estimate']} bytes")
        
        return export_result
    
    def run_comprehensive_workflow(self, query: str, region: str = "nairobi", 
                                 user_type: str = "researcher", export_format: str = "json"):
        """Comprehensive workflow using Kenyan-focused architecture"""
        if not self.use_comprehensive:
            print("⚠️  Comprehensive architecture not available - falling back to basic workflow")
            return self.run_basic_workflow(query, user_type, export_format), {}
        
        print(f"🔍 Comprehensive analysis for: {query} in {region}")
        
        try:
            # Collect data with Kenyan cultural context
            social_data = self.kenyan_collector.analyze_kenyan_social_media(
                platform="twitter", region=region, query=query
            )
            
            news_data = self.kenyan_collector.collect_kenyan_news(
                topics=[query], regions=[region]
            )
            
            # Analyze with cultural context
            cultural_insights = self.data_analyzer.generate_cultural_context_insights(
                data_source="combined", data=social_data["data"] + news_data["data"]
            )
            
            # Geospatial analysis
            geospatial_map = self.geospatial_analyzer.create_cultural_geospatial_map(
                region=region, data=news_data["data"]
            )
            
            # Combine all analysis
            comprehensive_results = {
                "query": query,
                "region": region,
                "social_media_analysis": social_data,
                "news_analysis": news_data,
                "cultural_insights": cultural_insights,
                "geospatial_analysis": geospatial_map,
                "analysis_timestamp": datetime.now().isoformat(),
                "kenyan_relevance_score": news_data.get("kenyan_relevance_score", 0.0),
                "architecture": "comprehensive"
            }
            
            # Export results
            export_result = self.exporter.export_data(
                [comprehensive_results], user_type, export_format
            )
            
            # Display comprehensive insights
            self._display_comprehensive_insights(comprehensive_results)
            
            return export_result, comprehensive_results
            
        except Exception as e:
            print(f"❌ Comprehensive workflow error: {e}")
            print("🔄 Falling back to basic workflow...")
            return self.run_basic_workflow(query, user_type, export_format), {}
    
    def run_enhanced_workflow(self, query: str, user_type: str = "researcher", export_format: str = "json"):
        """Enhanced workflow with correlation analysis (basic architecture)"""
        print(f"🔍 Collecting OSINT data for: {query}")
        
        # Use the basic collector
        collected_data = self.basic_collector.search(query)
        
        # Enhance with OSINT context
        enhanced_data = self.exporter.enhance_with_osint_context(collected_data, "news")
        
        print(f"🔍 Running correlation analysis...")
        
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
                'data_quality': correlation_analysis.get('data_quality', 'good'),
                'architecture': 'enhanced_basic'
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
        print("=" * 50)
        
        for finding in analysis.get('key_findings', []):
            print(f"• {finding}")
        
        print(f"📈 Data Quality: {analysis.get('data_quality', 'unknown')}")
        print(f"🔍 Source Reliability: {analysis.get('source_reliability', 'unknown')}")
        
        topics = analysis.get('topics_identified', [])
        if topics:
            print(f"🏷️  Topics Identified: {', '.join(topics)}")
        
        print("=" * 50)
    
    def _display_comprehensive_insights(self, analysis: dict):
        """Display comprehensive architecture insights"""
        print("\n" + "🧠 COMPREHENSIVE ANALYSIS INSIGHTS:")
        print("=" * 60)
        
        print(f"📍 Region: {analysis.get('region', 'Unknown')}")
        print(f"📊 Kenyan Relevance: {analysis.get('kenyan_relevance_score', 0):.2f}")
        
        cultural_insights = analysis.get('cultural_insights', {})
        print(f"🌍 Cultural Insights: {len(cultural_insights.get('insights', []))} found")
        
        geospatial = analysis.get('geospatial_analysis', {})
        print(f"🗺️  Cultural Landmarks: {len(geospatial.get('cultural_landmarks', []))} mapped")
        
        social_data = analysis.get('social_media_analysis', {})
        print(f"📱 Social Media Analysis: {social_data.get('ethical_boundaries_applied', False)}")
        
        print("=" * 60)


def main():
    display_banner()
    
    toolkit = SovereignOSINTToolkit(use_comprehensive=True)
    
    # Ensure exports directory exists
    os.makedirs("exports", exist_ok=True)
    os.makedirs("exports/enhanced", exist_ok=True)
    os.makedirs("exports/comprehensive", exist_ok=True)
    os.makedirs("exports/batch_test", exist_ok=True)
    
    print("🚀 SOVEREIGN OSINT TOOLKIT - UNIFIED ARCHITECTURE")
    print("=" * 60)
    
    # Example usage
    queries = [
        "Nairobi infrastructure development",
        "Kenyan digital economy", 
        "Mombasa tourism"
    ]
    
    # 1. Run basic workflow
    print("\n1. RUNNING BASIC WORKFLOW:")
    print("=" * 40)
    
    for query in queries[:2]:
        print(f"\n📋 Processing: {query}")
        result = toolkit.run_basic_workflow(query, "researcher", "json")
        filename = f"exports/{result['filename']}"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(result['content'])
        print(f"💾 Saved: {filename}")
    
    # 2. Run enhanced workflow
    print("\n2. RUNNING ENHANCED WORKFLOW:")
    print("=" * 40)
    
    for query in queries:
        print(f"\n{'='*50}")
        print(f"Processing: {query}")
        print('='*50)
        
        for user_type in ["journalist", "researcher"]:
            try:
                result, analysis = toolkit.run_enhanced_workflow(query, user_type, "json")
                filename = f"exports/enhanced/{result['filename']}"
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(result['content'])
                print(f"💾 Saved: {filename}")
                
                analysis_filename = f"exports/enhanced/analysis_{query.replace(' ', '_')}_{user_type}.json"
                with open(analysis_filename, 'w', encoding='utf-8') as f:
                    json.dump(analysis, f, indent=2, ensure_ascii=False)
                print(f"📊 Analysis saved: {analysis_filename}")
                
            except Exception as e:
                print(f"⚠️  Error: {e}")
                continue
    
    # 3. Run comprehensive workflow (if available)
    if COMPREHENSIVE_ARCHITECTURE:
        print("\n3. RUNNING COMPREHENSIVE WORKFLOW:")
        print("=" * 40)
        
        regions = ["nairobi", "mombasa", "kisumu"]
        for i, query in enumerate(queries):
            region = regions[i] if i < len(regions) else "nairobi"
            print(f"\n{'='*50}")
            print(f"Comprehensive Analysis: {query} in {region}")
            print('='*50)
            
            try:
                result, analysis = toolkit.run_comprehensive_workflow(query, region, "researcher", "json")
                filename = f"exports/comprehensive/{result['filename']}"
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(result['content'])
                print(f"💾 Comprehensive export saved: {filename}")
                
            except Exception as e:
                print(f"⚠️  Comprehensive workflow error: {e}")
                continue
    
    # 4. Test batch export
    print("\n4. TESTING BATCH EXPORT:")
    print("=" * 40)
    
    try:
        sample_data = [{"title": "Batch Test", "content": "Testing batch export functionality"}]
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