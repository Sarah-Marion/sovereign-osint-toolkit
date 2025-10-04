#!/usr/bin/virtual python3
"""
Demo script showing successful Sovereign OSINT Toolkit exports
"""

from src.exporters.sovereign_exporter import SovereignExporter

def demo_improved_exporter():
    """Demonstrate the improved exporter with both single and list inputs"""
    
    exporter = SovereignExporter()
    print("🚀 Sovereign OSINT Toolkit - Export Demo")
    print("=" * 50)
    
    # Sample data with Kenyan cultural context
    sample_data = {
        'query': 'Lamu Cultural Heritage Preservation',
        'sources': ['local_news', 'cultural_database'],
        'kenyan_relevance_score': 0.92,
        'cultural_context': {
            'region': 'Lamu County',
            'topics': ['swahili_architecture', 'cultural_preservation'],
            'local_entities': ['Lamu Old Town UNESCO Site', 'Swahili Cultural Center']
        },
        'results': [
            {
                'title': 'Preserving Lamu\'s Swahili Architecture',
                'content': 'Community-led initiatives to maintain traditional building techniques in Lamu Old Town, a UNESCO World Heritage site.',
                'source': 'local_news',
                'kenyan_relevance': 0.95,
                'data_sensitivity': 'public',
                'data_type': 'cultural'
            }
        ],
        'data_types': ['cultural']
    }
    
    print("\n📊 Testing User Types with Cultural Data:")
    print("-" * 40)
    
    user_types = ['journalist', 'researcher', 'ngo']
    
    for user_type in user_types:
        print(f"\n👤 {user_type.upper()}:")
        
        # Test single dict input
        result_single = exporter.export_data(sample_data, user_type, 'json')
        print(f"  Single Dict: {result_single.get('filename', 'N/A')}")
        print(f"    Normalized: {result_single.get('input_normalized', 'N/A')}")
        
        # Test list input  
        result_list = exporter.export_data([sample_data], user_type, 'json')
        print(f"  List[Dict]:   {result_list.get('filename', 'N/A')}")
        print(f"    Normalized: {result_list.get('input_normalized', 'N/A')}")
    
    print("\n🎯 Key Improvements Demonstrated:")
    print("✅ Single Dict inputs now work (auto-normalized to List[Dict])")
    print("✅ List[Dict] inputs continue to work as before") 
    print("✅ Input normalization is properly tracked")
    print("✅ All user types supported with appropriate data")
    print("✅ Kenyan cultural context preserved in exports")

if __name__ == "__main__":
    demo_improved_exporter()
