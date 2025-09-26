#!/usr/bin/env python3
"""
Configuration Manager for the Intelligent Feedback Analysis System
Handles classification thresholds, priority rules, and agent settings
"""

import json
import os
from typing import Dict, Any, Optional
from dataclasses import dataclass, asdict
from datetime import datetime

@dataclass
class ClassificationThresholds:
    """Configuration for classification confidence thresholds"""
    bug_threshold: float = 0.7
    feature_threshold: float = 0.6
    praise_threshold: float = 0.6
    complaint_threshold: float = 0.6
    spam_threshold: float = 0.8
    minimum_confidence: float = 0.5
    
@dataclass
class PriorityWeights:
    """Configuration for priority assignment weights"""
    bug_severity_weight: float = 0.4
    user_impact_weight: float = 0.3
    technical_complexity_weight: float = 0.2
    business_priority_weight: float = 0.1
    
    # Category-specific priority mappings
    bug_priority_mapping: Dict[str, str] = None
    feature_priority_mapping: Dict[str, str] = None
    
    def __post_init__(self):
        if self.bug_priority_mapping is None:
            self.bug_priority_mapping = {
                "Critical": "Critical",
                "High": "High", 
                "Medium": "Medium",
                "Low": "Low"
            }
        
        if self.feature_priority_mapping is None:
            self.feature_priority_mapping = {
                "High Impact": "High",
                "Medium Impact": "Medium",
                "Low Impact": "Low"
            }

@dataclass
class QualityThresholds:
    """Configuration for quality review thresholds"""
    minimum_quality_score: float = 70.0
    auto_approve_threshold: float = 90.0
    manual_review_threshold: float = 60.0
    reject_threshold: float = 40.0

@dataclass
class AgentSettings:
    """Configuration for individual agent behaviors"""
    enable_bug_analysis: bool = True
    enable_feature_extraction: bool = True
    enable_quality_review: bool = True
    enable_technical_extraction: bool = True
    
    # Agent-specific timeouts (in seconds)
    classification_timeout: int = 30
    bug_analysis_timeout: int = 45
    feature_extraction_timeout: int = 30
    quality_review_timeout: int = 20

@dataclass  
class ProcessingRules:
    """Configuration for processing behavior rules"""
    skip_low_confidence_items: bool = False
    auto_categorize_spam: bool = True
    require_manual_review_for_critical: bool = True
    batch_size: int = 10
    max_retries: int = 3

@dataclass
class SystemConfiguration:
    """Complete system configuration"""
    classification_thresholds: ClassificationThresholds
    priority_weights: PriorityWeights 
    quality_thresholds: QualityThresholds
    agent_settings: AgentSettings
    processing_rules: ProcessingRules
    
    # Metadata
    version: str = "1.0.0"
    last_updated: str = ""
    created_by: str = "system"
    
    def __post_init__(self):
        if not self.last_updated:
            self.last_updated = datetime.now().isoformat()

