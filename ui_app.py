#!/usr/bin/env python3
"""
Streamlit UI for the Intelligent Feedback Analysis System
Provides a user-friendly interface for processing feedback and monitoring results
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
import time
import os
from datetime import datetime
import logging
from typing import Dict, List
import sys
import threading
import queue

# Import our custom modules
from multi_agent_system import FeedbackAnalysisSystem
from setup_script import SystemValidator
from config_manager import get_config_manager, get_current_config

# Import real-time display
try:
    from realtime_agent_display import get_realtime_logger, get_streamlit_display
    realtime_logger = get_realtime_logger()
    streamlit_display = get_streamlit_display()
    REALTIME_DISPLAY_AVAILABLE = True
except ImportError:
    realtime_logger = None
    streamlit_display = None
    REALTIME_DISPLAY_AVAILABLE = False

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FeedbackAnalysisUI:
    def __init__(self):
        self.analysis_system = FeedbackAnalysisSystem()
        self.validator = SystemValidator()
        self.config_manager = get_config_manager()
        
    def run_app(self):
        """Main Streamlit application"""
        st.set_page_config(
            page_title="Intelligent Feedback Analysis System",
            page_icon="🔍",
            layout="wide",
            initial_sidebar_state="expanded"
        )
        
        # Main title
        st.title("🔍 Intelligent Feedback Analysis System")
        st.markdown("---")
        
        # Sidebar navigation
        page = st.sidebar.selectbox(
            "Navigation",
            ["Dashboard", "Upload & Process", "Generate Tickets", "Ticket Review & Approval", "Results Analysis", "System Monitoring", "Configuration Panel", "Validation Reports"]
        )
        
        if page == "Dashboard":
            self.show_dashboard()
        elif page == "Upload & Process":
            self.show_upload_process()
        elif page == "Generate Tickets":
            self.show_generate_tickets()
        elif page == "Ticket Review & Approval":
            self.show_ticket_review_approval()
        elif page == "Results Analysis":
            self.show_results_analysis()
        elif page == "System Monitoring":
            self.show_system_monitoring()
        elif page == "Configuration Panel":
            self.show_configuration_panel()
        elif page == "Validation Reports":
            self.show_validation_reports()
    
    def show_dashboard(self):
        """Main dashboard with overview metrics"""
        st.header("📊 System Dashboard")
        
        col1, col2, col3, col4 = st.columns(4)
        
        # Check for existing data files
        files_status = self.check_data_files()
        
        with col1:
            st.metric("📧 Support Emails", files_status.get('emails_count', 0))
        
        with col2:
            st.metric("⭐ App Reviews", files_status.get('reviews_count', 0))
        
        with col3:
            st.metric("🎫 Generated Tickets", files_status.get('tickets_count', 0))
        
        with col4:
            st.metric("✅ System Status", "Ready" if files_status['system_ready'] else "Not Ready")
        
        st.markdown("---")
        
        # Data Export Section
        st.subheader("📥 Data Export")
        st.markdown("Download processed data and metrics for analysis")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            # Generated Tickets Export
            if os.path.exists('generated_tickets.csv'):
                with open('generated_tickets.csv', 'rb') as file:
                    st.download_button(
                        label="🎫 Download Tickets",
                        data=file.read(),
                        file_name=f"tickets_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                        mime="text/csv",
                        key="download_tickets_main",
                        help="Download complete ticket data with approval status"
                    )
            else:
                st.button("🎫 No Tickets", disabled=True, help="Generate tickets first")
        
        with col2:
            # Processing Log Export
            if os.path.exists('processing_log.csv'):
                with open('processing_log.csv', 'rb') as file:
                    st.download_button(
                        label="📝 Download Process Log",
                        data=file.read(),
                        file_name=f"processing_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                        mime="text/csv",
                        key="download_log_main",
                        help="Download processing history and decisions"
                    )
            else:
                st.button("📝 No Process Log", disabled=True, help="Process data first")
        
        with col3:
            # Metrics Export
            if os.path.exists('metrics.csv'):
                with open('metrics.csv', 'rb') as file:
                    st.download_button(
                        label="📊 Download Metrics",
                        data=file.read(),
                        file_name=f"metrics_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                        mime="text/csv",
                        key="download_metrics_main",
                        help="Download aggregated statistics and metrics"
                    )
            else:
                st.button("📊 No Metrics", disabled=True, help="Process data to generate metrics")
        
        with col4:
            # All Files Export (ZIP)
            if any(os.path.exists(f) for f in ['generated_tickets.csv', 'processing_log.csv', 'metrics.csv']):
                if st.button("📦 Download All", key="download_all_main", help="Download all CSV files as ZIP"):
                    self._create_export_package()
            else:
                st.button("📦 No Data", disabled=True, help="No data files available")
        
        st.markdown("---")
        
        # System overview
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.subheader("📈 Recent Activity")
            if os.path.exists('processing_log.csv'):
                log_df = pd.read_csv('processing_log.csv')
                if not log_df.empty:
                    fig = px.histogram(log_df, x='category', title="Feedback Categories Processed")
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("No processing activity yet. Upload files to get started!")
            else:
                st.info("No processing log found. Process some feedback first!")
        
        with col2:
            st.subheader("🎯 Quick Actions")
            if st.button("🔄 Refresh Dashboard", key="refresh_dash"):
                st.rerun()
            
            if st.button("📁 Process Sample Data", key="process_sample"):
                if files_status['has_sample_data']:
                    with st.spinner("Processing sample data..."):
                        self.process_sample_data()
                    st.success("Sample data processed!")
                    st.rerun()
                else:
                    st.warning("No sample data found!")
    
    def show_upload_process(self):
        """File upload and processing interface"""
        st.header("📤 Upload & Process Feedback")
        
        # File upload section
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📧 Support Emails")
            emails_file = st.file_uploader(
                "Upload support emails CSV",
                type=['csv'],
                key="emails_upload",
                help="CSV file with columns: email_id, subject, body, sender_email, timestamp"
            )
            
            if emails_file:
                try:
                    emails_df = pd.read_csv(emails_file)
                    st.write(f"📊 Preview ({len(emails_df)} rows):")
                    st.dataframe(emails_df.head())
                    
                    # Save uploaded file
                    emails_df.to_csv('support_emails.csv', index=False)
                    st.success(f"✅ Saved {len(emails_df)} support emails")
                except Exception as e:
                    st.error(f"Error reading file: {str(e)}")
        
        with col2:
            st.subheader("⭐ App Store Reviews")
            reviews_file = st.file_uploader(
                "Upload app store reviews CSV",
                type=['csv'],
                key="reviews_upload",
                help="CSV file with columns: review_id, platform, rating, review_text, user_name, date, app_version"
            )
            
            if reviews_file:
                try:
                    reviews_df = pd.read_csv(reviews_file)
                    st.write(f"📊 Preview ({len(reviews_df)} rows):")
                    st.dataframe(reviews_df.head())
                    
                    # Save uploaded file
                    reviews_df.to_csv('app_store_reviews.csv', index=False)
                    st.success(f"✅ Saved {len(reviews_df)} app store reviews")
                except Exception as e:
                    st.error(f"Error reading file: {str(e)}")
        
        st.markdown("---")
        
        # Processing section
        st.subheader("⚙️ Process Feedback")
        
        col1, col2, col3 = st.columns([1, 1, 2])
        
        with col1:
            if st.button("🚀 Start Processing", key="start_processing", type="primary"):
                if os.path.exists('support_emails.csv') and os.path.exists('app_store_reviews.csv'):
                    self.run_processing_with_progress()
                else:
                    st.error("Please upload both support emails and app store reviews files first!")
        
        with col2:
            if st.button("🧪 Use Sample Data", key="use_sample"):
                if self.check_data_files()['has_sample_data']:
                    self.run_processing_with_progress()
                else:
                    st.error("Sample data files not found!")
        
        with col3:
            st.info("💡 Processing will analyze feedback, classify categories, determine priorities, and generate tickets.")
    
    def show_generate_tickets(self):
        """Dedicated ticket generation interface"""
        st.header("🎫 Generate Tickets")
        
        # Check for processed data
        if not (os.path.exists('app_store_reviews.csv') or os.path.exists('support_emails.csv')):
            st.warning("⚠️ No data files found. Please upload files in the 'Upload & Process' section first.")
            return
        
        # Ticket generation options
        st.subheader("🔧 Ticket Generation Options")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Data Sources**")
            use_reviews = st.checkbox("📱 Include App Store Reviews", value=True, 
                                    disabled=not os.path.exists('app_store_reviews.csv'))
            use_emails = st.checkbox("📧 Include Support Emails", value=True, 
                                   disabled=not os.path.exists('support_emails.csv'))
            
            # Filter options
            st.write("**Filtering Options**")
            min_confidence = st.slider("Minimum Confidence Score", 0, 100, 60,
                                     help="Only generate tickets for feedback with confidence above this threshold")
            
            priority_filter = st.multiselect("Priority Levels", 
                                           ["Critical", "High", "Medium", "Low"], 
                                           default=["Critical", "High", "Medium", "Low"])
            
            category_filter = st.multiselect("Categories", 
                                           ["Bug", "Feature Request", "Praise", "Complaint", "Spam"],
                                           default=["Bug", "Feature Request", "Complaint"])
        
        with col2:
            st.write("**Ticket Settings**")
            ticket_prefix = st.text_input("Ticket ID Prefix", value="TICKET", 
                                        help="Prefix for generated ticket IDs")
            
            include_technical_details = st.checkbox("Include Technical Details", value=True)
            include_user_info = st.checkbox("Include User Information", value=True)
            include_timestamps = st.checkbox("Include Timestamps", value=True)
            
            # Output format
            st.write("**Output Format**")
            output_format = st.radio("Export Format", ["CSV", "JSON", "Excel"], horizontal=True)
            
            # Advanced options
            with st.expander("🔍 Advanced Options"):
                batch_size = st.number_input("Batch Size", min_value=10, max_value=1000, value=100,
                                           help="Number of items to process at once")
                enable_colorful_logging = st.checkbox("Enable Colorful Console Logging", value=True)
                processing_mode = st.radio("Processing Mode", 
                                          ["Simple (Fast)", "Hybrid Agents (Recommended)", "Full CrewAI (Needs LLM)"], 
                                          index=1,
                                          help="Choose processing approach")
                save_processing_log = st.checkbox("Save Detailed Processing Log", value=True)
                
                if processing_mode == "Simple (Fast)":
                    st.info("⚡ Fast processing without agent logging")
                elif processing_mode == "Hybrid Agents (Recommended)":
                    st.info("🤖 **Recommended**: All agents get used with colorful logging, no LLM required")
                    st.info("🎯 Agents: CSV Reader → Classifier → Bug Analyzer → Feature Extractor → **Ticket Creator** → Quality Reviewer")
                else:
                    st.info("🌟 Full CrewAI pipeline with LLM backend")
                    st.info("🔑 **Supported LLMs:** Google Gemini (GOOGLE_API_KEY), OpenAI (OPENAI_API_KEY), Anthropic Claude (ANTHROPIC_API_KEY)")
                    st.info("🚀 **Recommended**: Set GOOGLE_API_KEY to use Google Gemini")
                    st.warning("⚠️ May fall back to hybrid mode if no LLM is configured")
        
        st.markdown("---")
        
        # Generation controls
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            if st.button("🚀 Generate Tickets", type="primary", key="generate_tickets"):
                self.run_ticket_generation(
                    use_reviews=use_reviews,
                    use_emails=use_emails,
                    min_confidence=min_confidence,
                    priority_filter=priority_filter,
                    category_filter=category_filter,
                    ticket_prefix=ticket_prefix,
                    include_technical_details=include_technical_details,
                    include_user_info=include_user_info,
                    include_timestamps=include_timestamps,
                    output_format=output_format,
                    batch_size=batch_size,
                    enable_colorful_logging=enable_colorful_logging,
                    processing_mode=processing_mode,
                    save_processing_log=save_processing_log
                )
        
        with col2:
            if st.button("🔍 Preview Settings", key="preview_settings"):
                self.preview_ticket_settings(use_reviews, use_emails, category_filter, priority_filter)
        
        with col3:
            if os.path.exists('generated_tickets.csv'):
                with open('generated_tickets.csv', 'rb') as file:
                    st.download_button(
                        label="📥 Download Latest",
                        data=file.read(),
                        file_name=f"tickets_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                        mime="text/csv",
                        key="download_latest"
                    )
        
        # Show recent generation history
        if os.path.exists('processing_log.csv'):
            st.subheader("📋 Recent Generation History")
            log_df = pd.read_csv('processing_log.csv')
            
            if not log_df.empty:
                # Show last 10 generations
                recent_log = log_df.tail(10).sort_values('processing_time', ascending=False)
                
                for _, entry in recent_log.head(5).iterrows():
                    with st.expander(f"🎫 {entry.get('category', 'Unknown')} - {entry.get('processing_time', 'Unknown time')[:19]}"):
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.write(f"**Source ID:** {entry.get('source_id', 'N/A')}")
                            st.write(f"**Type:** {entry.get('source_type', 'N/A')}")
                        with col2:
                            st.write(f"**Category:** {entry.get('category', 'N/A')}")
                            st.write(f"**Confidence:** {entry.get('confidence', 0):.1f}%")
                        with col3:
                            st.write(f"**Status:** {entry.get('status', 'Unknown')}")
                            if entry.get('confidence', 0) >= 80:
                                st.success("High Confidence")
                            elif entry.get('confidence', 0) >= 60:
                                st.warning("Medium Confidence")
                            else:
                                st.error("Low Confidence")
        
        # Statistics summary
        if os.path.exists('generated_tickets.csv'):
            st.subheader("📊 Generation Statistics")
            tickets_df = pd.read_csv('generated_tickets.csv')
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Tickets", len(tickets_df))
            with col2:
                avg_conf = tickets_df.get('confidence_score', pd.Series([0])).mean()
                st.metric("Avg Confidence", f"{avg_conf:.1f}%")
            with col3:
                critical_count = len(tickets_df[tickets_df.get('priority', '') == 'Critical'])
                st.metric("Critical Issues", critical_count)
            with col4:
                open_count = len(tickets_df[tickets_df.get('status', '') == 'Open'])
                st.metric("Open Tickets", open_count)
    
    def show_results_analysis(self):
        """Analysis results and visualizations"""
        st.header("📊 Results Analysis")
        
        if not os.path.exists('generated_tickets.csv'):
            st.warning("No analysis results found. Please process some feedback first!")
            return
        
        # Load results data
        tickets_df = pd.read_csv('generated_tickets.csv')
        
        # Summary metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("🎫 Total Tickets", len(tickets_df))
        
        with col2:
            avg_confidence = tickets_df['confidence_score'].mean()
            st.metric("🎯 Avg Confidence", f"{avg_confidence:.1f}%")
        
        with col3:
            critical_count = len(tickets_df[tickets_df['priority'] == 'Critical'])
            st.metric("🚨 Critical Issues", critical_count)
        
        with col4:
            bug_count = len(tickets_df[tickets_df['category'] == 'Bug'])
            st.metric("🐛 Bug Reports", bug_count)
        
        st.markdown("---")
        
        # Visualizations
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📈 Category Distribution")
            category_counts = tickets_df['category'].value_counts()
            fig_cat = px.pie(
                values=category_counts.values,
                names=category_counts.index,
                title="Feedback Categories"
            )
            st.plotly_chart(fig_cat, use_container_width=True)
        
        with col2:
            st.subheader("⚡ Priority Levels")
            priority_counts = tickets_df['priority'].value_counts()
            colors = {'Critical': 'red', 'High': 'orange', 'Medium': 'yellow', 'Low': 'green'}
            fig_pri = px.bar(
                x=priority_counts.index,
                y=priority_counts.values,
                title="Priority Distribution",
                color=priority_counts.index,
                color_discrete_map=colors
            )
            st.plotly_chart(fig_pri, use_container_width=True)
        
        # Confidence analysis
        st.subheader("🎯 Confidence Score Analysis")
        fig_conf = px.histogram(
            tickets_df,
            x='confidence_score',
            nbins=20,
            title="Confidence Score Distribution"
        )
        st.plotly_chart(fig_conf, use_container_width=True)
        
        # Detailed ticket view
        st.subheader("🎫 Generated Tickets")
        
        # Filters
        col1, col2, col3 = st.columns(3)
        with col1:
            category_filter = st.selectbox("Filter by Category", ["All"] + list(tickets_df['category'].unique()))
        with col2:
            priority_filter = st.selectbox("Filter by Priority", ["All"] + list(tickets_df['priority'].unique()))
        with col3:
            min_confidence = st.slider(
                "Minimum Confidence", 
                min_value=0.0, 
                max_value=100.0, 
                value=0.0, 
                step=1.0,
                help="Filter tickets by minimum confidence score",
                key="confidence_filter_slider"
            )
        
        # Apply filters
        filtered_df = tickets_df.copy()
        
        # Ensure confidence_score is numeric
        filtered_df['confidence_score'] = pd.to_numeric(filtered_df['confidence_score'], errors='coerce')
        
        if category_filter != "All":
            filtered_df = filtered_df[filtered_df['category'] == category_filter]
        if priority_filter != "All":
            filtered_df = filtered_df[filtered_df['priority'] == priority_filter]
        filtered_df = filtered_df[filtered_df['confidence_score'] >= min_confidence]
        
        # Show filter results
        st.write(f"**Showing {len(filtered_df)} of {len(tickets_df)} tickets** (min confidence: {min_confidence}%)")
        
        # Debug info (can be removed later)
        with st.expander("🔍 Debug Info", expanded=False):
            conf_values = tickets_df['confidence_score'].unique()
            st.write(f"Available confidence scores: {sorted(conf_values)}")
            st.write(f"Filter threshold: {min_confidence}")
            st.write(f"Tickets meeting threshold: {len(filtered_df)}")
        
        if filtered_df.empty:
            st.warning(f"No tickets found with confidence >= {min_confidence}%. Try lowering the confidence threshold.")
        else:
            st.dataframe(filtered_df[['ticket_id', 'category', 'priority', 'title', 'confidence_score', 'status']], use_container_width=True)
        
        # Download results
        csv = filtered_df.to_csv(index=False)
        st.download_button(
            label="📥 Download Filtered Results",
            data=csv,
            file_name=f"filtered_tickets_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )
    
    def show_system_monitoring(self):
        """Real-time system monitoring"""
        st.header("🖥️ System Monitoring")
        
        # System health metrics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("💾 Memory Usage", "85%", "-2%")
        
        with col2:
            st.metric("⏱️ Processing Time", "2.3s", "+0.1s")
        
        with col3:
            st.metric("📊 Success Rate", "98.5%", "+1.2%")
        
        # Processing log
        if os.path.exists('processing_log.csv'):
            st.subheader("📋 Processing Log")
            log_df = pd.read_csv('processing_log.csv')
            
            # Recent activity
            st.write("Recent Processing Activity:")
            st.dataframe(log_df.tail(10), use_container_width=True)
            
            # Processing timeline
            if not log_df.empty and 'processing_time' in log_df.columns:
                log_df['processing_time'] = pd.to_datetime(log_df['processing_time'])
                fig_timeline = px.scatter(
                    log_df,
                    x='processing_time',
                    y='confidence',
                    color='category',
                    title="Processing Timeline",
                    hover_data=['source_id', 'status']
                )
                st.plotly_chart(fig_timeline, use_container_width=True)
        else:
            st.info("No processing log available yet.")
        
        # Auto-refresh option
        if st.checkbox("🔄 Auto-refresh (every 5 seconds)"):
            time.sleep(5)
            st.rerun()
    
    def show_configuration_panel(self):
        """Configuration panel for adjusting classification thresholds and priorities"""
        st.header("⚙️ Configuration Panel")
        st.markdown("Adjust classification thresholds, priority weights, and system settings to optimize performance.")
        
        # Load current configuration
        config = self.config_manager.config
        
        # Configuration validation
        validation = self.config_manager.validate_configuration()
        if not validation['valid']:
            st.error("⚠️ Configuration Issues Found:")
            for issue in validation['issues']:
                st.error(f"• {issue}")
        
        if validation['warnings']:
            st.warning("⚠️ Configuration Warnings:")
            for warning in validation['warnings']:
                st.warning(f"• {warning}")
        
        # Create tabs for different configuration sections
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "🎯 Classification Thresholds", 
            "⚖️ Priority Weights", 
            "✅ Quality Thresholds", 
            "🤖 Agent Settings", 
            "🔧 Processing Rules"
        ])
        
        with tab1:
            self._show_classification_config(config)
        
        with tab2:
            self._show_priority_config(config)
        
        with tab3:
            self._show_quality_config(config)
        
        with tab4:
            self._show_agent_config(config)
        
        with tab5:
            self._show_processing_config(config)
        
        # Configuration management actions
        st.markdown("---")
        st.subheader("🔧 Configuration Management")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if st.button("💾 Save Configuration", type="primary"):
                if self.config_manager.save_configuration():
                    st.success("✅ Configuration saved successfully!")
                    st.rerun()
                else:
                    st.error("❌ Failed to save configuration")
        
        with col2:
            if st.button("🔄 Reset to Defaults"):
                if st.session_state.get('confirm_reset', False):
                    if self.config_manager.reset_to_defaults():
                        st.success("✅ Configuration reset to defaults!")
                        st.session_state['confirm_reset'] = False
                        st.rerun()
                    else:
                        st.error("❌ Failed to reset configuration")
                else:
                    st.session_state['confirm_reset'] = True
                    st.warning("Click again to confirm reset to defaults")
        
        with col3:
            if st.button("📤 Export Config"):
                export_file = f"config_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                if self.config_manager.export_configuration(export_file):
                    st.success(f"✅ Configuration exported to {export_file}")
                    # Provide download link
                    with open(export_file, 'r') as f:
                        st.download_button(
                            label="⬇️ Download Config File",
                            data=f.read(),
                            file_name=export_file,
                            mime="application/json"
                        )
        
        with col4:
            uploaded_config = st.file_uploader("📤 Import Config", type=['json'], key="config_import")
            if uploaded_config is not None:
                try:
                    import tempfile
                    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as tmp_file:
                        tmp_file.write(uploaded_config.getvalue().decode('utf-8'))
                        temp_path = tmp_file.name
                    
                    if self.config_manager.import_configuration(temp_path):
                        st.success("✅ Configuration imported successfully!")
                        os.unlink(temp_path)
                        st.rerun()
                    else:
                        st.error("❌ Failed to import configuration")
                        os.unlink(temp_path)
                except Exception as e:
                    st.error(f"❌ Import error: {str(e)}")
        
        # Show current configuration info
        st.markdown("---")
        st.subheader("ℹ️ Configuration Information")
        info_col1, info_col2 = st.columns(2)
        
        with info_col1:
            st.info(f"**Version:** {config.version}")
            st.info(f"**Created by:** {config.created_by}")
        
        with info_col2:
            st.info(f"**Last updated:** {config.last_updated}")
            validation_status = "✅ Valid" if validation['valid'] else "❌ Has Issues"
            st.info(f"**Status:** {validation_status}")
    
    def _show_classification_config(self, config):
        """Show classification threshold configuration"""
        st.subheader("🎯 Classification Confidence Thresholds")
        st.markdown("Set minimum confidence scores required for each category classification.")
        
        # Create two columns for better layout
        col1, col2 = st.columns(2)
        
        with col1:
            bug_threshold = st.slider(
                "🐛 Bug Classification Threshold",
                min_value=0.0, max_value=1.0, 
                value=config.classification_thresholds.bug_threshold,
                step=0.05,
                help="Minimum confidence required to classify feedback as a bug report"
            )
            
            feature_threshold = st.slider(
                "✨ Feature Request Threshold", 
                min_value=0.0, max_value=1.0,
                value=config.classification_thresholds.feature_threshold,
                step=0.05,
                help="Minimum confidence required to classify feedback as a feature request"
            )
            
            praise_threshold = st.slider(
                "👍 Praise Classification Threshold",
                min_value=0.0, max_value=1.0,
                value=config.classification_thresholds.praise_threshold, 
                step=0.05,
                help="Minimum confidence required to classify feedback as praise"
            )
        
        with col2:
            complaint_threshold = st.slider(
                "😠 Complaint Classification Threshold",
                min_value=0.0, max_value=1.0,
                value=config.classification_thresholds.complaint_threshold,
                step=0.05,
                help="Minimum confidence required to classify feedback as a complaint"
            )
            
            spam_threshold = st.slider(
                "🚫 Spam Detection Threshold",
                min_value=0.0, max_value=1.0,
                value=config.classification_thresholds.spam_threshold,
                step=0.05,
                help="Minimum confidence required to classify feedback as spam"
            )
            
            minimum_confidence = st.slider(
                "⚖️ Global Minimum Confidence",
                min_value=0.0, max_value=1.0,
                value=config.classification_thresholds.minimum_confidence,
                step=0.05,
                help="Overall minimum confidence threshold for any classification"
            )
        
        # Update configuration if values changed
        if st.button("💾 Apply Classification Changes", key="apply_classification"):
            updates = {
                'bug_threshold': bug_threshold,
                'feature_threshold': feature_threshold, 
                'praise_threshold': praise_threshold,
                'complaint_threshold': complaint_threshold,
                'spam_threshold': spam_threshold,
                'minimum_confidence': minimum_confidence
            }
            
            if self.config_manager.update_classification_thresholds(**updates):
                st.success("✅ Classification thresholds updated!")
                st.rerun()
            else:
                st.error("❌ Failed to update thresholds")
    
    def _show_priority_config(self, config):
        """Show priority weight configuration"""
        st.subheader("⚖️ Priority Assignment Weights")
        st.markdown("Configure how different factors contribute to priority scoring.")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Priority Calculation Weights:**")
            bug_severity_weight = st.slider(
                "🐛 Bug Severity Weight",
                min_value=0.0, max_value=1.0,
                value=config.priority_weights.bug_severity_weight,
                step=0.1,
                help="How much bug severity affects priority"
            )
            
            user_impact_weight = st.slider(
                "👥 User Impact Weight", 
                min_value=0.0, max_value=1.0,
                value=config.priority_weights.user_impact_weight,
                step=0.1,
                help="How much user impact affects priority"
            )
            
            technical_complexity_weight = st.slider(
                "🔧 Technical Complexity Weight",
                min_value=0.0, max_value=1.0,
                value=config.priority_weights.technical_complexity_weight,
                step=0.1,
                help="How much technical complexity affects priority"
            )
            
            business_priority_weight = st.slider(
                "💼 Business Priority Weight",
                min_value=0.0, max_value=1.0, 
                value=config.priority_weights.business_priority_weight,
                step=0.1,
                help="How much business priority affects overall priority"
            )
        
        with col2:
            st.markdown("**Weight Summary:**")
            total_weight = (bug_severity_weight + user_impact_weight + 
                          technical_complexity_weight + business_priority_weight)
            
            weight_data = {
                'Factor': ['Bug Severity', 'User Impact', 'Technical Complexity', 'Business Priority'],
                'Weight': [bug_severity_weight, user_impact_weight, technical_complexity_weight, business_priority_weight],
                'Percentage': [f"{w/total_weight*100:.1f}%" for w in [bug_severity_weight, user_impact_weight, technical_complexity_weight, business_priority_weight]]
            }
            
            weight_df = pd.DataFrame(weight_data)
            st.dataframe(weight_df, use_container_width=True)
            
            if abs(total_weight - 1.0) > 0.1:
                st.warning(f"⚠️ Weights sum to {total_weight:.2f} (should be close to 1.0)")
            else:
                st.success(f"✅ Weights sum to {total_weight:.2f}")
        
        # Update configuration
        if st.button("💾 Apply Priority Changes", key="apply_priority"):
            updates = {
                'bug_severity_weight': bug_severity_weight,
                'user_impact_weight': user_impact_weight,
                'technical_complexity_weight': technical_complexity_weight,
                'business_priority_weight': business_priority_weight
            }
            
            if self.config_manager.update_priority_weights(**updates):
                st.success("✅ Priority weights updated!")
                st.rerun()
            else:
                st.error("❌ Failed to update priority weights")
    
    def _show_quality_config(self, config):
        """Show quality threshold configuration"""
        st.subheader("✅ Quality Review Thresholds")
        st.markdown("Configure quality scoring and review criteria.")
        
        col1, col2 = st.columns(2)
        
        with col1:
            minimum_quality_score = st.slider(
                "📊 Minimum Quality Score",
                min_value=0.0, max_value=100.0,
                value=config.quality_thresholds.minimum_quality_score,
                step=5.0,
                help="Minimum acceptable quality score"
            )
            
            auto_approve_threshold = st.slider(
                "✅ Auto-Approve Threshold", 
                min_value=0.0, max_value=100.0,
                value=config.quality_thresholds.auto_approve_threshold,
                step=5.0,
                help="Quality score for automatic approval"
            )
        
        with col2:
            manual_review_threshold = st.slider(
                "👁️ Manual Review Threshold",
                min_value=0.0, max_value=100.0,
                value=config.quality_thresholds.manual_review_threshold,
                step=5.0,
                help="Quality score requiring manual review"
            )
            
            reject_threshold = st.slider(
                "❌ Reject Threshold",
                min_value=0.0, max_value=100.0,
                value=config.quality_thresholds.reject_threshold,
                step=5.0,
                help="Quality score for automatic rejection"
            )
        
        # Validation logic
        thresholds = [reject_threshold, manual_review_threshold, auto_approve_threshold]
        if thresholds != sorted(thresholds):
            st.error("⚠️ Thresholds must be in ascending order: Reject < Manual Review < Auto-Approve")
        else:
            st.success("✅ Threshold order is valid")
        
        # Quality workflow diagram
        st.markdown("**Quality Review Workflow:**")
        workflow_data = {
            'Score Range': [
                f"< {reject_threshold}",
                f"{reject_threshold} - {manual_review_threshold}",
                f"{manual_review_threshold} - {auto_approve_threshold}",
                f"> {auto_approve_threshold}"
            ],
            'Action': ['Reject', 'Manual Review Required', 'Conditional Approval', 'Auto-Approve'],
            'Status': ['❌ Rejected', '👁️ Needs Review', '⚠️ Review Optional', '✅ Approved']
        }
        
        workflow_df = pd.DataFrame(workflow_data)
        st.dataframe(workflow_df, use_container_width=True)
        
        # Update configuration
        if st.button("💾 Apply Quality Changes", key="apply_quality"):
            updates = {
                'minimum_quality_score': minimum_quality_score,
                'auto_approve_threshold': auto_approve_threshold,
                'manual_review_threshold': manual_review_threshold,
                'reject_threshold': reject_threshold
            }
            
            if self.config_manager.update_quality_thresholds(**updates):
                st.success("✅ Quality thresholds updated!")
                st.rerun()
            else:
                st.error("❌ Failed to update quality thresholds")
    
    def _show_agent_config(self, config):
        """Show agent settings configuration"""
        st.subheader("🤖 Agent Settings")
        st.markdown("Configure individual agent behaviors and timeouts.")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Enable/Disable Agents:**")
            enable_bug_analysis = st.checkbox(
                "🐛 Bug Analysis Agent",
                value=config.agent_settings.enable_bug_analysis,
                help="Enable automatic bug analysis and severity assessment"
            )
            
            enable_feature_extraction = st.checkbox(
                "✨ Feature Extraction Agent",
                value=config.agent_settings.enable_feature_extraction,
                help="Enable feature request analysis and impact assessment"
            )
            
            enable_quality_review = st.checkbox(
                "✅ Quality Review Agent",
                value=config.agent_settings.enable_quality_review,
                help="Enable automated quality review and scoring"
            )
            
            enable_technical_extraction = st.checkbox(
                "🔧 Technical Details Agent",
                value=config.agent_settings.enable_technical_extraction,
                help="Enable extraction of technical information from feedback"
            )
        
        with col2:
            st.markdown("**Agent Timeouts (seconds):**")
            classification_timeout = st.number_input(
                "Classification Timeout",
                min_value=10, max_value=120,
                value=config.agent_settings.classification_timeout,
                step=5,
                help="Maximum time for classification agent"
            )
            
            bug_analysis_timeout = st.number_input(
                "Bug Analysis Timeout",
                min_value=10, max_value=120,
                value=config.agent_settings.bug_analysis_timeout,
                step=5,
                help="Maximum time for bug analysis agent"
            )
            
            feature_extraction_timeout = st.number_input(
                "Feature Extraction Timeout", 
                min_value=10, max_value=120,
                value=config.agent_settings.feature_extraction_timeout,
                step=5,
                help="Maximum time for feature extraction agent"
            )
            
            quality_review_timeout = st.number_input(
                "Quality Review Timeout",
                min_value=10, max_value=120,
                value=config.agent_settings.quality_review_timeout,
                step=5,
                help="Maximum time for quality review agent"
            )
        
        # Agent status summary
        st.markdown("**Agent Status Summary:**")
        agent_status = {
            'Agent': ['Bug Analysis', 'Feature Extraction', 'Quality Review', 'Technical Details'],
            'Status': [
                '✅ Enabled' if enable_bug_analysis else '❌ Disabled',
                '✅ Enabled' if enable_feature_extraction else '❌ Disabled', 
                '✅ Enabled' if enable_quality_review else '❌ Disabled',
                '✅ Enabled' if enable_technical_extraction else '❌ Disabled'
            ],
            'Timeout': [
                f"{bug_analysis_timeout}s",
                f"{feature_extraction_timeout}s", 
                f"{quality_review_timeout}s",
                "N/A"
            ]
        }
        
        status_df = pd.DataFrame(agent_status)
        st.dataframe(status_df, use_container_width=True)
        
        # Update configuration
        if st.button("💾 Apply Agent Changes", key="apply_agents"):
            updates = {
                'enable_bug_analysis': enable_bug_analysis,
                'enable_feature_extraction': enable_feature_extraction,
                'enable_quality_review': enable_quality_review,
                'enable_technical_extraction': enable_technical_extraction,
                'classification_timeout': classification_timeout,
                'bug_analysis_timeout': bug_analysis_timeout,
                'feature_extraction_timeout': feature_extraction_timeout,
                'quality_review_timeout': quality_review_timeout
            }
            
            if self.config_manager.update_agent_settings(**updates):
                st.success("✅ Agent settings updated!")
                st.rerun()
            else:
                st.error("❌ Failed to update agent settings")
    
    def _show_processing_config(self, config):
        """Show processing rules configuration"""
        st.subheader("🔧 Processing Rules")
        st.markdown("Configure general processing behavior and rules.")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Processing Behavior:**")
            skip_low_confidence_items = st.checkbox(
                "⏭️ Skip Low Confidence Items",
                value=config.processing_rules.skip_low_confidence_items,
                help="Skip processing items below minimum confidence threshold"
            )
            
            auto_categorize_spam = st.checkbox(
                "🚫 Auto-categorize Spam",
                value=config.processing_rules.auto_categorize_spam,
                help="Automatically categorize detected spam without further processing"
            )
            
            require_manual_review_for_critical = st.checkbox(
                "👁️ Manual Review for Critical",
                value=config.processing_rules.require_manual_review_for_critical,
                help="Require manual review for all critical priority items"
            )
        
        with col2:
            st.markdown("**Processing Parameters:**")
            batch_size = st.number_input(
                "Batch Size",
                min_value=1, max_value=100,
                value=config.processing_rules.batch_size,
                step=5,
                help="Number of items to process in each batch"
            )
            
            max_retries = st.number_input(
                "Max Retries",
                min_value=0, max_value=10,
                value=config.processing_rules.max_retries,
                step=1,
                help="Maximum number of retry attempts for failed processing"
            )
        
        # Processing rules summary
        st.markdown("**Processing Rules Summary:**")
        rules_data = {
            'Rule': [
                'Skip Low Confidence',
                'Auto-categorize Spam', 
                'Manual Review Critical',
                'Batch Processing',
                'Error Handling'
            ],
            'Setting': [
                '✅ Enabled' if skip_low_confidence_items else '❌ Disabled',
                '✅ Enabled' if auto_categorize_spam else '❌ Disabled',
                '✅ Enabled' if require_manual_review_for_critical else '❌ Disabled',
                f"{batch_size} items per batch",
                f"Up to {max_retries} retries"
            ]
        }
        
        rules_df = pd.DataFrame(rules_data)
        st.dataframe(rules_df, use_container_width=True)
        
        # Update configuration
        if st.button("💾 Apply Processing Changes", key="apply_processing"):
            updates = {
                'skip_low_confidence_items': skip_low_confidence_items,
                'auto_categorize_spam': auto_categorize_spam,
                'require_manual_review_for_critical': require_manual_review_for_critical,
                'batch_size': batch_size,
                'max_retries': max_retries
            }
            
            if self.config_manager.update_processing_rules(**updates):
                st.success("✅ Processing rules updated!")
                st.rerun()
            else:
                st.error("❌ Failed to update processing rules")
    
    def show_ticket_review_approval(self):
        """Ticket review and approval interface"""
        st.header("🎫 Ticket Review & Approval")
        st.markdown("Review, edit, and approve generated tickets before finalizing them.")
        
        # Add usage instructions
        with st.expander("ℹ️ How to Use Ticket Approval", expanded=False):
            st.markdown("""
            **Ticket Approval Workflow:**
            1. 📋 **Review each ticket** - Check title, description, category, and priority
            2. ✏️ **Edit if needed** - Modify any fields before approval
            3. 📝 **Add review notes** - Document your decision reasoning
            4. ✅ **Approve** - Accept the ticket as-is or with modifications
            5. ❌ **Reject** - Decline tickets that don't meet criteria
            6. 🔄 **Needs Changes** - Mark tickets requiring further modification
            
            **Bulk Actions:**
            - Use "✅ Approve All Visible" to approve multiple tickets at once
            - Set your reviewer name in the top-right input field
            - Use filters to focus on specific categories or priorities
            
            **Status Meanings:**
            - 🟡 **Pending Review** - Waiting for your decision
            - 🟢 **Approved** - Ready for implementation  
            - 🔴 **Rejected** - Will not be implemented
            - 🟠 **Needs Changes** - Requires modification before approval
            """)
        
        # Check if tickets exist
        if not os.path.exists('generated_tickets.csv'):
            st.warning("⚠️ No generated tickets found. Please generate tickets first.")
            if st.button("🎫 Go to Ticket Generation"):
                st.switch_page("Generate Tickets")
            return
        
        # Load tickets
        try:
            tickets_df = pd.read_csv('generated_tickets.csv')
            if tickets_df.empty:
                st.info("ℹ️ No tickets available for review.")
                return
        except Exception as e:
            st.error(f"❌ Error loading tickets: {str(e)}")
            
            # Check if it's a CSV parsing error and try to auto-fix
            if "Expected" in str(e) and "fields" in str(e):
                st.warning("🔧 Detected CSV format issue. Attempting automatic fix...")
                try:
                    self._fix_csv_format()
                    st.success("✅ CSV format fixed! Please refresh the page.")
                    if st.button("🔄 Refresh Page"):
                        st.rerun()
                except Exception as fix_error:
                    st.error(f"❌ Auto-fix failed: {str(fix_error)}")
                    st.error("Manual intervention may be required.")
            else:
                st.error("This might be due to CSV formatting issues. Try regenerating tickets.")
                if st.button("🔄 Try to Fix CSV Format"):
                    self._fix_csv_format()
            return
        
        # Add status column if it doesn't exist
        if 'approval_status' not in tickets_df.columns:
            tickets_df['approval_status'] = 'Pending Review'
        
        if 'approved_by' not in tickets_df.columns:
            tickets_df['approved_by'] = ''
        
        if 'approval_date' not in tickets_df.columns:
            tickets_df['approval_date'] = ''
        
        if 'review_notes' not in tickets_df.columns:
            tickets_df['review_notes'] = ''
        
        # Ticket filtering and statistics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_tickets = len(tickets_df)
            st.metric("📊 Total Tickets", total_tickets)
        
        with col2:
            approved_count = len(tickets_df[tickets_df['approval_status'] == 'Approved'])
            st.metric("✅ Approved", approved_count)
        
        with col3:
            pending_count = len(tickets_df[tickets_df['approval_status'] == 'Pending Review'])
            st.metric("⏳ Pending Review", pending_count)
        
        with col4:
            rejected_count = len(tickets_df[tickets_df['approval_status'] == 'Rejected'])
            st.metric("❌ Rejected", rejected_count)
        
        st.markdown("---")
        
        # Filter options
        col1, col2, col3 = st.columns(3)
        
        with col1:
            status_filter = st.selectbox(
                "Filter by Status",
                ["All", "Pending Review", "Approved", "Rejected", "Needs Changes"],
                index=1  # Default to Pending Review
            )
        
        with col2:
            category_filter = st.selectbox(
                "Filter by Category", 
                ["All"] + list(tickets_df['category'].unique())
            )
        
        with col3:
            priority_filter = st.selectbox(
                "Filter by Priority",
                ["All"] + list(tickets_df['priority'].unique())
            )
        
        # Apply filters
        filtered_df = tickets_df.copy()
        
        if status_filter != "All":
            filtered_df = filtered_df[filtered_df['approval_status'] == status_filter]
        
        if category_filter != "All":
            filtered_df = filtered_df[filtered_df['category'] == category_filter]
        
        if priority_filter != "All":
            filtered_df = filtered_df[filtered_df['priority'] == priority_filter]
        
        st.subheader(f"📋 Tickets ({len(filtered_df)} items)")
        
        if filtered_df.empty:
            st.info("No tickets match the current filters.")
            return
        
        # Bulk actions
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            st.write("**Bulk Actions:**")
        
        with col2:
            if st.button("✅ Approve All Visible", key="bulk_approve"):
                if st.session_state.get('confirm_bulk_approve', False):
                    filtered_df.loc[:, 'approval_status'] = 'Approved'
                    filtered_df.loc[:, 'approved_by'] = st.session_state.get('reviewer_name', 'System User')
                    filtered_df.loc[:, 'approval_date'] = datetime.now().isoformat()
                    
                    # Update the main dataframe
                    for idx, row in filtered_df.iterrows():
                        tickets_df.loc[tickets_df['ticket_id'] == row['ticket_id']] = row
                    
                    self._save_tickets(tickets_df)
                    st.success(f"✅ Approved {len(filtered_df)} tickets!")
                    st.session_state['confirm_bulk_approve'] = False
                    st.rerun()
                else:
                    st.session_state['confirm_bulk_approve'] = True
                    st.warning("Click again to confirm bulk approval")
        
        with col3:
            reviewer_name = st.text_input("👤 Reviewer Name", value="System User", key="reviewer_name")
        
        # Individual ticket review
        st.markdown("---")
        
        # Pagination
        items_per_page = 5
        total_pages = (len(filtered_df) - 1) // items_per_page + 1
        
        if 'current_page' not in st.session_state:
            st.session_state.current_page = 1
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col1:
            if st.button("⬅️ Previous", disabled=st.session_state.current_page <= 1):
                st.session_state.current_page -= 1
                st.rerun()
        
        with col2:
            st.write(f"Page {st.session_state.current_page} of {total_pages}")
        
        with col3:
            if st.button("➡️ Next", disabled=st.session_state.current_page >= total_pages):
                st.session_state.current_page += 1
                st.rerun()
        
        # Calculate slice for current page
        start_idx = (st.session_state.current_page - 1) * items_per_page
        end_idx = start_idx + items_per_page
        page_df = filtered_df.iloc[start_idx:end_idx]
        
        # Display tickets for review
        for idx, ticket in page_df.iterrows():
            self._render_ticket_review_card(ticket, tickets_df, idx)
        
        # Save updated tickets periodically
        col1, col2 = st.columns([1, 1])
        
        with col1:
            if st.button("💾 Save All Changes", type="primary"):
                self._save_tickets(tickets_df)
                st.success("✅ All changes saved successfully!")
        
        with col2:
            # Quick export of current tickets
            csv_data = tickets_df.to_csv(index=False)
            st.download_button(
                label="📥 Export Tickets CSV",
                data=csv_data,
                file_name=f"reviewed_tickets_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv",
                key="export_reviewed_tickets",
                help="Download tickets with current approval status"
            )
    
    def _render_ticket_review_card(self, ticket, tickets_df, idx):
        """Render individual ticket review card"""
        
        # Status color mapping
        status_colors = {
            'Pending Review': '🟡',
            'Approved': '🟢', 
            'Rejected': '🔴',
            'Needs Changes': '🟠'
        }
        
        status_icon = status_colors.get(ticket['approval_status'], '⚪')
        
        with st.expander(f"{status_icon} {ticket['ticket_id']} - {ticket['title']}", expanded=False):
            # Ticket overview
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.write(f"**Category:** {ticket['category']}")
            with col2:
                st.write(f"**Priority:** {ticket['priority']}")
            with col3:
                st.write(f"**Confidence:** {ticket['confidence_score']:.1f}%")
            with col4:
                st.write(f"**Status:** {ticket['approval_status']}")
            
            # Editable fields
            st.markdown("### ✏️ Editable Fields")
            
            col1, col2 = st.columns(2)
            
            with col1:
                new_title = st.text_input(
                    "Title",
                    value=ticket['title'],
                    key=f"title_{ticket['ticket_id']}"
                )
                
                new_category = st.selectbox(
                    "Category",
                    ["Bug", "Feature Request", "Praise", "Complaint", "Spam"],
                    index=["Bug", "Feature Request", "Praise", "Complaint", "Spam"].index(ticket['category']),
                    key=f"category_{ticket['ticket_id']}"
                )
                
                new_priority = st.selectbox(
                    "Priority", 
                    ["Critical", "High", "Medium", "Low"],
                    index=["Critical", "High", "Medium", "Low"].index(ticket['priority']),
                    key=f"priority_{ticket['ticket_id']}"
                )
            
            with col2:
                new_description = st.text_area(
                    "Description",
                    value=ticket['description'],
                    height=100,
                    key=f"desc_{ticket['ticket_id']}"
                )
                
                new_technical_details = st.text_area(
                    "Technical Details",
                    value=ticket.get('technical_details', ''),
                    height=60,
                    key=f"tech_{ticket['ticket_id']}"
                )
            
            # Review notes
            review_notes = st.text_area(
                "Review Notes",
                value=ticket.get('review_notes', ''),
                placeholder="Add any notes about this ticket review...",
                key=f"notes_{ticket['ticket_id']}"
            )
            
            # Action buttons
            col1, col2, col3, col4, col5 = st.columns(5)
            
            with col1:
                if st.button("✅ Approve", key=f"approve_{ticket['ticket_id']}"):
                    self._update_ticket_status(tickets_df, ticket['ticket_id'], 'Approved', 
                                             new_title, new_category, new_priority, 
                                             new_description, new_technical_details, review_notes)
                    st.success("✅ Ticket approved!")
                    st.rerun()
            
            with col2:
                if st.button("❌ Reject", key=f"reject_{ticket['ticket_id']}"):
                    self._update_ticket_status(tickets_df, ticket['ticket_id'], 'Rejected',
                                             new_title, new_category, new_priority,
                                             new_description, new_technical_details, review_notes)
                    st.error("❌ Ticket rejected!")
                    st.rerun()
            
            with col3:
                if st.button("🔄 Needs Changes", key=f"changes_{ticket['ticket_id']}"):
                    self._update_ticket_status(tickets_df, ticket['ticket_id'], 'Needs Changes',
                                             new_title, new_category, new_priority,
                                             new_description, new_technical_details, review_notes)
                    st.warning("🔄 Ticket marked for changes!")
                    st.rerun()
            
            with col4:
                if st.button("💾 Save Changes", key=f"save_{ticket['ticket_id']}"):
                    self._update_ticket_fields(tickets_df, ticket['ticket_id'], 
                                             new_title, new_category, new_priority,
                                             new_description, new_technical_details, review_notes)
                    st.info("💾 Changes saved!")
                    st.rerun()
            
            with col5:
                if st.button("🗑️ Delete", key=f"delete_{ticket['ticket_id']}"):
                    if st.session_state.get(f'confirm_delete_{ticket["ticket_id"]}', False):
                        self._delete_ticket(tickets_df, ticket['ticket_id'])
                        st.success("🗑️ Ticket deleted!")
                        st.rerun()
                    else:
                        st.session_state[f'confirm_delete_{ticket["ticket_id"]}'] = True
                        st.warning("Click again to confirm deletion")
            
            # Original source data
            if st.checkbox("📋 Show Source Data", key=f"source_{ticket['ticket_id']}"):
                st.json(json.loads(ticket.get('additional_data', '{}')))
    
    def _update_ticket_status(self, tickets_df, ticket_id, new_status, title, category, priority, description, technical_details, review_notes):
        """Update ticket status and fields"""
        mask = tickets_df['ticket_id'] == ticket_id
        tickets_df.loc[mask, 'approval_status'] = new_status
        tickets_df.loc[mask, 'approved_by'] = st.session_state.get('reviewer_name', 'System User')
        tickets_df.loc[mask, 'approval_date'] = datetime.now().isoformat()
        tickets_df.loc[mask, 'review_notes'] = review_notes
        
        # Update fields
        tickets_df.loc[mask, 'title'] = title
        tickets_df.loc[mask, 'category'] = category
        tickets_df.loc[mask, 'priority'] = priority
        tickets_df.loc[mask, 'description'] = description
        tickets_df.loc[mask, 'technical_details'] = technical_details
        
        self._save_tickets(tickets_df)
    
    def _update_ticket_fields(self, tickets_df, ticket_id, title, category, priority, description, technical_details, review_notes):
        """Update ticket fields without changing status"""
        mask = tickets_df['ticket_id'] == ticket_id
        tickets_df.loc[mask, 'title'] = title
        tickets_df.loc[mask, 'category'] = category  
        tickets_df.loc[mask, 'priority'] = priority
        tickets_df.loc[mask, 'description'] = description
        tickets_df.loc[mask, 'technical_details'] = technical_details
        tickets_df.loc[mask, 'review_notes'] = review_notes
        
        self._save_tickets(tickets_df)
    
    def _delete_ticket(self, tickets_df, ticket_id):
        """Delete a ticket from the dataset"""
        tickets_df.drop(tickets_df[tickets_df['ticket_id'] == ticket_id].index, inplace=True)
        self._save_tickets(tickets_df)
    
    def _save_tickets(self, tickets_df):
        """Save tickets dataframe to CSV"""
        try:
            tickets_df.to_csv('generated_tickets.csv', index=False)
        except Exception as e:
            st.error(f"❌ Error saving tickets: {str(e)}")
    
    def show_validation_reports(self):
        """System validation and accuracy reports"""
        st.header("🎯 Validation Reports")
        
        if st.button("🧪 Run System Validation", type="primary"):
            with st.spinner("Running validation..."):
                try:
                    results = self.validator.run_validation()
                    st.success("Validation completed!")
                    
                    # Display results
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("📧 Support Emails", results.get('emails_count', 'N/A'))
                    with col2:
                        st.metric("⭐ App Reviews", results.get('reviews_count', 'N/A'))
                    with col3:
                        st.metric("🎯 Expected Items", results.get('expected_items', 'N/A'))
                        
                except Exception as e:
                    st.error(f"Validation failed: {str(e)}")
        
        # Show validation report if exists
        if os.path.exists('validation_report.md'):
            st.subheader("📄 Latest Validation Report")
            with open('validation_report.md', 'r', encoding='utf-8') as f:
                report_content = f.read()
            st.markdown(report_content)
        else:
            st.info("No validation report available. Run validation to generate a report.")
    
    def check_data_files(self) -> Dict:
        """Check status of data files"""
        status = {
            'emails_count': 0,
            'reviews_count': 0,
            'tickets_count': 0,
            'system_ready': False,
            'has_sample_data': False
        }
        
        if os.path.exists('support_emails.csv'):
            try:
                emails_df = pd.read_csv('support_emails.csv')
                status['emails_count'] = len(emails_df)
                status['has_sample_data'] = True
            except:
                pass
        
        if os.path.exists('app_store_reviews.csv'):
            try:
                reviews_df = pd.read_csv('app_store_reviews.csv')
                status['reviews_count'] = len(reviews_df)
            except:
                pass
        
        if os.path.exists('generated_tickets.csv'):
            try:
                tickets_df = pd.read_csv('generated_tickets.csv')
                status['tickets_count'] = len(tickets_df)
            except:
                pass
        
        status['system_ready'] = status['emails_count'] > 0 or status['reviews_count'] > 0
        
        return status
    
    def run_processing_with_progress(self):
        """Run processing with progress bar"""
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        try:
            status_text.text('🔄 Initializing processing...')
            progress_bar.progress(10)
            time.sleep(1)
            
            status_text.text('📊 Loading data files...')
            progress_bar.progress(30)
            time.sleep(1)
            
            status_text.text('🤖 Running AI analysis...')
            progress_bar.progress(60)
            
            # Run the actual processing
            results = self.analysis_system.process_feedback_simple(
                'app_store_reviews.csv',
                'support_emails.csv'
            )
            
            progress_bar.progress(90)
            status_text.text('💾 Saving results...')
            time.sleep(1)
            
            progress_bar.progress(100)
            status_text.text('✅ Processing completed!')
            
            st.success(f"🎉 Successfully processed {len(results)} feedback items!")
            
        except Exception as e:
            st.error(f"❌ Processing failed: {str(e)}")
            logger.error(f"Processing error: {str(e)}")
    
    def process_sample_data(self):
        """Process existing sample data"""
        try:
            results = self.analysis_system.process_feedback_simple(
                'app_store_reviews.csv',
                'support_emails.csv'
            )
            return results
        except Exception as e:
            logger.error(f"Sample processing error: {str(e)}")
            return None
    
    def run_ticket_generation(self, **kwargs):
        """Run ticket generation with specified parameters"""
        # Check if real-time display should be used
        use_realtime = kwargs.get('enable_colorful_logging', False) and REALTIME_DISPLAY_AVAILABLE
        
        if use_realtime:
            return self.run_ticket_generation_with_realtime(**kwargs)
        else:
            return self.run_ticket_generation_standard(**kwargs)
    
    def run_ticket_generation_with_realtime(self, **kwargs):
        """Run ticket generation with real-time agent interaction display"""
        st.subheader("🤖 Real-time Agent Interactions")
        st.info("Watch the agents work together to process your feedback!")
        
        # Create real-time display containers
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("### 🎭 Agent Activity Feed")
            activity_container = st.empty()
            
        with col2:
            st.markdown("### 📊 Processing Statistics")
            stats_container = st.empty()
            
        # Progress and status
        progress_container = st.container()
        with progress_container:
            overall_progress = st.progress(0)
            status_text = st.empty()
            
        # Reset real-time logger
        if realtime_logger:
            realtime_logger.reset()
            
        try:
            # Initialize
            if realtime_logger:
                realtime_logger.log_phase_change("Initializing system")
                
            status_text.text('🔄 Initializing ticket generation...')
            overall_progress.progress(5)
            
            # Prepare files
            files_to_process = []
            if kwargs.get('use_reviews') and os.path.exists('app_store_reviews.csv'):
                files_to_process.append('app_store_reviews.csv')
            if kwargs.get('use_emails') and os.path.exists('support_emails.csv'):
                files_to_process.append('support_emails.csv')
                
            if not files_to_process:
                st.error("No valid data files selected for processing!")
                return
                
            if realtime_logger:
                realtime_logger.log_phase_change("Loading data files")
                
            status_text.text('📊 Loading and filtering data...')
            overall_progress.progress(15)
            
            # Start processing with real-time updates
            processing_mode = kwargs.get('processing_mode', 'Simple (Fast)')
            
            # Create a thread to update the display
            update_thread = threading.Thread(target=self.update_realtime_display, 
                                            args=(activity_container, stats_container))
            update_thread.daemon = True
            update_thread.start()
            
            if realtime_logger:
                realtime_logger.log_phase_change("Running multi-agent analysis")
                
            status_text.text('🤖 Running AI analysis with real-time agent interactions...')
            overall_progress.progress(30)
            
            # Choose processing method
            if processing_mode == "Full CrewAI (Needs LLM)":
                if realtime_logger:
                    realtime_logger.log_phase_change("Full CrewAI pipeline with LLM")
                results = self.analysis_system.process_feedback(
                    'app_store_reviews.csv' if kwargs.get('use_reviews') else None,
                    'support_emails.csv' if kwargs.get('use_emails') else None
                )
            elif processing_mode == "Hybrid Agents (Recommended)":
                if realtime_logger:
                    realtime_logger.log_phase_change("Hybrid agent pipeline")
                results = self.analysis_system.process_feedback_hybrid(
                    'app_store_reviews.csv' if kwargs.get('use_reviews') else None,
                    'support_emails.csv' if kwargs.get('use_emails') else None
                )
            else:
                if realtime_logger:
                    realtime_logger.log_phase_change("Simple processing")
                results = self.analysis_system.process_feedback_simple(
                    'app_store_reviews.csv' if kwargs.get('use_reviews') else None,
                    'support_emails.csv' if kwargs.get('use_emails') else None
                )
                
            overall_progress.progress(80)
            
            if realtime_logger:
                realtime_logger.log_phase_change("Applying filters and saving results")
                
            status_text.text('🔍 Applying filters and generating final tickets...')
            
            # Apply filters and save results
            if results:
                filtered_results = self.apply_ticket_filters(
                    results,
                    kwargs.get('min_confidence', 0),
                    kwargs.get('priority_filter', []),
                    kwargs.get('category_filter', [])
                )
                
                if kwargs.get('ticket_prefix') != 'TICKET':
                    for result in filtered_results:
                        result['ticket_id'] = result['ticket_id'].replace('TICKET', kwargs.get('ticket_prefix'))
                        
                self.save_tickets_in_format(filtered_results, kwargs.get('output_format', 'CSV'))
                
                overall_progress.progress(100)
                
                if realtime_logger:
                    realtime_logger.log_phase_change("Processing completed")
                
                status_text.text('✅ Ticket generation completed!')
                
                # Final update of displays
                time.sleep(1)  # Allow final updates to show
                
                # Success message with stats
                col1_success, col2_success, col3_success = st.columns(3)
                
                with col1_success:
                    critical_count = sum(1 for r in filtered_results if r.get('priority') == 'Critical')
                    st.metric("🚨 Critical Issues", critical_count)
                    
                with col2_success:
                    avg_confidence = sum(r.get('confidence_score', 0) for r in filtered_results) / len(filtered_results)
                    st.metric("🎯 Avg Confidence", f"{avg_confidence:.1f}%")
                    
                with col3_success:
                    bug_count = sum(1 for r in filtered_results if r.get('category') == 'Bug')
                    st.metric("🐛 Bug Reports", bug_count)
                    
                st.success(f"🎉 Successfully generated {len(filtered_results)} tickets with real-time agent monitoring!")
                st.info(f"📁 Tickets saved in {kwargs.get('output_format', 'CSV')} format")
                
                return filtered_results
            else:
                st.error("❌ No results generated from processing")
                return None
                
        except Exception as e:
            st.error(f"❌ Ticket generation failed: {str(e)}")
            if realtime_logger:
                realtime_logger.log_phase_change(f"Error: {str(e)}")
            logger.error(f"Ticket generation error: {str(e)}")
            return None
    
    def update_realtime_display(self, activity_container, stats_container):
        """Update real-time display containers"""
        while True:
            try:
                if realtime_logger:
                    # Update activity feed
                    with activity_container:
                        activities = realtime_logger.get_recent_activities(15)
                        if activities:
                            activity_html = self.generate_activity_html(activities)
                            st.markdown(activity_html, unsafe_allow_html=True)
                        else:
                            st.info("🤖 Waiting for agent activity...")
                    
                    # Update stats
                    with stats_container:
                        stats = realtime_logger.get_stats()
                        self.display_processing_stats(stats)
                
                time.sleep(0.5)  # Update every 500ms
                
            except Exception as e:
                # If containers are no longer valid, stop updating
                break
                
    def generate_activity_html(self, activities):
        """Generate HTML for activity display"""
        html_content = '<div style="max-height: 400px; overflow-y: auto; font-family: monospace;">'
        
        for activity in reversed(activities[-10:]):  # Show last 10 activities
            timestamp = activity['timestamp']
            message = activity['message']
            color = activity.get('color', '#CCCCCC')
            agent = activity.get('agent', 'System')
            
            if activity['type'] == 'agent_start':
                html_content += f'''
                <div style="border-left: 4px solid {color}; padding: 8px; margin: 4px 0; background: rgba(255,255,255,0.1); border-radius: 4px;">
                    <span style="color: {color}; font-weight: bold;">[{timestamp}]</span><br>
                    <span style="color: white;">{message}</span>
                </div>
                '''
            elif activity['type'] == 'agent_complete':
                html_content += f'''
                <div style="border-left: 4px solid {color}; padding: 8px; margin: 4px 0; background: rgba(0,255,0,0.1); border-radius: 4px;">
                    <span style="color: {color}; font-weight: bold;">[{timestamp}]</span><br>
                    <span style="color: #90EE90;">{message}</span>
                </div>
                '''
            elif activity['type'] == 'progress':
                progress = activity.get('progress', 0)
                html_content += f'''
                <div style="border-left: 4px solid #00FF00; padding: 8px; margin: 4px 0; border-radius: 4px;">
                    <span style="color: #00FF00; font-weight: bold;">[{timestamp}]</span><br>
                    <span style="color: #90EE90;">{message}</span>
                    <div style="background: #333; border-radius: 4px; margin-top: 4px;">
                        <div style="background: #00FF00; height: 8px; border-radius: 4px; width: {progress}%;"></div>
                    </div>
                </div>
                '''
            else:
                html_content += f'''
                <div style="padding: 4px 8px; margin: 2px 0; color: #AAA;">
                    <span style="color: #888;">[{timestamp}]</span> {message}
                </div>
                '''
        
        html_content += '</div>'
        return html_content
        
    def display_processing_stats(self, stats):
        """Display processing statistics"""
        if stats['total_items'] > 0:
            progress = stats['processed_items'] / stats['total_items']
            st.progress(progress)
            st.write(f"**Progress:** {stats['processed_items']}/{stats['total_items']} items")
            
        st.write(f"**Phase:** {stats['current_phase']}")
        
        if stats['agents_used']:
            st.write(f"**Active Agents:** {len(stats['agents_used'])}")
            for agent in sorted(stats['agents_used']):
                st.write(f"• {agent}")
                
        if stats.get('elapsed_time'):
            st.write(f"**Duration:** {stats['elapsed_time']:.1f}s")
            if stats.get('items_per_second', 0) > 0:
                st.write(f"**Speed:** {stats['items_per_second']:.1f} items/sec")
    
    def run_ticket_generation_standard(self, **kwargs):
        """Run ticket generation with standard progress display"""
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        try:
            status_text.text('🔄 Initializing ticket generation...')
            progress_bar.progress(10)
            time.sleep(0.5)
            
            # Prepare file list based on selections
            files_to_process = []
            if kwargs.get('use_reviews') and os.path.exists('app_store_reviews.csv'):
                files_to_process.append('app_store_reviews.csv')
            if kwargs.get('use_emails') and os.path.exists('support_emails.csv'):
                files_to_process.append('support_emails.csv')
            
            if not files_to_process:
                st.error("No valid data files selected for processing!")
                return
            
            status_text.text('📊 Loading and filtering data...')
            progress_bar.progress(30)
            time.sleep(0.5)
            
            status_text.text('🤖 Running AI analysis with colorful logging...')
            progress_bar.progress(60)
            
            if kwargs.get('enable_colorful_logging'):
                st.info("🎨 Check your console for colorful logging output!")
            
            # Choose processing method based on settings
            processing_mode = kwargs.get('processing_mode', 'Simple (Fast)')
            
            if processing_mode == "Full CrewAI (Needs LLM)":
                st.info("🤖 Using full CrewAI multi-agent pipeline with LLM backend!")
                # Run the full CrewAI pipeline
                results = self.analysis_system.process_feedback(
                    'app_store_reviews.csv' if kwargs.get('use_reviews') else None,
                    'support_emails.csv' if kwargs.get('use_emails') else None
                )
                
            elif processing_mode == "Hybrid Agents (Recommended)":
                st.info("🔄 Using hybrid agent pipeline - all agents with colorful logging!")
                # Run the hybrid pipeline
                results = self.analysis_system.process_feedback_hybrid(
                    'app_store_reviews.csv' if kwargs.get('use_reviews') else None,
                    'support_emails.csv' if kwargs.get('use_emails') else None
                )
                
            else:  # Simple (Fast)
                st.info("⚡ Using simple processing for fast results")
                # Run the simplified processing
                results = self.analysis_system.process_feedback_simple(
                    'app_store_reviews.csv' if kwargs.get('use_reviews') else None,
                    'support_emails.csv' if kwargs.get('use_emails') else None
                )
            
            progress_bar.progress(80)
            status_text.text('🔍 Applying filters and generating final tickets...')
            
            # Apply filters
            if results:
                filtered_results = self.apply_ticket_filters(
                    results, 
                    kwargs.get('min_confidence', 0),
                    kwargs.get('priority_filter', []),
                    kwargs.get('category_filter', [])
                )
                
                # Update ticket IDs if custom prefix provided
                if kwargs.get('ticket_prefix') != 'TICKET':
                    for result in filtered_results:
                        result['ticket_id'] = result['ticket_id'].replace('TICKET', kwargs.get('ticket_prefix'))
                
                # Save in requested format
                self.save_tickets_in_format(filtered_results, kwargs.get('output_format', 'CSV'))
                
                progress_bar.progress(100)
                status_text.text('✅ Ticket generation completed!')
                
                st.success(f"🎉 Successfully generated {len(filtered_results)} tickets!")
                st.info(f"📁 Tickets saved in {kwargs.get('output_format', 'CSV')} format")
                
                # Show quick stats
                col1, col2, col3 = st.columns(3)
                with col1:
                    critical_count = sum(1 for r in filtered_results if r.get('priority') == 'Critical')
                    st.metric("Critical Issues", critical_count)
                with col2:
                    avg_confidence = sum(r.get('confidence_score', 0) for r in filtered_results) / len(filtered_results)
                    st.metric("Avg Confidence", f"{avg_confidence:.1f}%")
                with col3:
                    bug_count = sum(1 for r in filtered_results if r.get('category') == 'Bug')
                    st.metric("Bug Reports", bug_count)
            else:
                st.error("❌ No results generated from processing")
                
        except Exception as e:
            st.error(f"❌ Ticket generation failed: {str(e)}")
            logger.error(f"Ticket generation error: {str(e)}")
    
    def preview_ticket_settings(self, use_reviews, use_emails, category_filter, priority_filter):
        """Preview current ticket generation settings"""
        st.subheader("🔍 Preview: Ticket Generation Settings")
        
        # Data sources preview
        col1, col2 = st.columns(2)
        with col1:
            st.write("**Data Sources:**")
            if use_reviews:
                try:
                    reviews_df = pd.read_csv('app_store_reviews.csv')
                    st.write(f"✅ App Store Reviews: {len(reviews_df)} items")
                except:
                    st.write("❌ App Store Reviews: File error")
            else:
                st.write("➖ App Store Reviews: Not selected")
                
            if use_emails:
                try:
                    emails_df = pd.read_csv('support_emails.csv')
                    st.write(f"✅ Support Emails: {len(emails_df)} items")
                except:
                    st.write("❌ Support Emails: File error")
            else:
                st.write("➖ Support Emails: Not selected")
        
        with col2:
            st.write("**Filters:**")
            st.write(f"📊 Categories: {', '.join(category_filter) if category_filter else 'None selected'}")
            st.write(f"⚡ Priorities: {', '.join(priority_filter) if priority_filter else 'None selected'}")
            
            # Estimate potential ticket count
            total_items = 0
            if use_reviews and os.path.exists('app_store_reviews.csv'):
                try:
                    total_items += len(pd.read_csv('app_store_reviews.csv'))
                except:
                    pass
            if use_emails and os.path.exists('support_emails.csv'):
                try:
                    total_items += len(pd.read_csv('support_emails.csv'))
                except:
                    pass
            
            st.write(f"📈 Estimated Input: ~{total_items} items")
            
            # Rough estimate based on typical filtering
            if category_filter and priority_filter:
                estimated_output = int(total_items * 0.7)  # Rough estimate
                st.write(f"🎯 Estimated Output: ~{estimated_output} tickets")
    
    def apply_ticket_filters(self, results, min_confidence, priority_filter, category_filter):
        """Apply filters to ticket results"""
        filtered_results = []
        
        for result in results:
            # Confidence filter
            if result.get('confidence_score', 0) < min_confidence:
                continue
                
            # Priority filter
            if priority_filter and result.get('priority') not in priority_filter:
                continue
                
            # Category filter
            if category_filter and result.get('category') not in category_filter:
                continue
                
            filtered_results.append(result)
        
        return filtered_results
    
    def save_tickets_in_format(self, results, format_type):
        """Save tickets in the specified format"""
        df = pd.DataFrame(results)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        if format_type.upper() == 'CSV':
            filename = f'generated_tickets_{timestamp}.csv'
            df.to_csv(filename, index=False, encoding='utf-8')
        elif format_type.upper() == 'JSON':
            filename = f'generated_tickets_{timestamp}.json'
            df.to_json(filename, orient='records', indent=2)
        elif format_type.upper() == 'EXCEL':
            filename = f'generated_tickets_{timestamp}.xlsx'
            df.to_excel(filename, index=False)
        
        # Also save as the default name for compatibility
        df.to_csv('generated_tickets.csv', index=False, encoding='utf-8')
        
        logger.info(f"Tickets saved as {filename}")
    
    def _fix_csv_format(self):
        """Fix mixed CSV format issues in processing logs and tickets"""
        try:
            st.info("🔧 Attempting to fix CSV format issues...")
            
            # Fix processing_log.csv format issues
            processing_log_path = "processing_log.csv"
            if os.path.exists(processing_log_path):
                with st.spinner("Fixing processing log format..."):
                    self._standardize_processing_log()
                    st.success("✅ Processing log format fixed")
            
            # Fix generated_tickets.csv format issues
            tickets_path = "generated_tickets.csv"
            if os.path.exists(tickets_path):
                with st.spinner("Fixing tickets format..."):
                    self._standardize_tickets_csv()
                    st.success("✅ Tickets format fixed")
                    
            st.success("🎉 CSV format fixes completed! Please try loading again.")
            
        except Exception as e:
            st.error(f"❌ Error during CSV format fix: {str(e)}")
            logger.error(f"CSV format fix error: {str(e)}")
    
    def _standardize_processing_log(self):
        """Standardize processing log CSV format"""
        backup_file = "processing_log_backup.csv"
        log_file = "processing_log.csv"
        
        # Create backup
        if os.path.exists(log_file):
            import shutil
            shutil.copy2(log_file, backup_file)
        
        # Read the file line by line to handle mixed formats
        standardized_rows = []
        simple_headers = ['source_id', 'source_type', 'category', 'confidence', 'processing_time', 'status']
        
        with open(log_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # Process each line
        for i, line in enumerate(lines):
            line = line.strip()
            if not line:
                continue
                
            fields = line.split(',')
            
            if i == 0:  # Header line
                standardized_rows.append(','.join(simple_headers))
            else:
                # Handle different formats
                if len(fields) == 6:
                    # Simple format - use as is
                    standardized_rows.append(line)
                elif len(fields) > 6:
                    # Complex format - extract relevant fields
                    if len(fields) >= 15:  # Detailed format
                        # Try to extract the basic fields we need
                        try:
                            # For session summary lines, skip or convert
                            if 'SESSION_SUMMARY' in line:
                                continue  # Skip session summary lines for now
                            else:
                                # Extract basic fields (adjust indices as needed)
                                source_id = fields[1] if len(fields) > 1 else 'UNKNOWN'
                                source_type = fields[2] if len(fields) > 2 else 'unknown'
                                category = fields[6] if len(fields) > 6 else 'Uncertain'
                                confidence = fields[9] if len(fields) > 9 else '0.0'
                                processing_time = fields[0] if len(fields) > 0 else '2025-09-26T00:00:00'
                                status = 'Processed'
                                
                                row = f"{source_id},{source_type},{category},{confidence},{processing_time},{status}"
                                standardized_rows.append(row)
                        except:
                            # If extraction fails, create a default entry
                            row = f"UNKNOWN_{i},unknown,Uncertain,0.0,{fields[0] if fields else '2025-09-26T00:00:00'},Processed"
                            standardized_rows.append(row)
        
        # Write standardized file
        with open(log_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(standardized_rows))
    
    def _standardize_tickets_csv(self):
        """Standardize tickets CSV format and fix encoding issues"""
        tickets_file = "generated_tickets.csv"
        backup_file = "generated_tickets_backup.csv"
        
        if not os.path.exists(tickets_file):
            return
        
        # Create backup
        import shutil
        shutil.copy2(tickets_file, backup_file)
        
        try:
            # Try to read with different encodings
            for encoding in ['utf-8', 'latin-1', 'cp1252']:
                try:
                    df = pd.read_csv(tickets_file, encoding=encoding)
                    break
                except UnicodeDecodeError:
                    continue
            else:
                raise Exception("Could not read CSV with any encoding")
            
            # Ensure required columns exist
            required_columns = [
                'ticket_id', 'source_id', 'source_type', 'category', 'priority',
                'title', 'description', 'technical_details', 'confidence_score',
                'created_date', 'status', 'additional_data'
            ]
            
            for col in required_columns:
                if col not in df.columns:
                    df[col] = '' if col in ['technical_details', 'additional_data', 'title', 'description'] else 'Unknown'
            
            # Add approval workflow columns if missing
            approval_columns = [
                'approval_status', 'approved_by', 'approval_date', 'review_notes',
                'bug_severity', 'reproduction_steps', 'bug_priority', 'quality_score',
                'quality_issues', 'review_status', 'feature_impact', 'feature_complexity', 'user_benefit'
            ]
            
            for col in approval_columns:
                if col not in df.columns:
                    if col == 'approval_status':
                        df[col] = 'approved'  # Default existing tickets as approved
                    elif col == 'quality_score':
                        df[col] = 100
                    elif col == 'quality_issues':
                        df[col] = '[]'
                    elif col == 'review_status':
                        df[col] = 'approved'
                    else:
                        df[col] = ''
            
            # Save with UTF-8 encoding
            df.to_csv(tickets_file, index=False, encoding='utf-8')
            
        except Exception as e:
            # If all else fails, restore from backup
            if os.path.exists(backup_file):
                shutil.copy2(backup_file, tickets_file)
            raise e
    
    def _validate_csv_format(self, file_path: str, expected_columns: list) -> tuple[bool, str]:
        """Validate CSV format and return status"""
        try:
            # Try reading with pandas
            df = pd.read_csv(file_path)
            
            # Check if all expected columns exist
            missing_columns = set(expected_columns) - set(df.columns)
            if missing_columns:
                return False, f"Missing columns: {missing_columns}"
            
            # Check for empty DataFrame
            if df.empty:
                return False, "CSV file is empty"
            
            # Basic format validation passed
            return True, "CSV format is valid"
            
        except pd.errors.ParserError as e:
            return False, f"CSV parsing error: {str(e)}"
        except Exception as e:
            return False, f"Validation error: {str(e)}"
    
    def _create_export_package(self):
        """Create and download a ZIP package with all CSV files"""
        import zipfile
        import io
        from datetime import datetime
        
        try:
            # Create a bytes buffer for the ZIP file
            zip_buffer = io.BytesIO()
            
            # Create ZIP file
            with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
                # Add each CSV file if it exists
                files_to_zip = [
                    ('generated_tickets.csv', 'tickets.csv'),
                    ('processing_log.csv', 'processing_log.csv'),
                    ('metrics.csv', 'metrics.csv'),
                    ('app_store_reviews.csv', 'source_reviews.csv'),
                    ('support_emails.csv', 'source_emails.csv')
                ]
                
                files_added = 0
                for source_file, zip_name in files_to_zip:
                    if os.path.exists(source_file):
                        zip_file.write(source_file, zip_name)
                        files_added += 1
                
                # Add a summary file
                summary_content = f"""Data Export Summary
Generated: {datetime.now().isoformat()}
Files included: {files_added}

File descriptions:
- tickets.csv: Generated tickets with approval workflow
- processing_log.csv: Processing history and decisions  
- metrics.csv: Aggregated statistics
- source_reviews.csv: Original app store reviews (if available)
- source_emails.csv: Original support emails (if available)

Total files: {files_added}
"""
                zip_file.writestr("README.txt", summary_content)
            
            # Prepare download
            zip_buffer.seek(0)
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            
            st.download_button(
                label="📦 Download Data Package",
                data=zip_buffer.getvalue(),
                file_name=f"feedback_analysis_data_{timestamp}.zip",
                mime="application/zip",
                key="download_zip_package"
            )
            
            st.success(f"✅ ZIP package ready with {files_added} CSV files + README")
            
        except Exception as e:
            st.error(f"❌ Error creating export package: {str(e)}")

def main():
    """Main function to run the Streamlit app"""
    try:
        ui = FeedbackAnalysisUI()
        ui.run_app()
    except Exception as e:
        st.error(f"Application error: {str(e)}")
        logger.error(f"App error: {str(e)}")

if __name__ == "__main__":
    main()