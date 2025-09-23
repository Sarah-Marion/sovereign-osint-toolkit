"""
Professional test suite for SovereignExporter
"""

import sys
import os
import unittest
import json

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from exporters.sovereign_exporter import SovereignExporter

class TestSovereignExporter(unittest.TestCase):
    """Test cases for SovereignExporter"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.exporter = SovereignExporter()
        self.sample_data = [
            {
                'title': 'Nairobi Development Project', 
                'content': 'New infrastructure in Nairobi county', 
                'kenyan_relevance': 0.9,
                'sources': ['source1', 'source2']
            },
            {
                'title': 'Mombasa Tourism Initiative', 
                'content': 'Coastal tourism development in Mombasa', 
                'kenyan_relevance': 0.8,
                'sources': ['source1']
            }
        ]
    
    def test_json_export(self):
        """Test JSON export functionality"""
        result = self.exporter.export_data(self.sample_data, "journalist", "json")
        
        self.assertEqual(result["format"], "json")
        self.assertIn(".json", result["filename"])
        self.assertGreater(result["size_estimate"], 0)
        
        # Verify JSON is valid
        json_data = json.loads(result["content"])
        self.assertIn("metadata", json_data)
        self.assertIn("data", json_data)
    
    def test_csv_export(self):
        """Test CSV export functionality"""
        result = self.exporter.export_data(self.sample_data, "researcher", "csv")
        
        self.assertEqual(result["format"], "csv")
        self.assertIn(".csv", result["filename"])
        self.assertGreater(result["size_estimate"], 0)
        self.assertIn("title", result["content"])
    
    def test_batch_export(self):
        """Test batch export functionality"""
        results = self.exporter.batch_export(self.sample_data, ["json", "csv"])
        
        self.assertIn("metadata", results)
        self.assertIn("exports", results)
        self.assertIn("journalist", results["exports"])
        self.assertIn("json", results["exports"]["journalist"])
    
    def test_quality_validation(self):
        """Test export quality validation"""
        result = self.exporter.export_data(self.sample_data, "developer", "json")
        quality_report = self.exporter.validate_export_quality(result)
        
        self.assertIn("kenyan_context_score", quality_report)
        self.assertIn("overall_score", quality_report)
        self.assertGreaterEqual(quality_report["overall_score"], 0)
        self.assertLessEqual(quality_report["overall_score"], 1)
    
    def test_osint_enhancement(self):
        """Test OSINT context enhancement"""
        enhanced_data = self.exporter.enhance_with_osint_context(self.sample_data, "news")
        
        self.assertEqual(len(enhanced_data), len(self.sample_data))
        self.assertIn("osint_source", enhanced_data[0])
        self.assertIn("verification_indicators", enhanced_data[0])

if __name__ == "__main__":
    # Run only the unittest tests
    unittest.main()