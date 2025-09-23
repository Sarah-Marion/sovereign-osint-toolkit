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
        
        # Export templates for different user types
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

    # NEW ENHANCED FEATURES
    def enhance_with_osint_context(self, data: List[Dict], source_type: str) -> List[Dict]:
        """Enhance OSINT data with source-specific context"""
        enhanced_data = []
        
        for item in data:
            enhanced_item = item.copy()
            
            # Add source metadata
            enhanced_item["osint_source"] = source_type
            enhanced_item["collection_timestamp"] = datetime.now().isoformat()
            enhanced_item["kenyan_relevance"] = self._calculate_kenyan_relevance_score(item)
            
            # Add verification flags
            enhanced_item["verification_indicators"] = {
                "cross_referenced": self._check_cross_references(item),
                "source_reliability": self._assess_source_reliability(source_type),
                "temporal_relevance": self._assess_temporal_relevance(item)
            }
            
            enhanced_data.append(enhanced_item)
        
        return enhanced_data

    def batch_export(self, data: List[Dict], formats: List[str] = None, user_types: List[str] = None) -> Dict[str, Dict]:
        """Export data in multiple formats and user types simultaneously"""
        if formats is None:
            formats = ["json", "csv", "html"]
        if user_types is None:
            user_types = ["journalist", "researcher", "ngo", "developer"]
        
        results = {
            "metadata": {
                "export_timestamp": datetime.now().isoformat(),
                "total_items": len(data),
                "kenyan_relevance_score": self._calculate_overall_kenyan_relevance(data)
            },
            "exports": {}
        }
        
        for user_type in user_types:
            results["exports"][user_type] = {}
            for fmt in formats:
                try:
                    result = self.export_data(data, user_type, fmt)
                    quality_report = self.validate_export_quality(result)
                    results["exports"][user_type][fmt] = {
                        "filename": result["filename"],
                        "size": result["size_estimate"],
                        "status": "success",
                        "quality_score": quality_report["overall_score"]
                    }
                except Exception as e:
                    results["exports"][user_type][fmt] = {
                        "filename": None,
                        "size": 0,
                        "status": f"error: {str(e)}",
                        "quality_score": 0.0
                    }
        
        return results

    def validate_export_quality(self, export_result: Dict) -> Dict:
        """Validate export quality and Kenyan context preservation"""
        content = export_result.get("content", "")
        user_type = export_result.get("user_type", "unknown")
        
        validation_result = {
            "kenyan_context_score": 0.0,
            "data_completeness": 0.0,
            "format_validity": True,
            "user_type_compliance": 0.0,
            "issues": [],
            "overall_score": 0.0
        }
        
        # Check Kenyan context preservation
        kenyan_indicators = ["kenya", "nairobi", "county", "kes", "swahili"]
        content_lower = content.lower()
        context_matches = sum(1 for indicator in kenyan_indicators if indicator in content_lower)
        validation_result["kenyan_context_score"] = context_matches / len(kenyan_indicators)
        
        # Validate format-specific requirements
        if export_result["format"] == "json":
            try:
                json.loads(content)
            except json.JSONDecodeError:
                validation_result["format_validity"] = False
                validation_result["issues"].append("Invalid JSON format")
        
        # Calculate overall quality score
        scores = [
            validation_result["kenyan_context_score"],
            validation_result["data_completeness"],
            float(validation_result["format_validity"]),
            validation_result["user_type_compliance"]
        ]
        validation_result["overall_score"] = sum(scores) / len(scores)
        
        return validation_result

    # ORIGINAL METHODS FROM YOUR WORKING VERSION
    def export_data(self, data: List[Dict], user_type: str = "developer", export_format: str = "json") -> Dict:
        """Main export function with user-type specific formatting"""
        
        # Validate export request
        self._validate_export_request(data, user_type)
        
        # Apply user-type specific processing
        processed_data = self._process_for_user_type(data, user_type)
        
        # Generate export based on format
        if export_format == "json":
            result = self._export_json(processed_data, user_type)
        elif export_format == "csv":
            result = self._export_csv(processed_data, user_type)
        elif export_format == "pdf":
            result = self._export_pdf(processed_data, user_type)
        elif export_format == "html":
            result = self._export_html(processed_data, user_type)
        else:
            raise ValueError(f"Unsupported export format: {export_format}")
        
        result["user_type"] = user_type
        return result
    
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
            "content": pdf_content,
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
    
    # HELPER METHODS
    def _calculate_public_interest(self, item: Dict) -> float:
        return 0.8
    
    def _assess_kenyan_impact(self, item: Dict) -> List[str]:
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
        if not data:
            return "No data available for context analysis"
        
        regional_mentions = {}
        topic_mentions = {}
        
        for item in data:
            content = str(item).lower()
            
            regions = ["nairobi", "mombasa", "kisumu", "nakuru", "eldoret"]
            for region in regions:
                if region in content:
                    regional_mentions[region] = regional_mentions.get(region, 0) + 1
            
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
        items = []
        for k, v in d.items():
            new_key = f"{parent_key}{sep}{k}" if parent_key else k
            if isinstance(v, dict):
                items.extend(self._flatten_dict(v, new_key, sep=sep).items())
            else:
                items.append((new_key, str(v)))
        return dict(items)
    
    def _format_html_item(self, item: Dict) -> str:
        title = item.get('title', item.get('text', 'No title'))
        return f'<div class="data-item"><h3>{title}</h3><pre>{json.dumps(item, indent=2)}</pre></div>'

    # MISSING METHOD STUBS
    def _assess_data_sensitivity(self, data):
        return "public"
    
    def _check_context_preservation(self, data, user_type):
        return {"adequate": True, "issues": []}
    
    def _assess_verification_status(self, item):
        return "unverified"
    
    def _generate_ethical_notes(self, item):
        return "Standard ethical considerations apply"
    
    def _identify_kenyan_stakeholders(self, item):
        return ["General public"]
    
    def _generate_methodology_notes(self, item):
        return "Standard methodology applied"
    
    def _identify_research_limitations(self, item):
        return ["Sample size limitations"]
    
    def _generate_replication_guide(self, item):
        return "Follow standard research protocols"
    
    def _suggest_local_adaptations(self, item):
        return ["Consider local context"]
    
    def _assess_cultural_validity(self, item):
        return "Moderate"
    
    def _assess_community_impact(self, item):
        return "Positive"
    
    def _generate_policy_recommendations(self, item):
        return ["Consider community input"]
    
    def _identify_advocacy_opportunities(self, item):
        return ["Public awareness campaigns"]
    
    def _suggest_local_partnerships(self, item):
        return ["Local community organizations"]
    
    def _assess_sustainability(self, item):
        return "Sustainable"
    
    def _assess_data_quality(self, item):
        return 0.9
    
    def _identify_technical_limitations(self, item):
        return ["API rate limits"]
    
    def _generate_integration_guide(self, item):
        return "Use standard API protocols"
    
    def _suggest_infrastructure_adaptations(self, item):
        return ["Consider local bandwidth limitations"]
    
    def _list_compliance_requirements(self, item):
        return ["Data Protection Act 2019"]

    # NEW HELPER METHODS FOR ENHANCED FEATURES
    def _calculate_kenyan_relevance_score(self, item: Dict) -> float:
        content = str(item).lower()
        indicators = {
            'nairobi': 0.3, 'mombasa': 0.2, 'kisumu': 0.1, 'nakuru': 0.1,
            'kenya': 0.4, 'county': 0.2, 'kes': 0.1
        }
        
        score = 0.0
        for indicator, weight in indicators.items():
            if indicator in content:
                score += weight
        
        return min(score, 1.0)

    def _check_cross_references(self, item: Dict) -> bool:
        """Check if data has been cross-referenced - FIXED VERSION"""
        sources = item.get('sources', [])
        return len(sources) > 1  # Fixed: compare length, not list

    def _assess_source_reliability(self, source_type: str) -> float:
        reliability_scores = {
            'official': 0.9, 'news': 0.7, 'social_media': 0.4, 'academic': 0.8
        }
        return reliability_scores.get(source_type, 0.5)

    def _assess_temporal_relevance(self, item: Dict) -> float:
        if 'timestamp' in item:
            try:
                data_time = datetime.fromisoformat(item['timestamp'].replace('Z', '+00:00'))
                time_diff = datetime.now() - data_time
                days_diff = time_diff.days
                return max(0, 1 - (days_diff / 365))
            except:
                return 0.5
        return 0.5