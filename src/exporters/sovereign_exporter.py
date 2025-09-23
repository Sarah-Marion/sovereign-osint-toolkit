"""
Sovereign OSINT Toolkit - Export System
Specialized export formats for different user types with Kenyan context preservation
By Sarah Marion
"""

import json
import csv
import io
import re
from datetime import datetime, timezone
from typing import Dict, List, Any, Optional
from pathlib import Path
from enum import Enum


class DataSensitivityLevel(Enum):
    PUBLIC = "public"
    SENSITIVE_PUBLIC_INTEREST = "sensitive_public_interest"
    SENSITIVE_RESEARCH = "sensitive_research"
    SENSITIVE_COMMUNITY = "sensitive_community"
    TECHNICAL = "technical"
    RESTRICTED = "restricted"


class KenyanContextValidator:
    """Enhanced Kenyan context validation with regional awareness"""
    
    KENYAN_REGIONS = {
        'nairobi': 'Nairobi County',
        'mombasa': 'Mombasa County', 
        'kisumu': 'Kisumu County',
        'nakuru': 'Nakuru County',
        'eldoret': 'Uasin Gishu County',
        'kakamega': 'Kakamega County',
        'kisii': 'Kisii County',
        'nyeri': 'Nyeri County',
        'lamu': 'Lamu County',
        'garissa': 'Garissa County'
    }
    
    KENYAN_INDICATORS = [
        'kenya', 'nairobi', 'mombasa', 'kisumu', 'nakuru', 'eldoret',
        'county', 'kes', 'kwanza', 'uhuru', 'ruto', 'raila',
        'matatu', 'nyama choma', 'safaricom', 'mpesa'
    ]
    
    def validate_context(self, data: Any) -> Dict[str, Any]:
        """Comprehensive Kenyan context validation"""
        validation_result = {
            "has_kenyan_context": False,
            "regional_mentions": [],
            "cultural_relevance": 0.0,
            "data_sovereignty_compliant": True,
            "issues": [],
            "recommendations": []
        }
        
        if not data:
            return validation_result
            
        content = str(data).lower()
        
        # Check for Kenyan regional mentions
        regional_mentions = []
        for region, county in self.KENYAN_REGIONS.items():
            if region in content:
                regional_mentions.append(county)
        
        validation_result["regional_mentions"] = regional_mentions
        validation_result["has_kenyan_context"] = len(regional_mentions) > 0
        
        # Calculate cultural relevance score
        indicator_matches = sum(1 for indicator in self.KENYAN_INDICATORS if indicator in content)
        validation_result["cultural_relevance"] = indicator_matches / len(self.KENYAN_INDICATORS)
        
        # Check data sovereignty compliance
        if 'personal_data' in content and 'consent' not in content:
            validation_result["data_sovereignty_compliant"] = False
            validation_result["issues"].append("Potential personal data processing without consent mention")
            
        # Generate recommendations
        if validation_result["cultural_relevance"] < 0.3:
            validation_result["recommendations"].append("Consider adding more Kenyan context for local relevance")
            
        return validation_result


class KenyanAnonymization:
    """Enhanced anonymization for Kenyan data protection compliance"""
    
    SENSITIVE_PATTERNS = [
        r'\b\d{8,12}\b',  # Phone numbers
        r'\b\d{10,15}\b',  # ID numbers
        r'\b[A-Z0-9]{6,12}\b',  # License plates, IDs
    ]
    
    def anonymize(self, data: Any, aggression_level: str = "medium") -> Any:
        """Anonymize sensitive information with configurable aggression"""
        if isinstance(data, str):
            return self._anonymize_text(data, aggression_level)
        elif isinstance(data, dict):
            return self._anonymize_dict(data, aggression_level)
        elif isinstance(data, list):
            return [self.anonymize(item, aggression_level) for item in data]
        else:
            return data
    
    def _anonymize_text(self, text: str, aggression_level: str) -> str:
        """Anonymize text content"""
        anonymized = text
        
        # Replace sensitive patterns based on aggression level
        replacements = {
            "low": "[REDACTED_SENSITIVE]",
            "medium": "[REDACTED]",
            "high": "[***]"
        }
        replacement = replacements.get(aggression_level, "[REDACTED]")
        
        for pattern in self.SENSITIVE_PATTERNS:
            anonymized = re.sub(pattern, replacement, anonymized)
            
        return anonymized
    
    def _anonymize_dict(self, data: Dict, aggression_level: str) -> Dict:
        """Anonymize dictionary keys and values"""
        sensitive_keys = ['phone', 'id', 'identification', 'passport', 'license', 'email']
        
        anonymized = {}
        for key, value in data.items():
            if any(sensitive in key.lower() for sensitive in sensitive_keys):
                anonymized[key] = self.anonymize(value, aggression_level)
            else:
                anonymized[key] = value
                
        return anonymized


