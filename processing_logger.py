#!/usr/bin/env python3
"""
Processing Logger Module
Logs detailed processing history and agent decisions for transparency and analysis
"""

import csv
import json
import os
from datetime import datetime
from typing import Dict, List, Any, Optional

class ProcessingLogger:
    """Logs all agent decisions and processing steps to CSV"""
    
    def __init__(self, log_file: str = "processing_log.csv"):
        self.log_file = log_file
        self.log_entries: List[Dict[str, Any]] = []
        self._initialize_log_file()
    
    def _initialize_log_file(self):
        """Initialize the CSV file with headers if it doesn't exist"""
        if not os.path.exists(self.log_file):
            headers = [
                'timestamp',
                'session_id',
                'source_id',
                'source_type', 
                'agent_name',
                'action_type',
                'decision_point',
                'input_data',
                'output_data',
                'confidence_score',
                'reasoning',
                'processing_time_ms',
                'success_status',
                'error_message',
                'metadata'
            ]
            
            with open(self.log_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(headers)
    
    def log_agent_decision(self, 
                          session_id: str,
                          source_id: str, 
                          source_type: str,
                          agent_name: str,
                          action_type: str,
                          decision_point: str,
                          input_data: Any,
                          output_data: Any,
                          confidence_score: Optional[float] = None,
                          reasoning: str = "",
                          processing_time_ms: Optional[float] = None,
                          success_status: bool = True,
                          error_message: str = "",
                          metadata: Dict[str, Any] = None):
        """Log a single agent decision"""
        
        entry = {
            'timestamp': datetime.now().isoformat(),
            'session_id': session_id,
            'source_id': source_id,
            'source_type': source_type,
            'agent_name': agent_name,
            'action_type': action_type,
            'decision_point': decision_point,
            'input_data': json.dumps(input_data) if isinstance(input_data, (dict, list)) else str(input_data)[:500],
            'output_data': json.dumps(output_data) if isinstance(output_data, (dict, list)) else str(output_data)[:500], 
            'confidence_score': confidence_score or 0.0,
            'reasoning': reasoning[:1000],  # Limit reasoning text
            'processing_time_ms': processing_time_ms or 0.0,
            'success_status': success_status,
            'error_message': error_message[:500],
            'metadata': json.dumps(metadata or {})
        }
        
        self.log_entries.append(entry)
        self._write_entry_to_file(entry)
    
    def _write_entry_to_file(self, entry: Dict[str, Any]):
        """Write a single entry to the CSV file"""
        try:
            with open(self.log_file, 'a', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=entry.keys())
                writer.writerow(entry)
        except Exception as e:
            print(f"Warning: Failed to write to processing log: {e}")
    
    def log_classification_decision(self, session_id: str, source_id: str, source_type: str, 
                                  text: str, category: str, confidence: float, 
                                  processing_time: float = 0.0):
        """Log feedback classification decision"""
        self.log_agent_decision(
            session_id=session_id,
            source_id=source_id,
            source_type=source_type,
            agent_name="Feedback Classifier Agent",
            action_type="classification",
            decision_point="feedback_categorization",
            input_data=text[:200],
            output_data={"category": category, "confidence": confidence},
            confidence_score=confidence,
            reasoning=f"Classified feedback as '{category}' based on text patterns and keywords",
            processing_time_ms=processing_time,
            metadata={"text_length": len(text)}
        )
    
    def log_bug_analysis_decision(self, session_id: str, source_id: str, source_type: str,
                                text: str, is_bug: bool, severity: str = "", 
                                priority: str = "", reproduction_steps: str = "",
                                processing_time: float = 0.0):
        """Log bug analysis decision"""
        decision = "analyze_bug" if is_bug else "skip_non_bug"
        reasoning = f"Analyzed as {'bug report' if is_bug else 'non-bug item'}"
        if is_bug:
            reasoning += f" with severity: {severity}, priority: {priority}"
        
        output_data = {
            "is_bug": is_bug,
            "severity": severity,
            "priority": priority, 
            "has_reproduction_steps": bool(reproduction_steps)
        }
        
        self.log_agent_decision(
            session_id=session_id,
            source_id=source_id,
            source_type=source_type,
            agent_name="Bug Analysis Agent",
            action_type="bug_analysis",
            decision_point=decision,
            input_data=text[:200],
            output_data=output_data,
            reasoning=reasoning,
            processing_time_ms=processing_time,
            metadata={"reproduction_steps_available": bool(reproduction_steps)}
        )
    
    def log_feature_analysis_decision(self, session_id: str, source_id: str, source_type: str,
                                    text: str, is_feature: bool, impact: str = "",
                                    complexity: str = "", user_benefit: str = "",
                                    processing_time: float = 0.0):
        """Log feature analysis decision"""
        decision = "analyze_feature" if is_feature else "skip_non_feature"
        reasoning = f"Analyzed as {'feature request' if is_feature else 'non-feature item'}"
        if is_feature:
            reasoning += f" with impact: {impact}, complexity: {complexity}"
        
        output_data = {
            "is_feature": is_feature,
            "impact": impact,
            "complexity": complexity,
            "user_benefit": user_benefit
        }
        
        self.log_agent_decision(
            session_id=session_id,
            source_id=source_id,
            source_type=source_type,
            agent_name="Feature Extractor Agent",
            action_type="feature_analysis", 
            decision_point=decision,
            input_data=text[:200],
            output_data=output_data,
            reasoning=reasoning,
            processing_time_ms=processing_time
        )
    
    def log_priority_decision(self, session_id: str, source_id: str, source_type: str,
                            text: str, category: str, priority: str,
                            processing_time: float = 0.0):
        """Log priority assignment decision"""
        self.log_agent_decision(
            session_id=session_id,
            source_id=source_id, 
            source_type=source_type,
            agent_name="Priority Analyzer Agent",
            action_type="priority_assignment",
            decision_point="determine_priority",
            input_data={"text": text[:200], "category": category},
            output_data={"priority": priority},
            reasoning=f"Assigned '{priority}' priority based on category '{category}' and content analysis",
            processing_time_ms=processing_time,
            metadata={"category": category}
        )
    
    def log_technical_extraction_decision(self, session_id: str, source_id: str, source_type: str,
                                        text: str, technical_details: str,
                                        processing_time: float = 0.0):
        """Log technical details extraction decision"""
        has_technical_info = technical_details != "No technical details found"
        
        self.log_agent_decision(
            session_id=session_id,
            source_id=source_id,
            source_type=source_type,
            agent_name="Technical Details Agent",
            action_type="technical_extraction",
            decision_point="extract_technical_info",
            input_data=text[:200],
            output_data={"technical_details": technical_details},
            reasoning=f"{'Found' if has_technical_info else 'No'} technical details in feedback text",
            processing_time_ms=processing_time,
            metadata={"has_technical_info": has_technical_info}
        )
    
    def log_ticket_creation_decision(self, session_id: str, source_id: str, source_type: str,
                                   title: str, category: str, priority: str,
                                   processing_time: float = 0.0):
        """Log ticket creation decision"""
        self.log_agent_decision(
            session_id=session_id,
            source_id=source_id,
            source_type=source_type,
            agent_name="Ticket Creator Agent",
            action_type="ticket_creation",
            decision_point="generate_ticket",
            input_data={"category": category, "priority": priority},
            output_data={"title": title, "ticket_id": f"TICKET-{source_id}"},
            reasoning=f"Created '{category}' ticket with '{priority}' priority",
            processing_time_ms=processing_time,
            metadata={"category": category, "priority": priority}
        )
    
    def log_quality_review_decision(self, session_id: str, source_id: str, source_type: str,
                                  quality_score: float, status: str, issues: List[str],
                                  processing_time: float = 0.0):
        """Log quality review decision"""
        self.log_agent_decision(
            session_id=session_id,
            source_id=source_id,
            source_type=source_type,
            agent_name="Quality Reviewer Agent",
            action_type="quality_review",
            decision_point="assess_quality",
            input_data=f"ticket-{source_id}",
            output_data={"quality_score": quality_score, "status": status, "issues_count": len(issues)},
            confidence_score=quality_score,
            reasoning=f"Quality assessment: {status} with score {quality_score}% ({len(issues)} issues found)",
            processing_time_ms=processing_time,
            metadata={"issues": issues, "status": status}
        )
    
    def log_session_summary(self, session_id: str, total_items: int, 
                          processing_time: float, success_count: int):
        """Log overall session summary using simple format to maintain CSV compatibility"""
        # Use simple logging to maintain CSV format consistency
        import pandas as pd
        from datetime import datetime
        
        # Create a simple summary entry that matches the 6-field format
        summary_data = {
            'source_id': f'SESSION_{session_id[:8]}',  # Truncate session ID 
            'source_type': 'session_summary',
            'category': 'Summary',
            'confidence': round(100.0 * success_count / total_items if total_items > 0 else 0.0, 2),
            'processing_time': datetime.now().isoformat(),
            'status': f'Completed {success_count}/{total_items}'
        }
        
        # Append to CSV file directly to maintain format consistency
        try:
            df = pd.DataFrame([summary_data])
            df.to_csv(self.log_file, mode='a', header=False, index=False)
        except Exception as e:
            print(f"Warning: Could not log session summary: {e}")
            # If CSV append fails, skip session summary to avoid format issues
    
    def get_session_stats(self, session_id: str) -> Dict[str, Any]:
        """Get statistics for a specific session"""
        session_entries = [entry for entry in self.log_entries if entry['session_id'] == session_id]
        
        if not session_entries:
            return {}
        
        total_time = sum(float(entry.get('processing_time_ms', 0)) for entry in session_entries)
        successful_operations = sum(1 for entry in session_entries if entry.get('success_status', False))
        
        agent_stats = {}
        for entry in session_entries:
            agent = entry['agent_name']
            if agent not in agent_stats:
                agent_stats[agent] = {'count': 0, 'avg_confidence': 0, 'total_time': 0}
            
            agent_stats[agent]['count'] += 1
            agent_stats[agent]['avg_confidence'] += float(entry.get('confidence_score', 0))
            agent_stats[agent]['total_time'] += float(entry.get('processing_time_ms', 0))
        
        # Calculate averages
        for agent in agent_stats:
            if agent_stats[agent]['count'] > 0:
                agent_stats[agent]['avg_confidence'] /= agent_stats[agent]['count']
        
        return {
            'session_id': session_id,
            'total_operations': len(session_entries),
            'successful_operations': successful_operations,
            'success_rate': successful_operations / len(session_entries) if session_entries else 0,
            'total_processing_time_ms': total_time,
            'agent_statistics': agent_stats,
            'timestamp': session_entries[0]['timestamp'] if session_entries else None
        }

# Global processing logger instance
_processing_logger: Optional[ProcessingLogger] = None

def get_processing_logger(log_file: str = "processing_log.csv") -> ProcessingLogger:
    """Get the global processing logger instance"""
    global _processing_logger
    if _processing_logger is None:
        _processing_logger = ProcessingLogger(log_file)
    return _processing_logger

def reset_processing_logger(log_file: str = "processing_log.csv"):
    """Reset the global processing logger"""
    global _processing_logger
    _processing_logger = ProcessingLogger(log_file)