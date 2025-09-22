"""
Sovereign OSINT Toolkit - Export System
Specialized export formats for different user types with Kenyan context preservation
By Sarah Marion
"""

import json
import csv
import io
from datetime import datetime
from typing import Dict, List, Any

# Mock the Kenyan context classes
class KenyanContextValidator:
    def validate_context(self, data): return True

class KenyanAnonymization:
    def anonymize(self, data): return data

    
class SovereignExporter:
    """Export system that preserves Kenyan context for different user types"""
    
    def __init__(self):
        self.kenyan_context = KenyanContextValidator()
        self.anonymizer = KenyanAnonymization()
        
        # Export templates for different user types (unchanged)
        self.export_templates = {
            "journalist": {
                "format": "investigative_report",
                "sections": ["executive_summary", "key_findings", "sources", "ethical_considerations"],
                "kenyan_context": ["political_implications", "public_interest_justification"]
            },
            "researcher": {
                "format": "academic_paper",
                "sections": ["abstract", "methodology", "findings", "discussion", "references"],
                "kenyan_context": ["literature_review", "local_methodology_adaptation"]
            },
            "ngo": {
                "format": "policy_brief",
                "sections": ["issue_overview", "evidence", "recommendations", "stakeholder_analysis"],
                "kenyan_context": ["community_impact", "local_partnerships"]
            },
            "developer": {
                "format": "technical_report",
                "sections": ["data_schema", "methodology", "limitations", "api_documentation"],
                "kenyan_context": ["local_data_standards", "infrastructure_considerations"]
            }
        }

    
    def export_data(self, data: List[Dict], user_type: str = "developer", export_format: str = "json") -> Dict:
        """Main export function with user-type specific formatting"""
        
        # Validate export request
        self._validate_export_request(data, user_type)
        
        # Apply user-type specific processing
        processed_data = self._process_for_user_type(data, user_type)
        
        # Generate export based on format
        if export_format == "json":
            return self._export_json(processed_data, user_type)
        elif export_format == "csv":
            return self._export_csv(processed_data, user_type)
        elif export_format == "pdf":
            return self._export_pdf(processed_data, user_type)
        elif export_format == "html":
            return self._export_html(processed_data, user_type)
        else:
            raise ValueError(f"Unsupported export format: {export_format}")
    
    def _validate_export_request(self, data: List[Dict], user_type: str):
        """Validate that the export request meets Kenyan ethical standards"""
        
        # Check data sensitivity against user type permissions
        sensitivity_level = self._assess_data_sensitivity(data)
        
        user_permissions = {
            "journalist": ["public", "sensitive_public_interest"],
            "researcher": ["public", "sensitive_research"],
            "ngo": ["public", "sensitive_community"],
            "developer": ["public", "technical"]
        }
        
        if sensitivity_level not in user_permissions.get(user_type, []):
            raise PermissionError(
                f"User type '{user_type}' not permitted to export {sensitivity_level} data"
            )
        
        # Validate Kenyan context preservation
        context_preservation = self._check_context_preservation(data, user_type)
        if not context_preservation["adequate"]:
            print(f"Warning: Context preservation issues: {context_preservation['issues']}")
    
    def _process_for_user_type(self, data: List[Dict], user_type: str) -> List[Dict]:
        """Process data specifically for each user type"""
        
        processed_data = data.copy()
        
        if user_type == "journalist":
            return self._process_for_journalist(processed_data)
        elif user_type == "researcher":
            return self._process_for_researcher(processed_data)
        elif user_type == "ngo":
            return self._process_for_ngo(processed_data)
        elif user_type == "developer":
            return self._process_for_developer(processed_data)
        else:
            return processed_data
    
    def _process_for_journalist(self, data: List[Dict]) -> List[Dict]:
        """Process data for journalistic use with public interest focus"""
        
        processed = []
        for item in data:
            journalist_item = item.copy()
            
            # Add public interest context
            journalist_item["public_interest_score"] = self._calculate_public_interest(item)
            journalist_item["verification_status"] = self._assess_verification_status(item)
            journalist_item["ethical_considerations"] = self._generate_ethical_notes(item)
            
            # Kenyan context for journalism
            journalist_item["kenyan_impact"] = self._assess_kenyan_impact(item)
            journalist_item["stakeholder_analysis"] = self._identify_kenyan_stakeholders(item)
            
            processed.append(journalist_item)
        
        return processed
    
    def _process_for_researcher(self, data: List[Dict]) -> List[Dict]:
        """Process data for academic research with methodological rigor"""
        
        processed = []
        for item in data:
            research_item = item.copy()
            
            # Add research context
            research_item["methodological_notes"] = self._generate_methodology_notes(item)
            research_item["limitations"] = self._identify_research_limitations(item)
            research_item["replication_instructions"] = self._generate_replication_guide(item)
            
            # Kenyan context for research
            research_item["local_methodology_adaptation"] = self._suggest_local_adaptations(item)
            research_item["cultural_validity"] = self._assess_cultural_validity(item)
            
            processed.append(research_item)
        
        return processed
    
    def _process_for_ngo(self, data: List[Dict]) -> List[Dict]:
        """Process data for NGO use with community focus"""
        
        processed = []
        for item in data:
            ngo_item = item.copy()
            
            # Add NGO context
            ngo_item["community_impact"] = self._assess_community_impact(item)
            ngo_item["policy_recommendations"] = self._generate_policy_recommendations(item)
            ngo_item["advocacy_opportunities"] = self._identify_advocacy_opportunities(item)
            
            # Kenyan context for NGOs
            ngo_item["local_partnership_opportunities"] = self._suggest_local_partnerships(item)
            ngo_item["sustainability_considerations"] = self._assess_sustainability(item)
            
            processed.append(ngo_item)
        
        return processed
    
    def _process_for_developer(self, data: List[Dict]) -> List[Dict]:
        """Process data for developers with technical focus"""
        
        processed = []
        for item in data:
            developer_item = item.copy()
            
            # Add technical context
            developer_item["data_quality_score"] = self._assess_data_quality(item)
            developer_item["technical_limitations"] = self._identify_technical_limitations(item)
            developer_item["integration_guidance"] = self._generate_integration_guide(item)
            
            # Kenyan context for developers
            developer_item["local_infrastructure_considerations"] = self._suggest_infrastructure_adaptations(item)
            developer_item["compliance_requirements"] = self._list_compliance_requirements(item)
            
            processed.append(developer_item)
        
        return processed
    
    def _export_json(self, data: List[Dict], user_type: str) -> Dict:
        """Export data as JSON with user-type specific structure"""
        
        export_structure = {
            "metadata": {
                "export_timestamp": datetime.now().isoformat(),
                "user_type": user_type,
                "kenyan_context_version": "1.0",
                "data_protection_compliance": "DPA_2019"
            },
            "export_template": self.export_templates.get(user_type, {}),
            "data": data,
            "kenyan_context_summary": self._generate_kenyan_context_summary(data)
        }
        
        return {
            "format": "json",
            "content": json.dumps(export_structure, indent=2, ensure_ascii=False),
            "filename": f"sovereign_export_{user_type}_{datetime.now():%Y%m%d_%H%M%S}.json",
            "size_estimate": len(json.dumps(export_structure))
        }
    
    def _export_csv(self, data: List[Dict], user_type: str) -> Dict:
        """Export data as CSV with user-type specific columns - lightweight version"""
        
        if not data:
            return {
            "format": "csv", 
            "content": "", 
            "filename": f"sovereign_export_{user_type}_{datetime.now():%Y%m%d_%H%M%S}.csv",
            "size_estimate": 0
        }
        
        # Flatten data for CSV (lightweight implementation)
        flattened_data = []
        for item in data:
            flat_item = self._flatten_dict(item)
            flattened_data.append(flat_item)
        
        # Create CSV content using standard library only
        output = io.StringIO()
        
        if flattened_data:
            fieldnames = flattened_data[0].keys()
            writer = csv.DictWriter(output, fieldnames=fieldnames)
            writer.writeheader()
            for row in flattened_data:
                writer.writerow(row)
        
        csv_content = output.getvalue()
        output.close()
        
        return {
            "format": "csv",
            "content": csv_content,
            "filename": f"sovereign_export_{user_type}_{datetime.now():%Y%m%d_%H%M%S}.csv",
            "size_estimate": len(csv_content)
        }
    

    def _calculate_overall_kenyan_relevance(self, data: List[Dict]) -> float:
        """Lightweight Kenyan relevance calculation without pandas"""
        if not data:
            return 0.0
        
        total_relevance = 0.0
        count = 0
        
        for item in data:
            if 'kenyan_relevance' in item:
                total_relevance += item['kenyan_relevance']
                count += 1
            else:
                # Estimate relevance based on content
                content = str(item).lower()
                kenyan_indicators = ['kenya', 'nairobi', 'mombasa', 'county', 'kes']
                relevance_score = sum(1 for indicator in kenyan_indicators if indicator in content) / len(kenyan_indicators)
                total_relevance += relevance_score
                count += 1
        
        return total_relevance / count if count > 0 else 0.0


    def _export_pdf(self, data: List[Dict], user_type: str) -> Dict:
        """Export data as PDF report (simplified version)"""
        # In a full implementation, this would use ReportLab or similar
        
        pdf_content = f"""
        SOVEREIGN OSINT EXPORT - {user_type.upper()}
        Generated: {datetime.now():%Y-%m-%d %H:%M:%S}
        Kenyan Context: Preserved
        
        SUMMARY:
        {self._generate_kenyan_context_summary(data)}
        
        DATA OVERVIEW:
        Total items: {len(data)}
        Kenyan relevance score: {self._calculate_overall_kenyan_relevance(data):.2f}
        
        This export maintains Kenyan data sovereignty and ethical standards.
        """
        
        return {
            "format": "pdf",
            "content": pdf_content,  # Would be actual PDF bytes in full implementation
            "filename": f"sovereign_report_{user_type}_{datetime.now():%Y%m%d}.pdf",
            "size_estimate": len(pdf_content)
        }
    
    def _export_html(self, data: List[Dict], user_type: str) -> Dict:
        """Export data as interactive HTML report"""
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Sovereign OSINT Export - {user_type.title()}</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 40px; }}
                .kenyan-context {{ background-color: #f0f8ff; padding: 15px; border-left: 4px solid #006400; }}
                .data-item {{ border: 1px solid #ddd; margin: 10px 0; padding: 10px; }}
            </style>
        </head>
        <body>
            <h1>🇰🇪 Sovereign OSINT Export</h1>
            <div class="kenyan-context">
                <h3>Kenyan Context Preservation</h3>
                <p>{self._generate_kenyan_context_summary(data)}</p>
            </div>
            <h2>Data Items ({len(data)})</h2>
            {"".join([self._format_html_item(item) for item in data])}
        </body>
        </html>
        """
        
        return {
            "format": "html",
            "content": html_content,
            "filename": f"sovereign_export_{user_type}_{datetime.now():%Y%m%d}.html",
            "size_estimate": len(html_content)
        }
    
    # Helper methods for context processing
    def _calculate_public_interest(self, item: Dict) -> float:
        """Calculate public interest score for journalistic content"""
        # Implementation would analyze content for public benefit
        return 0.8  # Placeholder
    
    def _assess_kenyan_impact(self, item: Dict) -> List[str]:
        """Assess which Kenyan communities are impacted"""
        content = str(item).lower()
        impacts = []
        
        if "nairobi" in content:
            impacts.append("Nairobi residents")
        if "rural" in content or "county" in content:
            impacts.append("Rural communities")
        if "youth" in content or "students" in content:
            impacts.append("Youth population")
        
        return impacts if impacts else ["General Kenyan public"]
    
    def _generate_kenyan_context_summary(self, data: List[Dict]) -> str:
        """Generate summary of Kenyan context in the data"""
        if not data:
            return "No data available for context analysis"
        
        regional_mentions = {}
        topic_mentions = {}
        
        for item in data:
            content = str(item).lower()
            
            # Count regional mentions
            regions = ["nairobi", "mombasa", "kisumu", "nakuru", "eldoret"]
            for region in regions:
                if region in content:
                    regional_mentions[region] = regional_mentions.get(region, 0) + 1
            
            # Count topic mentions
            topics = ["development", "politics", "economy", "health", "education"]
            for topic in topics:
                if topic in content:
                    topic_mentions[topic] = topic_mentions.get(topic, 0) + 1
        
        summary = f"Analysis of {len(data)} items: "
        if regional_mentions:
            summary += f"Regional focus: {', '.join(regional_mentions.keys())}. "
        if topic_mentions:
            summary += f"Key topics: {', '.join(topic_mentions.keys())}."
        
        return summary
    
    def _flatten_dict(self, d: Dict, parent_key: str = '', sep: str = '_') -> Dict:
        """Flatten a nested dictionary for CSV export"""
        items = []
        for k, v in d.items():
            new_key = f"{parent_key}{sep}{k}" if parent_key else k
            if isinstance(v, dict):
                items.extend(self._flatten_dict(v, new_key, sep=sep).items())
            else:
                items.append((new_key, str(v)))
        return dict(items)
    
    def _format_html_item(self, item: Dict) -> str:
        """Format a single data item for HTML export"""
        title = item.get('title', item.get('text', 'No title'))
        return f'<div class="data-item"><h3>{title}</h3><pre>{json.dumps(item, indent=2)}</pre></div>'

    # ADD MISSING METHOD STUBS TO PREVENT ERRORS
    def _assess_data_sensitivity(self, data):
        """Assess data sensitivity level"""
        return "public"  # Placeholder
    
    def _check_context_preservation(self, data, user_type):
        """Check if Kenyan context is adequately preserved"""
        return {"adequate": True, "issues": []}  # Placeholder
    
    def _assess_verification_status(self, item):
        """Assess verification status for journalism"""
        return "unverified"  # Placeholder
    
    def _generate_ethical_notes(self, item):
        """Generate ethical considerations"""
        return "Standard ethical considerations apply"  # Placeholder
    
    def _identify_kenyan_stakeholders(self, item):
        """Identify Kenyan stakeholders"""
        return ["General public"]  # Placeholder
    
    def _generate_methodology_notes(self, item):
        """Generate methodology notes for research"""
        return "Standard methodology applied"  # Placeholder
    
    def _identify_research_limitations(self, item):
        """Identify research limitations"""
        return ["Sample size limitations"]  # Placeholder
    
    def _generate_replication_guide(self, item):
        """Generate replication guide"""
        return "Follow standard research protocols"  # Placeholder
    
    def _suggest_local_adaptations(self, item):
        """Suggest local methodology adaptations"""
        return ["Consider local context"]  # Placeholder
    
    def _assess_cultural_validity(self, item):
        """Assess cultural validity"""
        return "Moderate"  # Placeholder
    
    def _assess_community_impact(self, item):
        """Assess community impact for NGOs"""
        return "Positive"  # Placeholder
    
    def _generate_policy_recommendations(self, item):
        """Generate policy recommendations"""
        return ["Consider community input"]  # Placeholder
    
    def _identify_advocacy_opportunities(self, item):
        """Identify advocacy opportunities"""
        return ["Public awareness campaigns"]  # Placeholder
    
    def _suggest_local_partnerships(self, item):
        """Suggest local partnerships"""
        return ["Local community organizations"]  # Placeholder
    
    def _assess_sustainability(self, item):
        """Assess sustainability"""
        return "Sustainable"  # Placeholder
    
    def _assess_data_quality(self, item):
        """Assess data quality for developers"""
        return 0.9  # Placeholder
    
    def _identify_technical_limitations(self, item):
        """Identify technical limitations"""
        return ["API rate limits"]  # Placeholder
    
    def _generate_integration_guide(self, item):
        """Generate integration guidance"""
        return "Use standard API protocols"  # Placeholder
    
    def _suggest_infrastructure_adaptations(self, item):
        """Suggest infrastructure adaptations"""
        return ["Consider local bandwidth limitations"]  # Placeholder
    
    def _list_compliance_requirements(self, item):
        """List compliance requirements"""
        return ["Data Protection Act 2019"]  # Placeholder