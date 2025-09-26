#!/usr/bin/env python3
"""
Real-time Agent Display System for Streamlit UI
Captures agent interactions and displays them in real-time
"""

import streamlit as st
import time
import threading
import queue
from datetime import datetime
from typing import Dict, List, Any
import json
import logging

class AgentActivityLogger:
    """Captures and stores agent activity for real-time display"""
    
    def __init__(self):
        self.activity_queue = queue.Queue()
        self.activity_log = []
        self.current_agent = None
        self.processing_stats = {
            'total_items': 0,
            'processed_items': 0,
            'start_time': None,
            'agents_used': set(),
            'current_phase': 'Initializing'
        }
        
    def log_agent_start(self, agent_name: str, task: str):
        """Log when an agent starts working"""
        activity = {
            'timestamp': datetime.now().strftime('%H:%M:%S'),
            'type': 'agent_start',
            'agent': agent_name,
            'message': f"🚀 {agent_name} started: {task}",
            'color': self._get_agent_color(agent_name),
            'icon': self._get_agent_icon(agent_name)
        }
        self._add_activity(activity)
        self.current_agent = agent_name
        self.processing_stats['agents_used'].add(agent_name)
        
    def log_agent_action(self, agent_name: str, action: str, details: str):
        """Log agent actions"""
        activity = {
            'timestamp': datetime.now().strftime('%H:%M:%S'),
            'type': 'agent_action',
            'agent': agent_name,
            'message': f"➤ {agent_name} {action}: {details}",
            'color': self._get_agent_color(agent_name),
            'icon': '⚙️'
        }
        self._add_activity(activity)
        
    def log_agent_complete(self, agent_name: str, result: str):
        """Log when an agent completes"""
        activity = {
            'timestamp': datetime.now().strftime('%H:%M:%S'),
            'type': 'agent_complete',
            'agent': agent_name,
            'message': f"🎉 {agent_name} completed: {result}",
            'color': self._get_agent_color(agent_name),
            'icon': '✅'
        }
        self._add_activity(activity)
        
    def log_phase_change(self, phase: str):
        """Log processing phase changes"""
        activity = {
            'timestamp': datetime.now().strftime('%H:%M:%S'),
            'type': 'phase_change',
            'agent': 'System',
            'message': f"📋 Phase: {phase}",
            'color': '#FFFFFF',
            'icon': '📋'
        }
        self._add_activity(activity)
        self.processing_stats['current_phase'] = phase
        
    def log_progress_update(self, current: int, total: int):
        """Log progress updates"""
        self.processing_stats['processed_items'] = current
        self.processing_stats['total_items'] = total
        
        progress_percent = (current / total * 100) if total > 0 else 0
        activity = {
            'timestamp': datetime.now().strftime('%H:%M:%S'),
            'type': 'progress',
            'agent': 'System',
            'message': f"📊 Progress: {current}/{total} items ({progress_percent:.1f}%)",
            'color': '#00FF00',
            'icon': '📊',
            'progress': progress_percent
        }
        self._add_activity(activity)
        
    def _add_activity(self, activity: Dict):
        """Add activity to log and queue"""
        self.activity_log.append(activity)
        try:
            self.activity_queue.put_nowait(activity)
        except queue.Full:
            pass  # Skip if queue is full
            
        # Keep only last 100 activities to prevent memory issues
        if len(self.activity_log) > 100:
            self.activity_log.pop(0)
            
    def _get_agent_color(self, agent_name: str) -> str:
        """Get color for specific agent"""
        colors = {
            'CSV Reader Agent': '#00FFFF',
            'Feedback Classifier Agent': '#00FF00', 
            'Bug Analysis Agent': '#FF6B6B',
            'Feature Extractor Agent': '#4ECDC4',
            'Priority Analyzer Agent': '#45B7D1',
            'Technical Details Agent': '#96CEB4',
            'Ticket Creator Agent': '#FFEAA7',
            'Quality Reviewer Agent': '#DDA0DD',
            'System': '#FFFFFF'
        }
        return colors.get(agent_name, '#CCCCCC')
        
    def _get_agent_icon(self, agent_name: str) -> str:
        """Get icon for specific agent"""
        icons = {
            'CSV Reader Agent': '📖',
            'Feedback Classifier Agent': '🔍',
            'Bug Analysis Agent': '🐛', 
            'Feature Extractor Agent': '🚀',
            'Priority Analyzer Agent': '⚡',
            'Technical Details Agent': '🔧',
            'Ticket Creator Agent': '🎫',
            'Quality Reviewer Agent': '✨',
            'System': '⚙️'
        }
        return icons.get(agent_name, '🤖')
        
    def get_recent_activities(self, limit: int = 10) -> List[Dict]:
        """Get recent activities for display"""
        return self.activity_log[-limit:] if self.activity_log else []
        
    def get_stats(self) -> Dict:
        """Get current processing statistics"""
        stats = self.processing_stats.copy()
        if stats['start_time']:
            elapsed = (datetime.now() - stats['start_time']).total_seconds()
            stats['elapsed_time'] = elapsed
            stats['items_per_second'] = stats['processed_items'] / elapsed if elapsed > 0 else 0
        return stats
        
    def reset(self):
        """Reset the activity logger"""
        self.activity_log.clear()
        while not self.activity_queue.empty():
            try:
                self.activity_queue.get_nowait()
            except queue.Empty:
                break
        self.processing_stats = {
            'total_items': 0,
            'processed_items': 0,
            'start_time': datetime.now(),
            'agents_used': set(),
            'current_phase': 'Initializing'
        }

