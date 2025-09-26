# 🔍 Intelligent Feedback Analysis System - User Interface

A comprehensive web-based interface for the Intelligent Feedback Analysis System built with Streamlit.

## 🚀 Quick Start

### Windows
```bash
run_ui.bat
```

### Linux/Mac
```bash
chmod +x run_ui.sh
./run_ui.sh
```

### Manual Start
```bash
pip install -r requirements.txt
streamlit run ui_app.py
```

## 📊 Features

### 1. Dashboard
- **System Overview**: Real-time metrics and status indicators
- **Quick Stats**: Support emails, app reviews, generated tickets count
- **Recent Activity**: Visual representation of processed feedback
- **Quick Actions**: Refresh dashboard, process sample data

### 2. Upload & Process
- **File Upload**: Drag-and-drop interface for CSV files
- **Data Preview**: Instant preview of uploaded data
- **Processing Control**: Start processing with progress tracking
- **Sample Data**: Use pre-loaded sample data for testing

### 3. Results Analysis
- **Metrics Dashboard**: Total tickets, confidence scores, critical issues
- **Interactive Visualizations**: 
  - Category distribution (pie chart)
  - Priority levels (bar chart)
  - Confidence score distribution (histogram)
- **Filtering**: Filter results by category, priority, and confidence
- **Export**: Download filtered results as CSV

### 4. System Monitoring
- **Real-time Metrics**: Memory usage, processing time, success rate
- **Processing Log**: Historical view of all processing activities
- **Timeline View**: Visual timeline of processing events
- **Auto-refresh**: Optional automatic dashboard updates

### 5. Validation Reports
- **System Validation**: Run comprehensive system validation
- **Accuracy Reports**: View validation results and metrics
- **Report History**: Access historical validation reports

## 📈 Monitoring Capabilities

### Real-time Metrics
- **Performance Monitoring**: Track system performance metrics
- **Success Rate**: Monitor processing success rates
- **Processing Timeline**: Visualize processing activities over time

### Data Quality Monitoring
- **Confidence Scores**: Track AI confidence in classifications
- **Category Distribution**: Monitor feedback category patterns
- **Priority Analysis**: Track priority level distributions

### System Health
- **File Status**: Monitor availability of data files
- **Processing Status**: Track current processing state
- **Error Logging**: Comprehensive error tracking and logging

## 🎯 Key UI Components

### Interactive Elements
- **Progress Bars**: Real-time processing progress
- **Dynamic Charts**: Auto-updating visualizations
- **Filtering Controls**: Interactive data filtering
- **File Upload**: Drag-and-drop file handling

### Navigation
- **Sidebar Navigation**: Easy access to all features
- **Tab-based Layout**: Organized content sections
- **Responsive Design**: Works on desktop and mobile

### Data Visualization
- **Plotly Charts**: Interactive, responsive visualizations
- **Data Tables**: Sortable, filterable data displays
- **Metrics Cards**: Key performance indicators

## 📋 Usage Instructions

### 1. Starting the Application
Run the appropriate startup script for your platform and navigate to `http://localhost:8501`

### 2. Processing Feedback
1. Go to "Upload & Process" page
2. Upload your CSV files or use sample data
3. Click "Start Processing" to begin analysis
4. Monitor progress in real-time

### 3. Viewing Results
1. Navigate to "Results Analysis"
2. View interactive charts and metrics
3. Filter results as needed
4. Export filtered data

### 4. Monitoring System
1. Use "System Monitoring" for real-time metrics
2. Enable auto-refresh for continuous monitoring
3. View processing logs and timelines

### 5. Validation
1. Go to "Validation Reports"
2. Run system validation
3. Review accuracy metrics and reports

## 🔧 Configuration

The UI automatically detects and loads configuration from:
- Environment variables
- Local data files
- System settings

## 📊 Data Requirements

### Support Emails CSV
Required columns:
- `email_id`: Unique identifier
- `subject`: Email subject line
- `body`: Email content
- `sender_email`: Sender's email address
- `timestamp`: Email timestamp

### App Store Reviews CSV
Required columns:
- `review_id`: Unique identifier
- `platform`: App store platform
- `rating`: Star rating
- `review_text`: Review content
- `user_name`: Reviewer name
- `date`: Review date
- `app_version`: App version reviewed

## 🚨 Troubleshooting

### Common Issues
1. **Port 8501 in use**: Change port in startup script
2. **Missing dependencies**: Run `pip install -r requirements.txt`
3. **File encoding errors**: Ensure CSV files are UTF-8 encoded
4. **Memory issues**: Close other applications if processing large datasets

### Performance Tips
- Use filtering to reduce data visualization load
- Enable auto-refresh only when needed
- Process data in smaller batches for large datasets

## 🎨 Customization

The UI can be customized by modifying:
- `ui_app.py`: Main application logic
- Color schemes in Plotly charts
- Layout and styling options
- Metrics and thresholds

## 📝 Logging

All activities are logged with different levels:
- INFO: Normal operations
- WARNING: Non-critical issues
- ERROR: Critical errors
- DEBUG: Detailed debugging information

Logs are displayed in the console and can be configured for file output.