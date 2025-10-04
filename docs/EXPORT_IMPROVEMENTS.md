# Sovereign OSINT Toolkit - Export Improvements

## Enhanced Exporter API

The `SovereignExporter.export_data()` method has been improved to accept both single dictionaries and lists of dictionaries for better user experience.

### Before (v1.0)
```python
# Only worked with List[Dict]
data = [{"query": "test", "results": [...]}]
result = exporter.export_data(data, "journalist", "json")
```

### After (Improved)
```python
# Now works with both Dict and List[Dict]
single_data = {"query": "test", "results": [...]}
result1 = exporter.export_data(single_data, "journalist", "json")  # ✅ Works!

list_data = [single_data]
result2 = exporter.export_data(list_data, "researcher", "json")    # ✅ Still works!
```

### Key Features

1. **Automatic Input Normalization**
   - Single `Dict` → Automatically wrapped in `List[Dict]`
   - `List[Dict]` → Used as-is
   - Tracked via `result["input_normalized"]` flag

2. **User Type Support**
   - **Journalist, Researcher, NGO**: Cultural and public interest data
   - **Developer**: Technical data
   - **Government**: Restricted data (with permissions)

3. **Export Formats**
   - JSON, CSV, HTML exports
   - User-type specific templates
   - Kenyan cultural context preservation


## Usage Examples
```python
from src.exporters.sovereign_exporter import SovereignExporter

exporter = SovereignExporter()

# Single result export
single_result = collector.search("Kenyan topic")
export_result = exporter.export_data(single_result, "journalist", "json")

# Multiple results export  
multiple_results = [result1, result2, result3]
export_result = exporter.export_data(multiple_results, "researcher", "csv")
```


## Validation & Ethics

- Data sensitivity classification (Public to Restricted)

- Kenyan cultural context validation

- Data Protection Act 2019 compliance

- Ethical boundaries enforcement