class SovereignExporter:
    """Unified export system with enhanced Kenyan context preservation"""
    
    def __init__(self, config: Optional[Dict] = None):
        self.kenyan_context = KenyanContextValidator()
        self.anonymizer = KenyanAnonymization()
        
        # Enhanced configuration with defaults
        self.config = {
            "enable_anonymization": True,
            "anonymization_level": "medium",
            "validate_context": True,
            "include_metadata": True,
            "quality_validation": True,
            **({} if config is None else config)
        }
        
        # Enhanced export templates for different user types
        self.export_templates = {
            "journalist": {
                "format": "investigative_report",
                "sections": ["executive_summary", "key_findings", "sources", "ethical_considerations"],
                "kenyan_context": ["political_implications", "public_interest_justification", "local_stakeholders"],
                "required_fields": ["title", "source", "timestamp", "public_interest_score"],
                "sensitivity_allowed": [DataSensitivityLevel.PUBLIC, DataSensitivityLevel.SENSITIVE_PUBLIC_INTEREST]
            },
            "researcher": {
                "format": "academic_paper",
                "sections": ["abstract", "methodology", "findings", "discussion", "references"],
                "kenyan_context": ["literature_review", "local_methodology_adaptation", "cultural_validity"],
                "required_fields": ["methodology", "limitations", "replication_data"],
                "sensitivity_allowed": [DataSensitivityLevel.PUBLIC, DataSensitivityLevel.SENSITIVE_RESEARCH]
            },
            "ngo": {
                "format": "policy_brief",
                "sections": ["issue_overview", "evidence", "recommendations", "stakeholder_analysis"],
                "kenyan_context": ["community_impact", "local_partnerships", "sustainability"],
                "required_fields": ["community_impact", "policy_recommendations", "stakeholders"],
                "sensitivity_allowed": [DataSensitivityLevel.PUBLIC, DataSensitivityLevel.SENSITIVE_COMMUNITY]
            },
            "developer": {
                "format": "technical_report",
                "sections": ["data_schema", "methodology", "limitations", "api_documentation"],
                "kenyan_context": ["local_data_standards", "infrastructure_considerations", "compliance"],
                "required_fields": ["data_schema", "technical_specs", "integration_guide"],
                "sensitivity_allowed": [DataSensitivityLevel.PUBLIC, DataSensitivityLevel.TECHNICAL]
            },
            "government": {
                "format": "official_report",
                "sections": ["executive_summary", "detailed_analysis", "recommendations", "implementation_plan"],
                "kenyan_context": ["national_impact", "county_coordination", "legal_framework"],
                "required_fields": ["official_ref", "approval_status", "classification"],
                "sensitivity_allowed": [DataSensitivityLevel.PUBLIC, DataSensitivityLevel.RESTRICTED]
            }
        }

    def enhance_with_osint_context(self, data: List[Dict], source_type: str, metadata: Optional[Dict] = None) -> List[Dict]:
        """Enhanced OSINT data with comprehensive source-specific context"""
        enhanced_data = []
        
        for item in data:
            enhanced_item = item.copy()
            
            # Add enhanced source metadata
            enhanced_item["osint_metadata"] = {
                "source_type": source_type,
                "collection_timestamp": datetime.now(timezone.utc).isoformat(),
                "kenyan_relevance": self._calculate_kenyan_relevance_score(item),
                "source_verification_level": self._assess_source_reliability(source_type),
                "context_validation": self.kenyan_context.validate_context(item)
            }
            
            # Enhanced verification flags
            enhanced_item["verification_indicators"] = {
                "cross_referenced": self._check_cross_references(item),
                "source_reliability_score": self._assess_source_reliability(source_type),
                "temporal_relevance": self._assess_temporal_relevance(item),
                "geographic_consistency": self._check_geographic_consistency(item),
                "corroboration_level": self._assess_corroboration(item)
            }
            
            # Add custom metadata if provided
            if metadata:
                enhanced_item["custom_metadata"] = metadata
            
            enhanced_data.append(enhanced_item)
        
        return enhanced_data

    def batch_export(self, data: List[Dict], formats: List[str] = None, 
                    user_types: List[str] = None, output_dir: Optional[Path] = None) -> Dict[str, Any]:
        """Enhanced batch export with file writing and comprehensive reporting"""
        if formats is None:
            formats = ["json", "csv", "html", "pdf"]
        if user_types is None:
            user_types = ["journalist", "researcher", "ngo", "developer"]
        
        results = {
            "metadata": {
                "export_timestamp": datetime.now(timezone.utc).isoformat(),
                "total_items": len(data),
                "kenyan_relevance_score": self._calculate_overall_kenyan_relevance(data),
                "context_validation": self.kenyan_context.validate_context(data),
                "export_config": self.config
            },
            "exports": {},
            "quality_report": {},
            "files_written": []
        }
        
        # Apply anonymization if enabled
        if self.config["enable_anonymization"]:
            data = self.anonymizer.anonymize(data, self.config["anonymization_level"])
        
        for user_type in user_types:
            if user_type not in self.export_templates:
                print(f"Warning: Unknown user type '{user_type}', skipping...")
                continue
                
            results["exports"][user_type] = {}
            
            for fmt in formats:
                try:
                    export_result = self.export_data(data, user_type, fmt)
                    quality_report = self.validate_export_quality(export_result)
                    
                    # Write to file if output directory provided
                    file_path = None
                    if output_dir:
                        file_path = self._write_export_to_file(export_result, output_dir)
                    
                    results["exports"][user_type][fmt] = {
                        "filename": export_result["filename"],
                        "file_path": str(file_path) if file_path else None,
                        "size_bytes": len(export_result["content"]),
                        "status": "success",
                        "quality_score": quality_report["overall_score"],
                        "content_preview": export_result["content"][:200] + "..." if len(export_result["content"]) > 200 else export_result["content"]
                    }
                    
                    if file_path:
                        results["files_written"].append(str(file_path))
                        
                except Exception as e:
                    results["exports"][user_type][fmt] = {
                        "filename": None,
                        "file_path": None,
                        "size_bytes": 0,
                        "status": f"error: {str(e)}",
                        "quality_score": 0.0,
                        "content_preview": None
                    }
        
        # Generate overall quality report
        results["quality_report"] = self._generate_overall_quality_report(results)
        
        return results

    def export_data(self, data: List[Dict], user_type: str = "developer", export_format: str = "json") -> Dict[str, Any]:
        """Enhanced main export function with comprehensive error handling"""
        
        if user_type not in self.export_templates:
            raise ValueError(f"Unsupported user type: {user_type}")
        
        # Validate export request with enhanced checks
        validation_result = self._validate_export_request(data, user_type)
        if not validation_result["valid"]:
            raise PermissionError(f"Export validation failed: {validation_result['issues']}")
        
        # Apply user-type specific processing
        processed_data = self._process_for_user_type(data, user_type)
        
        # Apply anonymization if enabled
        if self.config["enable_anonymization"]:
            processed_data = self.anonymizer.anonymize(processed_data, self.config["anonymization_level"])
        
        # Generate export based on format
        format_handlers = {
            "json": self._export_json,
            "csv": self._export_csv,
            "pdf": self._export_pdf,
            "html": self._export_html
        }
        
        if export_format not in format_handlers:
            raise ValueError(f"Unsupported export format: {export_format}")
        
        try:
            result = format_handlers[export_format](processed_data, user_type)
            result["user_type"] = user_type
            result["validation_result"] = validation_result
            return result
        except Exception as e:
            raise RuntimeError(f"Export generation failed for {export_format}: {str(e)}")

    def validate_export_quality(self, export_result: Dict) -> Dict[str, Any]:
        """Comprehensive export quality validation"""
        content = export_result.get("content", "")
        user_type = export_result.get("user_type", "unknown")
        export_format = export_result.get("format", "unknown")
        
        validation_result = {
            "kenyan_context_score": 0.0,
            "data_completeness": 0.0,
            "format_validity": True,
            "user_type_compliance": 0.0,
            "ethical_compliance": True,
            "performance_metrics": {},
            "issues": [],
            "warnings": [],
            "overall_score": 0.0
        }
        
        # Check Kenyan context preservation
        context_validation = self.kenyan_context.validate_context(content)
        validation_result["kenyan_context_score"] = context_validation["cultural_relevance"]
        
        if not context_validation["data_sovereignty_compliant"]:
            validation_result["ethical_compliance"] = False
            validation_result["issues"].append("Data sovereignty compliance issues detected")
        
        # Validate format-specific requirements
        format_validators = {
            "json": self._validate_json_export,
            "csv": self._validate_csv_export,
            "html": self._validate_html_export
        }
        
        if export_format in format_validators:
            format_validation = format_validators[export_format](content)
            validation_result["format_validity"] = format_validation["valid"]
            validation_result["issues"].extend(format_validation["issues"])
        
        # Check user-type compliance
        template = self.export_templates.get(user_type, {})
        validation_result["user_type_compliance"] = self._assess_user_type_compliance(content, template)
        
        # Performance metrics
        validation_result["performance_metrics"] = {
            "content_size": len(content),
            "processing_time": export_result.get("processing_time", 0),
            "compression_ratio": self._calculate_compression_ratio(content)
        }
        
        # Calculate overall quality score
        scores = [
            validation_result["kenyan_context_score"],
            validation_result["data_completeness"],
            float(validation_result["format_validity"]),
            validation_result["user_type_compliance"],
            float(validation_result["ethical_compliance"])
        ]
        validation_result["overall_score"] = sum(scores) / len(scores)
        
        return validation_result

    def _validate_export_request(self, data: List[Dict], user_type: str) -> Dict[str, Any]:
        """Enhanced export request validation"""
        validation_result = {
            "valid": True,
            "sensitivity_level": DataSensitivityLevel.PUBLIC,
            "context_preservation": {"adequate": True, "issues": []},
            "ethical_approval": True,
            "issues": [],
            "warnings": []
        }
        
        # Check data sensitivity against user type permissions
        sensitivity_level = self._assess_data_sensitivity(data)
        validation_result["sensitivity_level"] = sensitivity_level
        
        template = self.export_templates.get(user_type, {})
        allowed_sensitivities = template.get("sensitivity_allowed", [DataSensitivityLevel.PUBLIC])
        
        if sensitivity_level not in allowed_sensitivities:
            validation_result["valid"] = False
            validation_result["issues"].append(
                f"User type '{user_type}' not permitted to export {sensitivity_level.value} data"
            )
        
        # Enhanced Kenyan context preservation check
        context_preservation = self._check_context_preservation(data, user_type)
        validation_result["context_preservation"] = context_preservation
        
        if not context_preservation["adequate"]:
            validation_result["warnings"].extend(context_preservation["issues"])
        
        # Ethical compliance check
        if not self._check_ethical_compliance(data, user_type):
            validation_result["ethical_approval"] = False
            validation_result["issues"].append("Ethical compliance check failed")
        
        return validation_result

    # Enhanced user-type specific processing methods
    def _process_for_user_type(self, data: List[Dict], user_type: str) -> List[Dict]:
        """Enhanced user-type specific processing"""
        
        processor_map = {
            "journalist": self._process_for_journalist,
            "researcher": self._process_for_researcher,
            "ngo": self._process_for_ngo,
            "developer": self._process_for_developer,
            "government": self._process_for_government
        }
        
        processor = processor_map.get(user_type, lambda x: x)
        return processor(data.copy())

    def _process_for_journalist(self, data: List[Dict]) -> List[Dict]:
        """Enhanced processing for journalistic use"""
        processed = []
        for item in data:
            journalist_item = item.copy()
            
            journalist_item["public_interest_metrics"] = {
                "public_interest_score": self._calculate_public_interest(item),
                "verification_status": self._assess_verification_status(item),
                "ethical_considerations": self._generate_ethical_notes(item),
                "urgency_level": self._assess_urgency(item)
            }
            
            journalist_item["kenyan_context"] = {
                "kenyan_impact": self._assess_kenyan_impact(item),
                "stakeholder_analysis": self._identify_kenyan_stakeholders(item),
                "regional_sensitivity": self._assess_regional_sensitivity(item)
            }
            
            processed.append(journalist_item)
        return processed

    def _process_for_researcher(self, data: List[Dict]) -> List[Dict]:
        """Enhanced processing for academic research"""
        processed = []
        for item in data:
            research_item = item.copy()
            
            research_item["research_metadata"] = {
                "methodological_notes": self._generate_methodology_notes(item),
                "limitations": self._identify_research_limitations(item),
                "replication_instructions": self._generate_replication_guide(item),
                "validity_indicators": self._assess_validity(item)
            }
            
            research_item["kenyan_context"] = {
                "local_methodology_adaptation": self._suggest_local_adaptations(item),
                "cultural_validity": self._assess_cultural_validity(item),
                "local_irb_considerations": self._generate_irb_notes(item)
            }
            
            processed.append(research_item)
        return processed

    # Enhanced export format handlers
    def _export_json(self, data: List[Dict], user_type: str) -> Dict[str, Any]:
        """Enhanced JSON export with comprehensive metadata"""
        export_structure = {
            "metadata": {
                "export_timestamp": datetime.now(timezone.utc).isoformat(),
                "user_type": user_type,
                "kenyan_context_version": "2.0",
                "data_protection_compliance": "DPA_2019",
                "export_config": self.config,
                "quality_indicators": {
                    "kenyan_relevance": self._calculate_overall_kenyan_relevance(data),
                    "item_count": len(data),
                    "context_validation": self.kenyan_context.validate_context(data)
                }
            },
            "export_template": self.export_templates.get(user_type, {}),
            "data": data,
            "kenyan_context_summary": self._generate_kenyan_context_summary(data),
            "additional_resources": self._generate_additional_resources(user_type)
        }
        
        content = json.dumps(export_structure, indent=2, ensure_ascii=False)
        
        return {
            "format": "json",
            "content": content,
            "filename": f"sovereign_export_{user_type}_{datetime.now():%Y%m%d_%H%M%S}.json",
            "size_estimate": len(content),
            "processing_time": 0  # Would be calculated in real implementation
        }

    def _export_csv(self, data: List[Dict], user_type: str) -> Dict[str, Any]:
        """Enhanced CSV export with better flattening"""
        if not data:
            return {
                "format": "csv", 
                "content": "", 
                "filename": f"sovereign_export_{user_type}_{datetime.now():%Y%m%d_%H%M%S}.csv",
                "size_estimate": 0,
                "processing_time": 0
            }
        
        flattened_data = []
        for item in data:
            flat_item = self._flatten_dict_enhanced(item)
            flattened_data.append(flat_item)
        
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
            "size_estimate": len(csv_content),
            "processing_time": 0
        }

    # Enhanced helper methods
    def _flatten_dict_enhanced(self, d: Dict, parent_key: str = '', sep: str = '_') -> Dict:
        """Enhanced dictionary flattening with type preservation hints"""
        items = []
        for k, v in d.items():
            new_key = f"{parent_key}{sep}{k}" if parent_key else k
            
            if isinstance(v, dict):
                items.extend(self._flatten_dict_enhanced(v, new_key, sep=sep).items())
            elif isinstance(v, list):
                # Handle lists by converting to JSON string or indexing
                if len(v) > 0 and isinstance(v[0], dict):
                    items.append((new_key, json.dumps(v)))
                else:
                    items.append((new_key, '|'.join(map(str, v))))
            else:
                items.append((new_key, v))
        return dict(items)

    def _calculate_overall_kenyan_relevance(self, data: List[Dict]) -> float:
        """Enhanced Kenyan relevance calculation"""
        if not data:
            return 0.0
        
        total_relevance = 0.0
        valid_items = 0
        
        for item in data:
            # Use pre-calculated relevance if available
            if 'osint_metadata' in item and 'kenyan_relevance' in item['osint_metadata']:
                total_relevance += item['osint_metadata']['kenyan_relevance']
                valid_items += 1
            else:
                # Calculate relevance based on content analysis
                relevance_score = self._calculate_kenyan_relevance_score(item)
                total_relevance += relevance_score
                valid_items += 1
        
        return total_relevance / valid_items if valid_items > 0 else 0.0

    # New enhanced validation methods
    def _validate_json_export(self, content: str) -> Dict[str, Any]:
        """Validate JSON export format"""
        try:
            json.loads(content)
            return {"valid": True, "issues": []}
        except json.JSONDecodeError as e:
            return {"valid": False, "issues": [f"JSON validation error: {str(e)}"]}

    def _validate_csv_export(self, content: str) -> Dict[str, Any]:
        """Validate CSV export format"""
        try:
            csv.reader(io.StringIO(content))
            return {"valid": True, "issues": []}
        except Exception as e:
            return {"valid": False, "issues": [f"CSV validation error: {str(e)}"]}

    def _validate_html_export(self, content: str) -> Dict[str, Any]:
        """Basic HTML structure validation"""
        if "<html" in content.lower() and "</html>" in content.lower():
            return {"valid": True, "issues": []}
        else:
            return {"valid": False, "issues": ["Invalid HTML structure"]}

    def _assess_user_type_compliance(self, content: str, template: Dict) -> float:
        """Assess compliance with user-type template requirements"""
        required_fields = template.get("required_fields", [])
        if not required_fields:
            return 1.0
        
        content_lower = content.lower()
        matches = sum(1 for field in required_fields if field.lower() in content_lower)
        return matches / len(required_fields)

    def _calculate_compression_ratio(self, content: str) -> float:
        """Calculate potential compression ratio"""
        if not content:
            return 1.0
        return len(content.encode('utf-8')) / len(content)

    def _generate_overall_quality_report(self, batch_results: Dict) -> Dict[str, Any]:
        """Generate comprehensive quality report for batch export"""
        quality_scores = []
        total_exports = 0
        successful_exports = 0
        
        for user_type, formats in batch_results["exports"].items():
            for fmt, result in formats.items():
                total_exports += 1
                if result["status"] == "success":
                    successful_exports += 1
                    quality_scores.append(result["quality_score"])
        
        avg_quality = sum(quality_scores) / len(quality_scores) if quality_scores else 0.0
        
        return {
            "overall_quality_score": avg_quality,
            "success_rate": successful_exports / total_exports if total_exports > 0 else 0.0,
            "total_exports": total_exports,
            "successful_exports": successful_exports,
            "performance_metrics": {
                "average_quality": avg_quality,
                "quality_std_dev": self._calculate_std_dev(quality_scores) if quality_scores else 0.0
            }
        }

    def _write_export_to_file(self, export_result: Dict, output_dir: Path) -> Path:
        """Write export content to file"""
        output_dir.mkdir(parents=True, exist_ok=True)
        file_path = output_dir / export_result["filename"]
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(export_result["content"])
        
        return file_path

    # Missing method implementations with enhanced functionality
    def _calculate_std_dev(self, numbers: List[float]) -> float:
        """Calculate standard deviation"""
        if len(numbers) < 2:
            return 0.0
        mean = sum(numbers) / len(numbers)
        variance = sum((x - mean) ** 2 for x in numbers) / len(numbers)
        return variance ** 0.5

    def _check_geographic_consistency(self, item: Dict) -> bool:
        """Check geographic consistency of data"""
        content = str(item).lower()
        regions = ['nairobi', 'mombasa', 'kisumu', 'nakuru', 'coast', 'rift valley']
        mentions = [region for region in regions if region in content]
        return len(mentions) <= 2  # More than 2 regions might indicate inconsistency

    def _assess_corroboration(self, item: Dict) -> float:
        """Assess level of corroboration for the data"""
        sources = item.get('sources', [])
        if len(sources) >= 3:
            return 0.9
        elif len(sources) == 2:
            return 0.7
        elif len(sources) == 1:
            return 0.4
        else:
            return 0.1

    def _assess_urgency(self, item: Dict) -> str:
        """Assess urgency level for journalistic content"""
        urgent_indicators = ['breaking', 'urgent', 'crisis', 'emergency', 'alert']
        content = str(item).lower()
        if any(indicator in content for indicator in urgent_indicators):
            return "high"
        return "medium"

    def _assess_regional_sensitivity(self, item: Dict) -> List[str]:
        """Assess regional sensitivity for Kenyan context"""
        sensitive_regions = ['north eastern', 'coast', 'border']
        content = str(item).lower()
        return [region for region in sensitive_regions if region in content]

    def _assess_validity(self, item: Dict) -> Dict[str, float]:
        """Assess research validity indicators"""
        return {
            "internal_validity": 0.8,
            "external_validity": 0.6,
            "construct_validity": 0.7
        }

    def _generate_irb_notes(self, item: Dict) -> List[str]:
        """Generate IRB considerations for research"""
        return ["Ensure local IRB approval", "Consider cultural sensitivity"]

    def _check_ethical_compliance(self, data: List[Dict], user_type: str) -> bool:
        """Check ethical compliance for export"""
        # Basic ethical checks - would be expanded in real implementation
        sensitive_keywords = ['personal', 'private', 'confidential']
        content = str(data).lower()
        
        if any(keyword in content for keyword in sensitive_keywords):
            return user_type in ['researcher', 'government']  # More strict checks
        
        return True

    # Original method stubs with enhanced implementations
    def _assess_data_sensitivity(self, data: List[Dict]) -> DataSensitivityLevel:
        """Enhanced data sensitivity assessment"""
        if not data:
            return DataSensitivityLevel.PUBLIC
        
        content = str(data).lower()
        sensitive_indicators = {
            DataSensitivityLevel.RESTRICTED: ['classified', 'top secret', 'confidential'],
            DataSensitivityLevel.SENSITIVE_PUBLIC_INTEREST: ['whistleblower', 'corruption', 'scandal'],
            DataSensitivityLevel.SENSITIVE_RESEARCH: ['personal data', 'medical', 'health'],
            DataSensitivityLevel.SENSITIVE_COMMUNITY: ['community', 'ethnic', 'tribal'],
            DataSensitivityLevel.TECHNICAL: ['api', 'database', 'infrastructure']
        }
        
        for level, indicators in sensitive_indicators.items():
            if any(indicator in content for indicator in indicators):
                return level
        
        return DataSensitivityLevel.PUBLIC

    def _check_context_preservation(self, data: List[Dict], user_type: str) -> Dict[str, Any]:
        """Enhanced context preservation check"""
        validation = self.kenyan_context.validate_context(data)
        
        return {
            "adequate": validation["has_kenyan_context"],
            "issues": validation["issues"],
            "recommendations": validation["recommendations"],
            "regional_mentions": validation["regional_mentions"]
        }

    # Keep the original helper methods but enhance where needed
    def _calculate_public_interest(self, item: Dict) -> float:
        """Enhanced public interest calculation"""
        content = str(item).lower()
        interest_indicators = ['corruption', 'development', 'health', 'education', 'infrastructure']
        matches = sum(1 for indicator in interest_indicators if indicator in content)
        return min(matches / len(interest_indicators), 1.0)

    def _assess_kenyan_impact(self, item: Dict) -> List[str]:
        """Enhanced Kenyan impact assessment"""
        content = str(item).lower()
        impacts = []
        
        impact_mapping = {
            'nairobi': "Nairobi residents",
            'rural': "Rural communities", 
            'county': "County residents",
            'youth': "Youth population",
            'women': "Women and girls",
            'farmers': "Agricultural sector",
            'business': "Business community"
        }
        
        for indicator, impact in impact_mapping.items():
            if indicator in content:
                impacts.append(impact)
        
        return impacts if impacts else ["General Kenyan public"]

    def _generate_kenyan_context_summary(self, data: List[Dict]) -> str:
        """Enhanced Kenyan context summary"""
        if not data:
            return "No data available for context analysis"
        
        regional_mentions = {}
        topic_mentions = {}
        impact_levels = []
        
        for item in data:
            content = str(item).lower()
            
            # Regional analysis
            for region in self.kenyan_context.KENYAN_REGIONS.keys():
                if region in content:
                    regional_mentions[region] = regional_mentions.get(region, 0) + 1
            
            # Topic analysis
            topics = ["development", "politics", "economy", "health", "education", "security"]
            for topic in topics:
                if topic in content:
                    topic_mentions[topic] = topic_mentions.get(topic, 0) + 1
            
            # Impact assessment
            impacts = self._assess_kenyan_impact(item)
            impact_levels.extend(impacts)
        
        summary_parts = []
        
        if regional_mentions:
            top_regions = sorted(regional_mentions.items(), key=lambda x: x[1], reverse=True)[:3]
            summary_parts.append(f"Regional focus: {', '.join([r[0] for r in top_regions])}")
        
        if topic_mentions:
            top_topics = sorted(topic_mentions.items(), key=lambda x: x[1], reverse=True)[:3]
            summary_parts.append(f"Key topics: {', '.join([t[0] for t in top_topics])}")
        
        if impact_levels:
            from collections import Counter
            common_impacts = Counter(impact_levels).most_common(3)
            summary_parts.append(f"Primary impacts: {', '.join([i[0] for i in common_impacts])}")
        
        return f"Analysis of {len(data)} items: {'; '.join(summary_parts)}"

    # Enhanced OSINT context methods
    def _calculate_kenyan_relevance_score(self, item: Dict) -> float:
        """Enhanced Kenyan relevance scoring"""
        content = str(item).lower()
        indicators = {
            'nairobi': 0.3, 'mombasa': 0.2, 'kisumu': 0.15, 'nakuru': 0.1, 'eldoret': 0.05,
            'kenya': 0.4, 'county': 0.2, 'kes': 0.1, 'kwanza': 0.05, 'uhuru': 0.1, 'ruto': 0.1
        }
        
        score = 0.0
        for indicator, weight in indicators.items():
            if indicator in content:
                score += weight
        
        return min(score, 1.0)

    def _check_cross_references(self, item: Dict) -> bool:
        """Check if data has been cross-referenced"""
        sources = item.get('sources', [])
        return len(sources) >= 2

    def _assess_temporal_relevance(self, item: Dict) -> float:
        """Assess temporal relevance of data"""
        timestamp = item.get('timestamp')
        if not timestamp:
            return 0.5
        
        try:
            if isinstance(timestamp, str):
                from dateutil.parser import parse
                item_time = parse(timestamp)
            else:
                item_time = timestamp
            
            time_diff = datetime.now(timezone.utc) - item_time
            days_diff = time_diff.days
            
            if days_diff <= 1:
                return 1.0
            elif days_diff <= 7:
                return 0.8
            elif days_diff <= 30:
                return 0.6
            elif days_diff <= 365:
                return 0.4
            else:
                return 0.2
        except:
            return 0.5

    def _assess_source_reliability(self, source_type: str) -> float:
        """Enhanced source reliability assessment"""
        reliability_scores = {
            'official_gov': 0.9,
            'verified_news': 0.8,
            'academic': 0.85,
            'ngo_report': 0.7,
            'social_media': 0.4,
            'user_generated': 0.3,
            'unknown': 0.5
        }
        return reliability_scores.get(source_type, 0.5)

    # Stub methods for other user types (would be implemented similarly)
    def _process_for_ngo(self, data: List[Dict]) -> List[Dict]:
        """Process data for NGO use"""
        processed = []
        for item in data:
            ngo_item = item.copy()
            ngo_item["community_impact"] = self._assess_community_impact(item)
            ngo_item["stakeholder_analysis"] = self._identify_stakeholders(item)
            processed.append(ngo_item)
        return processed

    def _process_for_developer(self, data: List[Dict]) -> List[Dict]:
        """Process data for developer use"""
        processed = []
        for item in data:
            dev_item = item.copy()
            dev_item["technical_metadata"] = {
                "data_quality": self._assess_data_quality(item),
                "api_compatibility": self._check_api_compatibility(item)
            }
            processed.append(dev_item)
        return processed

    def _process_for_government(self, data: List[Dict]) -> List[Dict]:
        """Process data for government use"""
        processed = []
        for item in data:
            gov_item = item.copy()
            gov_item["official_metadata"] = {
                "classification_level": self._determine_classification(item),
                "interagency_relevance": self._assess_interagency_relevance(item)
            }
            processed.append(gov_item)
        return processed

    # Stub implementations for the new methods
    def _assess_verification_status(self, item: Dict) -> str:
        """Assess verification status for journalistic content"""
        return "partially_verified"  # Simplified implementation

    def _generate_ethical_notes(self, item: Dict) -> List[str]:
        """Generate ethical considerations for journalism"""
        return ["Verify sources", "Consider privacy implications"]

    def _identify_kenyan_stakeholders(self, item: Dict) -> List[str]:
        """Identify Kenyan stakeholders mentioned in content"""
        content = str(item).lower()
        stakeholders = []
        
        stakeholder_indicators = {
            'government': ['government', 'ministry', 'county'],
            'civil_society': ['ngo', 'community', 'organization'],
            'private_sector': ['company', 'business', 'enterprise'],
            'citizens': ['resident', 'citizen', 'public']
        }
        
        for stakeholder_type, indicators in stakeholder_indicators.items():
            if any(indicator in content for indicator in indicators):
                stakeholders.append(stakeholder_type)
        
        return stakeholders if stakeholders else ["General public"]

    def _generate_methodology_notes(self, item: Dict) -> str:
        """Generate methodology notes for research"""
        return "Standard OSINT collection methodology applied"

    def _identify_research_limitations(self, item: Dict) -> List[str]:
        """Identify research limitations"""
        return ["Sample size limitations", "Potential source bias"]

    def _generate_replication_guide(self, item: Dict) -> str:
        """Generate replication guide for research"""
        return "Follow standard OSINT protocols with local context adaptation"

    def _suggest_local_adaptations(self, item: Dict) -> List[str]:
        """Suggest local methodology adaptations for Kenya"""
        return ["Consider local language nuances", "Account for regional variations"]

    def _assess_cultural_validity(self, item: Dict) -> float:
        """Assess cultural validity for Kenyan context"""
        return 0.8  # Simplified implementation

    def _assess_community_impact(self, item: Dict) -> str:
        """Assess community impact for NGO use"""
        return "medium"  # Simplified implementation

    def _identify_stakeholders(self, item: Dict) -> List[str]:
        """Identify stakeholders for NGO analysis"""
        return ["Local communities", "Government agencies", "Development partners"]

    def _assess_data_quality(self, item: Dict) -> Dict[str, float]:
        """Assess data quality for developer use"""
        return {"completeness": 0.8, "accuracy": 0.7, "timeliness": 0.9}

    def _check_api_compatibility(self, item: Dict) -> bool:
        """Check API compatibility for developer use"""
        return True  # Simplified implementation

    def _determine_classification(self, item: Dict) -> str:
        """Determine classification level for government use"""
        return "OFFICIAL"  # Simplified implementation

    def _assess_interagency_relevance(self, item: Dict) -> List[str]:
        """Assess interagency relevance for government use"""
        return ["Ministry of ICT", "Data Protection Commission"]

    def _generate_additional_resources(self, user_type: str) -> List[str]:
        """Generate additional resources based on user type"""
        resources = {
            "journalist": ["Kenya Media Council Guidelines", "OSINT Verification Handbook"],
            "researcher": ["Kenya Data Protection Act", "Research Ethics Guidelines"],
            "ngo": ["Community Engagement Protocols", "Stakeholder Mapping Guide"],
            "developer": ["API Documentation", "Data Schema Specifications"],
            "government": ["Official Classification Guide", "Interagency Protocols"]
        }
        return resources.get(user_type, ["General OSINT Resources"])

    def _export_pdf(self, data: List[Dict], user_type: str) -> Dict[str, Any]:
        """Enhanced PDF export stub"""
        # In a real implementation, this would use a PDF generation library
        pdf_content = f"PDF Export for {user_type}\n\n{json.dumps(data, indent=2)}"
        
        return {
            "format": "pdf",
            "content": pdf_content,
            "filename": f"sovereign_export_{user_type}_{datetime.now():%Y%m%d_%H%M%S}.pdf",
            "size_estimate": len(pdf_content),
            "processing_time": 0
        }

    def _export_html(self, data: List[Dict], user_type: str) -> Dict[str, Any]:
        """Enhanced HTML export stub"""
        html_content = f"""
        <html>
        <head><title>Sovereign Export for {user_type}</title></head>
        <body>
            <h1>OSINT Data Export</h1>
            <p>User Type: {user_type}</p>
            <pre>{json.dumps(data, indent=2)}</pre>
        </body>
        </html>
        """
        
        return {
            "format": "html",
            "content": html_content,
            "filename": f"sovereign_export_{user_type}_{datetime.now():%Y%m%d_%H%M%S}.html",
            "size_estimate": len(html_content),
            "processing_time": 0
        }


# Example usage and testing
if __name__ == "__main__":
    # Test the enhanced exporter
    sample_data = [
        {
            "title": "Nairobi Development Project Analysis",
            "content": "Analysis of infrastructure development in Nairobi County affecting local communities",
            "sources": ["official_report", "local_news"],
            "timestamp": "2024-01-15T10:30:00Z"
        },
        {
            "title": "Mombasa Port Expansion Impact", 
            "content": "Study on economic impact of port expansion on Mombasa residents and businesses",
            "sources": ["academic_study", "government_data"],
            "timestamp": "2024-01-10T14:45:00Z"
        }
    ]
    
    exporter = SovereignExporter({
        "enable_anonymization": True,
        "anonymization_level": "medium",
        "validate_context": True
    })
    
    # Test batch export
    results = exporter.batch_export(
        data=sample_data,
        formats=["json", "csv"],
        user_types=["journalist", "researcher"],
        output_dir=Path("./exports")
    )
    
    print("Batch export completed successfully!")
    print(f"Generated {len(results['files_written'])} files")
    print(f"Overall quality score: {results['quality_report']['overall_quality_score']:.2f}")