"""
Sovereign OSINT Toolkit - Export System
Specialized export formats for different user types with Kenyan context preservation
By Sarah Marion
"""

import json
import csv
import io
import yaml
from datetime import datetime
from typing import Dict, List, Any
from pathlib import Path

# Mock the Kenyan context classes
class KenyanContextValidator:
    def validate_context(self, data): return True

class KenyanAnonymization:
    def anonymize(self, data): return data

class SovereignExporter:
    """Export system that preserves Kenyan context for different user types"""
    
    def __init__(self, config_path: str = None):
        self.kenyan_context = KenyanContextValidator()
        self.anonymizer = KenyanAnonymization()
        
        # Load export profiles configuration
        self.export_profiles = self._load_export_profiles(config_path)
        
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

    def _load_export_profiles(self, config_path: str) -> Dict:
        """Load export profiles from YAML configuration"""
        default_profiles = {
            "journalist": {
                "required_fields": ["title", "source", "verification_status", "public_interest"],
                "sensitivity_level": "public",
                "kenyan_context": ["regional_impact", "stakeholder_analysis"]
            },
            "researcher": {
                "required_fields": ["methodology", "limitations", "citations", "replicability"],
                "sensitivity_level": "research",
                "kenyan_context": ["cultural_validity", "local_adaptation"]
            },
            "ngo": {
                "required_fields": ["community_impact", "policy_recommendations", "sustainability"],
                "sensitivity_level": "community",
                "kenyan_context": ["local_partnerships", "advocacy_opportunities"]
            },
            "developer": {
                "required_fields": ["data_schema", "api_spec", "technical_limitations"],
                "sensitivity_level": "technical",
                "kenyan_context": ["infrastructure_requirements", "compliance"]
            }
        }
        return default_profiles

    # ENHANCED EXPORT WITH REAL DATA INTEGRATION
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

    # BATCH EXPORT CAPABILITY
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
                    results["exports"][user_type][fmt] = {
                        "filename": result["filename"],
                        "size": result["size_estimate"],
                        "status": "success",
                        "quality_score": self.validate_export_quality(result)["overall_score"]
                    }
                except Exception as e:
                    results["exports"][user_type][fmt] = {
                        "filename": None,
                        "size": 0,
                        "status": f"error: {str(e)}",
                        "quality_score": 0.0
                    }
        
        return results

    # QUALITY ASSURANCE CHECKS
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
        kenyan_indicators = ["Kenya", "Nairobi", "county", "KES", "Swahili"]
        context_matches = sum(1 for indicator in kenyan_indicators if indicator.lower() in content.lower())
        validation_result["kenyan_context_score"] = context_matches / len(kenyan_indicators)
        
        # Check data completeness based on user type requirements
        profile_requirements = self.export_profiles.get(user_type, {}).get("required_fields", [])
        if profile_requirements:
            completeness = sum(1 for field in profile_requirements if field in content) / len(profile_requirements)
            validation_result["data_completeness"] = completeness
        
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

    # EXISTING METHODS (from your current implementation)
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

    # ... [ALL YOUR EXISTING METHODS REMAIN UNCHANGED] ...
    # _validate_export_request, _process_for_user_type, _export_json, _export_csv, etc.
    # Keep all your current methods exactly as they are

    # NEW HELPER METHODS FOR ENHANCED FEATURES
    def _calculate_kenyan_relevance_score(self, item: Dict) -> float:
        """Calculate detailed Kenyan relevance score"""
        content = str(item).lower()
        indicators = {
            'nairobi': 0.3, 'mombasa': 0.2, 'kisumu': 0.1, 'nakuru': 0.1,
            'kenya': 0.4, 'county': 0.2, 'kes': 0.1, 'nairobi': 0.3
        }
        
        score = 0.0
        for indicator, weight in indicators.items():
            if indicator in content:
                score += weight
        
        return min(score, 1.0)

    def _check_cross_references(self, item: Dict) -> bool:
        """Check if data has been cross-referenced"""
        return item.get('sources', []) > 1

    def _assess_source_reliability(self, source_type: str) -> float:
        """Assess reliability of OSINT source"""
        reliability_scores = {
            'official': 0.9, 'news': 0.7, 'social_media': 0.4, 'academic': 0.8
        }
        return reliability_scores.get(source_type, 0.5)

    def _assess_temporal_relevance(self, item: Dict) -> float:
        """Assess how current the information is"""
        if 'timestamp' in item:
            data_time = datetime.fromisoformat(item['timestamp'])
            time_diff = datetime.now() - data_time
            days_diff = time_diff.days
            return max(0, 1 - (days_diff / 365))  # 1.0 for current, 0.0 for year-old
        return 0.5