class ConfigurationManager:
    """Manages system configuration with persistence and validation"""
    
    def __init__(self, config_file: str = "system_config.json"):
        self.config_file = config_file
        self.config: Optional[SystemConfiguration] = None
        self.load_configuration()
    
    def load_configuration(self) -> SystemConfiguration:
        """Load configuration from file or create defaults"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config_dict = json.load(f)
                    
                # Convert dictionary back to dataclass
                self.config = SystemConfiguration(
                    classification_thresholds=ClassificationThresholds(**config_dict.get('classification_thresholds', {})),
                    priority_weights=PriorityWeights(**config_dict.get('priority_weights', {})),
                    quality_thresholds=QualityThresholds(**config_dict.get('quality_thresholds', {})),
                    agent_settings=AgentSettings(**config_dict.get('agent_settings', {})),
                    processing_rules=ProcessingRules(**config_dict.get('processing_rules', {})),
                    version=config_dict.get('version', '1.0.0'),
                    last_updated=config_dict.get('last_updated', ''),
                    created_by=config_dict.get('created_by', 'system')
                )
                
                print(f"✅ Loaded configuration from {self.config_file}")
                
            except Exception as e:
                print(f"⚠️ Error loading config file: {e}")
                print("🔧 Creating default configuration...")
                self.config = self.create_default_configuration()
                self.save_configuration()
        else:
            print(f"📝 Configuration file {self.config_file} not found")
            print("🔧 Creating default configuration...")
            self.config = self.create_default_configuration()
            self.save_configuration()
            
        return self.config
    
    def create_default_configuration(self) -> SystemConfiguration:
        """Create default system configuration"""
        return SystemConfiguration(
            classification_thresholds=ClassificationThresholds(),
            priority_weights=PriorityWeights(),
            quality_thresholds=QualityThresholds(),
            agent_settings=AgentSettings(),
            processing_rules=ProcessingRules(),
            created_by="system_default"
        )
    
    def save_configuration(self) -> bool:
        """Save current configuration to file"""
        try:
            # Update last modified timestamp
            self.config.last_updated = datetime.now().isoformat()
            
            # Convert to dictionary
            config_dict = asdict(self.config)
            
            # Save to file with pretty formatting
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config_dict, f, indent=2, ensure_ascii=False)
            
            print(f"✅ Configuration saved to {self.config_file}")
            return True
            
        except Exception as e:
            print(f"❌ Error saving configuration: {e}")
            return False
    
    def update_classification_thresholds(self, **kwargs) -> bool:
        """Update classification threshold values"""
        try:
            for key, value in kwargs.items():
                if hasattr(self.config.classification_thresholds, key):
                    setattr(self.config.classification_thresholds, key, float(value))
                    print(f"🔧 Updated {key} to {value}")
            
            return self.save_configuration()
        except Exception as e:
            print(f"❌ Error updating classification thresholds: {e}")
            return False
    
    def update_priority_weights(self, **kwargs) -> bool:
        """Update priority weight values"""
        try:
            for key, value in kwargs.items():
                if hasattr(self.config.priority_weights, key) and not key.endswith('_mapping'):
                    setattr(self.config.priority_weights, key, float(value))
                    print(f"🔧 Updated {key} to {value}")
            
            return self.save_configuration()
        except Exception as e:
            print(f"❌ Error updating priority weights: {e}")
            return False
    
    def update_quality_thresholds(self, **kwargs) -> bool:
        """Update quality threshold values"""
        try:
            for key, value in kwargs.items():
                if hasattr(self.config.quality_thresholds, key):
                    setattr(self.config.quality_thresholds, key, float(value))
                    print(f"🔧 Updated {key} to {value}")
            
            return self.save_configuration()
        except Exception as e:
            print(f"❌ Error updating quality thresholds: {e}")
            return False
    
    def update_agent_settings(self, **kwargs) -> bool:
        """Update agent setting values"""
        try:
            for key, value in kwargs.items():
                if hasattr(self.config.agent_settings, key):
                    if key.endswith('_timeout'):
                        setattr(self.config.agent_settings, key, int(value))
                    else:
                        setattr(self.config.agent_settings, key, bool(value))
                    print(f"🔧 Updated {key} to {value}")
            
            return self.save_configuration()
        except Exception as e:
            print(f"❌ Error updating agent settings: {e}")
            return False
    
    def update_processing_rules(self, **kwargs) -> bool:
        """Update processing rule values"""
        try:
            for key, value in kwargs.items():
                if hasattr(self.config.processing_rules, key):
                    if key in ['batch_size', 'max_retries']:
                        setattr(self.config.processing_rules, key, int(value))
                    else:
                        setattr(self.config.processing_rules, key, bool(value))
                    print(f"🔧 Updated {key} to {value}")
            
            return self.save_configuration()
        except Exception as e:
            print(f"❌ Error updating processing rules: {e}")
            return False
    
    def get_classification_threshold(self, category: str) -> float:
        """Get classification threshold for a specific category"""
        threshold_map = {
            'Bug': self.config.classification_thresholds.bug_threshold,
            'Feature Request': self.config.classification_thresholds.feature_threshold,
            'Praise': self.config.classification_thresholds.praise_threshold,
            'Complaint': self.config.classification_thresholds.complaint_threshold,
            'Spam': self.config.classification_thresholds.spam_threshold
        }
        
        return threshold_map.get(category, self.config.classification_thresholds.minimum_confidence)
    
    def reset_to_defaults(self) -> bool:
        """Reset configuration to default values"""
        try:
            self.config = self.create_default_configuration()
            return self.save_configuration()
        except Exception as e:
            print(f"❌ Error resetting to defaults: {e}")
            return False
    
    def export_configuration(self, export_file: str) -> bool:
        """Export configuration to a different file"""
        try:
            config_dict = asdict(self.config)
            with open(export_file, 'w', encoding='utf-8') as f:
                json.dump(config_dict, f, indent=2, ensure_ascii=False)
            
            print(f"✅ Configuration exported to {export_file}")
            return True
        except Exception as e:
            print(f"❌ Error exporting configuration: {e}")
            return False
    
    def import_configuration(self, import_file: str) -> bool:
        """Import configuration from a file"""
        if not os.path.exists(import_file):
            print(f"❌ Import file {import_file} not found")
            return False
        
        try:
            # Backup current config
            self.export_configuration(f"{self.config_file}.backup")
            
            # Load new config
            backup_file = self.config_file
            self.config_file = import_file
            self.load_configuration()
            self.config_file = backup_file
            
            # Save imported config as current
            return self.save_configuration()
            
        except Exception as e:
            print(f"❌ Error importing configuration: {e}")
            return False
    
    def validate_configuration(self) -> Dict[str, Any]:
        """Validate current configuration and return any issues"""
        issues = []
        warnings = []
        
        # Check classification thresholds
        if not (0.0 <= self.config.classification_thresholds.minimum_confidence <= 1.0):
            issues.append("Minimum confidence must be between 0.0 and 1.0")
        
        for attr in ['bug_threshold', 'feature_threshold', 'praise_threshold', 'complaint_threshold', 'spam_threshold']:
            value = getattr(self.config.classification_thresholds, attr)
            if not (0.0 <= value <= 1.0):
                issues.append(f"{attr} must be between 0.0 and 1.0")
        
        # Check priority weights sum to reasonable value
        weights_sum = (
            self.config.priority_weights.bug_severity_weight +
            self.config.priority_weights.user_impact_weight +
            self.config.priority_weights.technical_complexity_weight +
            self.config.priority_weights.business_priority_weight
        )
        
        if abs(weights_sum - 1.0) > 0.1:
            warnings.append(f"Priority weights sum to {weights_sum:.2f}, consider normalizing to 1.0")
        
        # Check quality thresholds are in logical order
        qt = self.config.quality_thresholds
        if qt.reject_threshold >= qt.manual_review_threshold:
            issues.append("Reject threshold must be lower than manual review threshold")
        
        if qt.manual_review_threshold >= qt.auto_approve_threshold:
            issues.append("Manual review threshold must be lower than auto-approve threshold")
        
        return {
            'valid': len(issues) == 0,
            'issues': issues,
            'warnings': warnings
        }

# Global configuration manager instance
_config_manager: Optional[ConfigurationManager] = None

def get_config_manager(config_file: str = "system_config.json") -> ConfigurationManager:
    """Get the global configuration manager instance"""
    global _config_manager
    if _config_manager is None:
        _config_manager = ConfigurationManager(config_file)
    return _config_manager

def get_current_config() -> SystemConfiguration:
    """Get the current system configuration"""
    return get_config_manager().config