"""
Test Script for SovereignExporter
Fixed version with proper string formatting
"""

from sovereign_exporter import SovereignExporter

def test_exporter():
    """Test the exporter functionality"""
    exporter = SovereignExporter()
    
    # Sample test data
    sample_data = [
        {'title': 'Nairobi Development Project', 'content': 'New infrastructure in Nairobi county', 'kenyan_relevance': 0.9},
        {'title': 'Mombasa Tourism Initiative', 'content': 'Coastal tourism development in Mombasa', 'kenyan_relevance': 0.8}
    ]
    
    print("Testing SovereignExporter...")
    
    try:
        # Test JSON export
        result = exporter.export_data(sample_data, "journalist", "json")
        print(f'✓ JSON export working: {result["filename"]}')
        print(f'  Size: {result["size_estimate"]} bytes')
        
        # Test CSV export  
        result = exporter.export_data(sample_data, "researcher", "csv")
        print(f'✓ CSV export working: {result["filename"]}')
        print(f'  Size: {result["size_estimate"]} bytes')
        
        # Test PDF export
        result = exporter.export_data(sample_data, "ngo", "pdf")
        print(f'✓ PDF export working: {result["filename"]}')
        print(f'  Size: {result["size_estimate"]} bytes')
        
        # Test HTML export
        result = exporter.export_data(sample_data, "developer", "html")
        print(f'✓ HTML export working: {result["filename"]}')
        print(f'  Size: {result["size_estimate"]} bytes')
        
        # Test all user types
        user_types = ["journalist", "researcher", "ngo", "developer"]
        for user_type in user_types:
            result = exporter.export_data(sample_data, user_type, "json")
            print(f'✓ {user_type.title()} export successful: {result["filename"]}')
            
        print("\n🎉 All tests passed! SovereignExporter is working correctly.")
        
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_exporter()