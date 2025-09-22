"""
Demo: Sovereign Export System
Showcasing different export formats for various user types
By Sarah Marion
"""

from src.exporters.sovereign_exporter import SovereignExporter
import json

def demo_export_system():
    """Demonstrate the export system for different user types"""
    
    exporter = SovereignExporter()
    
    # Sample data with Kenyan context
    sample_data = [
        {
            "title": "Nairobi County Budget Analysis 2024",
            "content": "Analysis of budget allocation across Nairobi constituencies",
            "source": "County Government Portal",
            "kenyan_relevance": 0.9,
            "county": "Nairobi",
            "topics": ["budget", "development", "governance"]
        },
        {
            "title": "Mombasa Port Efficiency Report",
            "content": "Study of port operations and economic impact on Coastal region",
            "source": "KPA Annual Report",
            "kenyan_relevance": 0.8,
            "county": "Mombasa", 
            "topics": ["economy", "infrastructure", "trade"]
        }
    ]
    
    user_types = ["journalist", "researcher", "ngo", "developer"]
    formats = ["json", "csv", "html"]
    
    print("🇰🇪 Sovereign OSINT Export System Demo")
    print("=" * 50)
    
    for user_type in user_types:
        print(f"\n📊 Exporting for {user_type.upper()}:")
        print("-" * 30)
        
        for fmt in formats:
            try:
                result = exporter.export_data(sample_data, user_type, fmt)
                print(f"  ✅ {fmt.upper()}: {result['filename']} ({result['size_estimate']} bytes)")
                
                # Show a preview for JSON
                if fmt == "json":
                    data_preview = json.loads(result['content'])
                    print(f"     Metadata: {data_preview['metadata']['kenyan_context_version']}")
                    
            except Exception as e:
                print(f"  ❌ {fmt.upper()}: Error - {e}")
    
    print(f"\n🎯 Demo completed. Export system ready for {len(user_types)} user types.")

if __name__ == "__main__":
    demo_export_system()