# Global instance for real-time logging
realtime_logger = AgentActivityLogger()

class StreamlitAgentDisplay:
    """Displays agent activity in Streamlit interface"""
    
    def __init__(self):
        self.logger = realtime_logger
        
    def create_realtime_display(self):
        """Create real-time agent activity display"""
        
        # Create containers for different sections
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.subheader("🤖 Agent Activity Feed")
            activity_container = st.container()
            
        with col2:
            st.subheader("📊 Processing Stats")
            stats_container = st.container()
            
        return activity_container, stats_container
        
    def update_activity_display(self, activity_container):
        """Update the activity display with latest activities"""
        with activity_container:
            activities = self.logger.get_recent_activities(15)
            
            if not activities:
                st.info("🤖 Agents will appear here during processing...")
                return
                
            # Display activities in reverse order (newest first)
            for activity in reversed(activities):
                self._render_activity(activity)
                
    def update_stats_display(self, stats_container):
        """Update the statistics display"""
        with stats_container:
            stats = self.logger.get_stats()
            
            # Progress metrics
            if stats['total_items'] > 0:
                progress = stats['processed_items'] / stats['total_items']
                st.progress(progress)
                st.write(f"**Progress:** {stats['processed_items']}/{stats['total_items']} items")
            
            # Current phase
            st.write(f"**Current Phase:** {stats['current_phase']}")
            
            # Active agents
            if stats['agents_used']:
                st.write(f"**Agents Used:** {len(stats['agents_used'])}")
                agent_list = "\n".join([f"• {agent}" for agent in sorted(stats['agents_used'])])
                st.text(agent_list)
                
            # Performance stats
            if stats.get('elapsed_time'):
                st.write(f"**Elapsed Time:** {stats['elapsed_time']:.1f}s")
                if stats.get('items_per_second'):
                    st.write(f"**Speed:** {stats['items_per_second']:.1f} items/sec")
                    
    def _render_activity(self, activity: Dict):
        """Render a single activity item"""
        timestamp = activity['timestamp']
        message = activity['message']
        color = activity.get('color', '#CCCCCC')
        agent = activity.get('agent', 'Unknown')
        
        # Create colored message
        if activity['type'] == 'agent_start':
            st.markdown(f"""
            <div style="border-left: 4px solid {color}; padding-left: 10px; margin: 5px 0;">
                <span style="color: {color}; font-weight: bold;">[{timestamp}]</span> {message}
            </div>
            """, unsafe_allow_html=True)
        elif activity['type'] == 'agent_complete':
            st.markdown(f"""
            <div style="border-left: 4px solid {color}; padding-left: 10px; margin: 5px 0; background-color: rgba(0,255,0,0.1);">
                <span style="color: {color}; font-weight: bold;">[{timestamp}]</span> {message}
            </div>
            """, unsafe_allow_html=True)
        elif activity['type'] == 'progress':
            progress = activity.get('progress', 0)
            st.markdown(f"""
            <div style="border-left: 4px solid #00FF00; padding-left: 10px; margin: 5px 0;">
                <span style="color: #00FF00; font-weight: bold;">[{timestamp}]</span> {message}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div style="padding-left: 15px; margin: 2px 0; color: #888;">
                <span style="color: #888;">[{timestamp}]</span> {message}
            </div>
            """, unsafe_allow_html=True)
            
    def run_with_realtime_display(self, processing_function, *args, **kwargs):
        """Run a processing function with real-time display"""
        
        # Reset logger
        self.logger.reset()
        
        # Create display containers
        activity_container, stats_container = self.create_realtime_display()
        
        # Create placeholder for updates
        activity_placeholder = activity_container.empty()
        stats_placeholder = stats_container.empty()
        
        # Start processing in background
        result_container = st.empty()
        
        try:
            # Run the processing function
            # This should integrate with the existing processing system
            result = processing_function(*args, **kwargs)
            
            # Show final results
            with result_container:
                if result:
                    st.success(f"🎉 Processing completed! Generated {len(result)} tickets")
                else:
                    st.error("❌ Processing failed or returned no results")
                    
        except Exception as e:
            with result_container:
                st.error(f"❌ Processing error: {str(e)}")
            result = None
            
        return result

# Streamlit display instance
streamlit_display = StreamlitAgentDisplay()

def get_realtime_logger():
    """Get the global realtime logger instance"""
    return realtime_logger

def get_streamlit_display():
    """Get the streamlit display instance"""
    return streamlit_display