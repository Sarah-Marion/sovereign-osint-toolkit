"""
Simple test for SovereignExporter
"""

import sys
import os
import json

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from exporters.sovereign_exporter import SovereignExporter

def test_basic_functionality():
    """Test basic exporter functionality"""
    exporter = SovereignExporter()
    
    sample_data = [
        {'title': 'Nairobi Project', 'content': 'Test content', 'kenyan_relevance': 0.9},
        {'title': 'Mombasa Initiative', 'content': 'More test content', 'kenyan_relevance': 0.8}
    ]
    
    print("Testing SovereignExporter...")
    
    # Test JSON export
    result = exporter.export_data(sample_data, "journalist", "json")
    print(f"✓ JSON export: {result['filename']}")
    
    # Test CSV export
    result = exporter.export_data(sample_data, "researcher", "csv")
    print(f"✓ CSV export: {result['filename']}")
    
    # Test batch export
    batch_result = exporter.batch_export(sample_data)
    print(f"✓ Batch export: {len(batch_result['exports'])} user types")
    
    # Test OSINT enhancement
    enhanced_data = exporter.enhance_with_osint_context(sample_data, "news")
    print(f"✓ OSINT enhancement: {len(enhanced_data)} items enhanced")
    
    # Test quality validation
    quality = exporter.validate_export_quality(result)
    print(f"✓ Quality score: {quality['overall_score']:.2f}")
    
    print("🎉 All basic tests passed!")

if __name__ == "__main__":
    test_basic_functionality()