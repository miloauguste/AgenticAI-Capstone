import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json
import os
from datetime import datetime
import logging

# Import our multi-agent system
from multi_agent_system import FeedbackAnalysisSystem

# Configure page
st.set_page_config(
    page_title="Intelligent Feedback Analysis System",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'system' not in st.session_state:
    st.session_state.system = FeedbackAnalysisSystem()
if 'processed_data' not in st.session_state:
    st.session_state.processed_data = None
if 'processing_complete' not in st.session_state:
    st.session_state.processing_complete = False

def load_data():
    """Load existing CSV files if they exist"""
    data = {}
    try:
        if os.path.exists('app_store_reviews.csv'):
            data['app_reviews'] = pd.read_csv('app_store_reviews.csv')
        if os.path.exists('support_emails.csv'):
            data['support_emails'] = pd.read_csv('support_emails.csv')
        if os.path.exists('generated_tickets.csv'):
            data['generated_tickets'] = pd.read_csv('generated_tickets.csv')
        if os.path.exists('processing_log.csv'):
            data['processing_log'] = pd.read_csv('processing_log.csv')
        if os.path.exists('metrics.csv'):
            data['metrics'] = pd.read_csv('metrics.csv')
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
    return data

def create_dashboard():
    """Main dashboard view"""
    st.title("🤖 Intelligent Feedback Analysis System")
    st.markdown("### Multi-Agent AI System for User Feedback Processing")
    
    # Load data
    data = load_data()
    
    # Sidebar configuration
    st.sidebar.title("System Configuration")
    
    # File upload section
    st.sidebar.subheader("📁 Data Input")
    uploaded_reviews = st.sidebar.file_uploader(
        "Upload App Store Reviews CSV", 
        type=['csv'],
        key="reviews_upload"
    )
    uploaded_emails = st.sidebar.file_uploader(
        "Upload Support Emails CSV", 
        type=['csv'],
        key="emails_upload"
    )
    
    # Processing controls
    st.sidebar.subheader("🔧 Processing Controls")
    
    confidence_threshold = st.sidebar.slider(
        "Classification Confidence Threshold", 
        0.0, 1.0, 0.5, 0.1
    )
    
    priority_override = st.sidebar.selectbox(
        "Priority Override for Critical Issues",
        ["None", "High", "Critical"]
    )
    
    auto_process = st.sidebar.checkbox("Auto-process uploaded files", value=True)
    
    # Process button
    process_button = st.sidebar.button(
        "🚀 Process Feedback", 
        type="primary",
        disabled=not (os.path.exists('app_store_reviews.csv') and os.path.exists('support_emails.csv'))
    )
    
    # Handle file uploads
    if uploaded_reviews is not None:
        reviews_df = pd.read_csv(uploaded_reviews)
        reviews_df.to_csv('app_store_reviews.csv', index=False)
        st.sidebar.success(f"✅ Uploaded {len(reviews_df)} app reviews")
        
    if uploaded_emails is not None:
        emails_df = pd.read_csv(uploaded_emails)
        emails_df.to_csv('support_emails.csv', index=False)
        st.sidebar.success(f"✅ Uploaded {len(emails_df)} support emails")
    
    # Process feedback
    if process_button:
        with st.spinner("🔄 Processing feedback with multi-agent system..."):
            try:
                results = st.session_state.system.process_feedback_simple(
                    'app_store_reviews.csv',
                    'support_emails.csv'
                )
                st.session_state.processed_data = results
                st.session_state.processing_complete = True
                st.success(f"✅ Successfully processed {len(results)} feedback items!")
                st.rerun()
            except Exception as e:
                st.error(f"❌ Processing failed: {str(e)}")
    
    # Main content area
    col1, col2, col3 = st.columns([2, 2, 1])
    
    # Summary metrics
    if 'generated_tickets' in data and not data['generated_tickets'].empty:
        tickets_df = data['generated_tickets']
        
        with col1:
            st.metric("Total Tickets", len(tickets_df))
        with col2:
            avg_confidence = tickets_df['confidence_score'].mean()
            st.metric("Avg Confidence", f"{avg_confidence:.1f}%")
        with col3:
            open_tickets = len(tickets_df[tickets_df['status'] == 'Open'])
            st.metric("Open Tickets", open_tickets)
    
    # Create tabs for different views
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Dashboard", "🎫 Tickets", "📈 Analytics", "⚙️ Manual Override", "📋 Logs"
    ])
    
    with tab1:
        show_dashboard_tab(data)
    
    with tab2:
        show_tickets_tab(data)
    
    with tab3:
        show_analytics_tab(data)
    
    with tab4:
        show_manual_override_tab(data)
    
    with tab5:
        show_logs_tab(data)

