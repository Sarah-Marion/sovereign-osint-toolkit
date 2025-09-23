"""
Sovereign OSINT Toolkit - Main Application
Integrated export system with Kenyan context preservation
"""

import sys
import os

# Add the src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from exporters.sovereign_exporter import SovereignExporter
from collectors.osint_collector import OSINTCollector

class SovereignOSINTToolkit:
    def __init__(self):
        self.collector = OSINTCollector()  # ✅ UNCOMMENTED - FIXED
        self.exporter = SovereignExporter()
    
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

def main():
    toolkit = SovereignOSINTToolkit()
    
    # Ensure exports directory exists
    os.makedirs("exports", exist_ok=True)
    
    # Example usage
    queries = [
        "Nairobi infrastructure development",
        "Kenyan digital economy", 
        "Mombasa tourism 2024"
    ]
    
    for query in queries:
        print(f"\n{'='*50}")
        print(f"Processing: {query}")
        print('='*50)
        
        # Test different user types
        for user_type in ["journalist", "researcher", "ngo", "developer"]:
            result = toolkit.run_workflow(query, user_type, "json")
            
            # Save to file
            filename = f"exports/{result['filename']}"
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(result['content'])
            print(f"💾 Saved: {filename}")
            
            # Also test batch export for comprehensive coverage
            if user_type == "researcher":
                batch_result = toolkit.exporter.batch_export(
                    [{'title': query, 'content': f'Batch export test for {query}'}],
                    ["json", "csv", "html"]
                )
                print(f"📦 Batch export: {len(batch_result['exports'])} user types")

if __name__ == "__main__":
    main()