def show_dashboard_tab(data):
    """Dashboard overview tab"""
    st.subheader("📊 System Overview")
    
    if 'generated_tickets' not in data or data['generated_tickets'].empty:
        st.info("🔄 No processed data available. Please upload files and process feedback.")
        
        # Show sample data structure
        st.subheader("📋 Expected Data Format")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**App Store Reviews CSV:**")
            sample_reviews = pd.DataFrame({
                'review_id': ['REV001', 'REV002'],
                'platform': ['Google Play', 'App Store'],
                'rating': [1, 5],
                'review_text': ['App crashes when...', 'Amazing app!'],
                'user_name': ['user123', 'happyuser'],
                'date': ['2024-01-15', '2024-01-14'],
                'app_version': ['2.1.3', '2.1.2']
            })
            st.dataframe(sample_reviews)
        
        with col2:
            st.markdown("**Support Emails CSV:**")
            sample_emails = pd.DataFrame({
                'email_id': ['EMAIL001', 'EMAIL002'],
                'subject': ['App Crash Report', 'Feature Request'],
                'body': ['App crashes when I try to...', 'Please add dark mode...'],
                'sender_email': ['user1@email.com', 'user2@email.com'],
                'timestamp': ['2024-01-15 09:30:00', '2024-01-14 14:15:00'],
                'priority': ['High', 'Low']
            })
            st.dataframe(sample_emails)
        return
    
    tickets_df = data['generated_tickets']
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_tickets = len(tickets_df)
        st.metric("🎫 Total Tickets", total_tickets)
    
    with col2:
        bug_tickets = len(tickets_df[tickets_df['category'] == 'Bug'])
        st.metric("🐛 Bug Reports", bug_tickets)
    
    with col3:
        feature_tickets = len(tickets_df[tickets_df['category'] == 'Feature Request'])
        st.metric("✨ Feature Requests", feature_tickets)
    
    with col4:
        critical_tickets = len(tickets_df[tickets_df['priority'] == 'Critical'])
        st.metric("🚨 Critical Issues", critical_tickets)
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        # Category distribution
        category_counts = tickets_df['category'].value_counts()
        fig_cat = px.pie(
            values=category_counts.values,
            names=category_counts.index,
            title="📊 Feedback Categories",
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        st.plotly_chart(fig_cat, use_container_width=True)
    
    with col2:
        # Priority distribution
        priority_counts = tickets_df['priority'].value_counts()
        fig_pri = px.bar(
            x=priority_counts.index,
            y=priority_counts.values,
            title="⚡ Priority Distribution",
            color=priority_counts.values,
            color_continuous_scale="Reds"
        )
        fig_pri.update_layout(xaxis_title="Priority", yaxis_title="Count")
        st.plotly_chart(fig_pri, use_container_width=True)

def show_tickets_tab(data):
    """Tickets management tab"""
    st.subheader("🎫 Generated Tickets")
    
    if 'generated_tickets' not in data or data['generated_tickets'].empty:
        st.info("No tickets generated yet. Please process feedback first.")
        return
    
    tickets_df = data['generated_tickets']
    
    # Filters
    col1, col2, col3 = st.columns(3)
    
    with col1:
        category_filter = st.selectbox(
            "Filter by Category",
            ["All"] + list(tickets_df['category'].unique())
        )
    
    with col2:
        priority_filter = st.selectbox(
            "Filter by Priority", 
            ["All"] + list(tickets_df['priority'].unique())
        )
    
    with col3:
        status_filter = st.selectbox(
            "Filter by Status",
            ["All"] + list(tickets_df['status'].unique())
        )
    
    # Apply filters
    filtered_df = tickets_df.copy()
    if category_filter != "All":
        filtered_df = filtered_df[filtered_df['category'] == category_filter]
    if priority_filter != "All":
        filtered_df = filtered_df[filtered_df['priority'] == priority_filter]
    if status_filter != "All":
        filtered_df = filtered_df[filtered_df['status'] == status_filter]
    
    # Display tickets
    st.dataframe(
        filtered_df[['ticket_id', 'category', 'priority', 'title', 'confidence_score', 'status']],
        use_container_width=True
    )
    
    # Ticket details
    if not filtered_df.empty:
        st.subheader("🔍 Ticket Details")
        selected_ticket = st.selectbox(
            "Select ticket to view details",
            filtered_df['ticket_id'].tolist()
        )
        
        if selected_ticket:
            ticket_data = filtered_df[filtered_df['ticket_id'] == selected_ticket].iloc[0]
            
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown(f"**Title:** {ticket_data['title']}")
                st.markdown(f"**Description:** {ticket_data['description']}")
                st.markdown(f"**Technical Details:** {ticket_data['technical_details']}")
            
            with col2:
                st.markdown(f"**Category:** {ticket_data['category']}")
                st.markdown(f"**Priority:** {ticket_data['priority']}")
                st.markdown(f"**Confidence:** {ticket_data['confidence_score']:.1f}%")
                st.markdown(f"**Status:** {ticket_data['status']}")
                st.markdown(f"**Created:** {ticket_data['created_date']}")

def show_analytics_tab(data):
    """Analytics and insights tab"""
    st.subheader("📈 Analytics & Insights")
    
    if 'generated_tickets' not in data or data['generated_tickets'].empty:
        st.info("No analytics data available. Please process feedback first.")
        return
    
    tickets_df = data['generated_tickets']
    
    # Confidence score analysis
    st.subheader("🎯 Classification Confidence Analysis")
    
    fig_conf = px.histogram(
        tickets_df,
        x='confidence_score',
        nbins=20,
        title="Distribution of Classification Confidence Scores",
        color_discrete_sequence=['#1f77b4']
    )
    fig_conf.update_layout(xaxis_title="Confidence Score (%)", yaxis_title="Count")
    st.plotly_chart(fig_conf, use_container_width=True)
    
    # Source type analysis
    col1, col2 = st.columns(2)
    
    with col1:
        source_counts = tickets_df['source_type'].value_counts()
        fig_source = px.bar(
            x=source_counts.index,
            y=source_counts.values,
            title="📱 Feedback Sources",
            color=source_counts.values,
            color_continuous_scale="Blues"
        )
        st.plotly_chart(fig_source, use_container_width=True)
    
    with col2:
        # Category vs Priority heatmap
        heatmap_data = pd.crosstab(tickets_df['category'], tickets_df['priority'])
        fig_heatmap = px.imshow(
            heatmap_data,
            title="🌡️ Category vs Priority Heatmap",
            color_continuous_scale="YlOrRd",
            aspect="auto"
        )
        st.plotly_chart(fig_heatmap, use_container_width=True)
    
    # Performance metrics
    st.subheader("⚡ System Performance")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        avg_confidence = tickets_df['confidence_score'].mean()
        st.metric("Avg Confidence", f"{avg_confidence:.1f}%")
    
    with col2:
        high_confidence = len(tickets_df[tickets_df['confidence_score'] > 70])
        st.metric("High Confidence (>70%)", high_confidence)
    
    with col3:
        low_confidence = len(tickets_df[tickets_df['confidence_score'] < 50])
        st.metric("Low Confidence (<50%)", low_confidence)
    
    with col4:
        processing_success_rate = (len(tickets_df) / len(tickets_df)) * 100
        st.metric("Processing Success Rate", f"{processing_success_rate:.1f}%")

def show_manual_override_tab(data):
    """Manual override and editing tab"""
    st.subheader("⚙️ Manual Override & Ticket Editing")
    
    if 'generated_tickets' not in data or data['generated_tickets'].empty:
        st.info("No tickets available for editing. Please process feedback first.")
        return
    
    tickets_df = data['generated_tickets']
    
    st.markdown("Select a ticket to edit:")
    
    # Ticket selection
    ticket_ids = tickets_df['ticket_id'].tolist()
    selected_ticket_id = st.selectbox("Choose ticket:", ticket_ids)
    
    if selected_ticket_id:
        ticket_idx = tickets_df[tickets_df['ticket_id'] == selected_ticket_id].index[0]
        ticket = tickets_df.loc[ticket_idx]
        
        # Editable fields
        col1, col2 = st.columns(2)
        
        with col1:
            new_category = st.selectbox(
                "Category:",
                ["Bug", "Feature Request", "Praise", "Complaint", "Spam"],
                index=["Bug", "Feature Request", "Praise", "Complaint", "Spam"].index(ticket['category'])
            )
            
            new_priority = st.selectbox(
                "Priority:",
                ["Critical", "High", "Medium", "Low"],
                index=["Critical", "High", "Medium", "Low"].index(ticket['priority'])
            )
            
            new_status = st.selectbox(
                "Status:",
                ["Open", "In Progress", "Resolved", "Closed"],
                index=["Open", "In Progress", "Resolved", "Closed"].index(ticket['status'])
            )
        
        with col2:
            new_title = st.text_input("Title:", value=ticket['title'])
            new_technical_details = st.text_area(
                "Technical Details:", 
                value=ticket['technical_details']
            )
        
        new_description = st.text_area("Description:", value=ticket['description'])
        
        # Update button
        if st.button("💾 Update Ticket", type="primary"):
            # Update the ticket
            tickets_df.loc[ticket_idx, 'category'] = new_category
            tickets_df.loc[ticket_idx, 'priority'] = new_priority
            tickets_df.loc[ticket_idx, 'status'] = new_status
            tickets_df.loc[ticket_idx, 'title'] = new_title
            tickets_df.loc[ticket_idx, 'description'] = new_description
            tickets_df.loc[ticket_idx, 'technical_details'] = new_technical_details
            
            # Save updated data
            tickets_df.to_csv('generated_tickets.csv', index=False)
            st.success("✅ Ticket updated successfully!")
            st.rerun()
    
    # Bulk operations
    st.subheader("🔄 Bulk Operations")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Mark All Spam as Closed"):
            spam_tickets = tickets_df['category'] == 'Spam'
            tickets_df.loc[spam_tickets, 'status'] = 'Closed'
            tickets_df.to_csv('generated_tickets.csv', index=False)
            st.success("All spam tickets marked as closed!")
            st.rerun()
    
    with col2:
        if st.button("Set Critical Bugs to High Priority"):
            critical_bugs = (tickets_df['category'] == 'Bug') & (tickets_df['priority'] == 'Critical')
            tickets_df.loc[critical_bugs, 'priority'] = 'High'
            tickets_df.to_csv('generated_tickets.csv', index=False)
            st.success("Critical bugs updated!")
            st.rerun()

def show_logs_tab(data):
    """Processing logs and system information"""
    st.subheader("📋 System Logs & Processing History")
    
    # Processing log
    if 'processing_log' in data and not data['processing_log'].empty:
        st.subheader("🔄 Processing Log")
        st.dataframe(data['processing_log'], use_container_width=True)
    else:
        st.info("No processing logs available.")
    
    # System metrics
    if 'metrics' in data and not data['metrics'].empty:
        st.subheader("📊 System Metrics")
        metrics = data['metrics'].iloc[-1]  # Latest metrics
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Processed", int(metrics['total_processed']))
        
        with col2:
            st.metric("Average Confidence", f"{float(metrics['avg_confidence']):.1f}%")
        
        with col3:
            st.metric("Processing Date", str(metrics['processing_date'])[:19])
        
        # Category breakdown
        if 'categories' in metrics:
            categories = json.loads(metrics['categories'])
            st.subheader("📈 Category Breakdown")
            for category, count in categories.items():
                st.write(f"**{category}:** {count}")
    
    # System status
    st.subheader("🖥️ System Status")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**File Status:**")
        files_status = {
            'app_store_reviews.csv': os.path.exists('app_store_reviews.csv'),
            'support_emails.csv': os.path.exists('support_emails.csv'),
            'generated_tickets.csv': os.path.exists('generated_tickets.csv'),
            'processing_log.csv': os.path.exists('processing_log.csv'),
            'metrics.csv': os.path.exists('metrics.csv')
        }
        
        for file, exists in files_status.items():
            status = "✅" if exists else "❌"
            st.write(f"{status} {file}")
    
    with col2:
        st.write("**System Information:**")
        st.write(f"**Current Time:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        st.write(f"**Processing Status:** {'✅ Ready' if all(files_status.values()) else '⚠️ Incomplete'}")

# Main app
if __name__ == "__main__":
    create_dashboard()
