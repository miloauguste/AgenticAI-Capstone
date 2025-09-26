# Google Gemini LLM Integration

The Intelligent Feedback Analysis System now supports Google Gemini as the primary LLM backend!

## 🚀 Quick Setup

1. **Install Dependencies** (already done):
   ```bash
   pip install langchain-google-genai google-generativeai python-dotenv
   ```

2. **Configure API Key**:
   ```bash
   python setup_gemini.py
   ```
   
   Or manually set environment variable:
   ```bash
   export GOOGLE_API_KEY=your_api_key_here
   ```

3. **Run the System**:
   ```bash
   python -m streamlit run ui_app.py
   ```

## 🎯 LLM Priority Order

The system automatically selects LLM backends in this order:

1. **Google Gemini** (if `GOOGLE_API_KEY` is set) - **RECOMMENDED**
2. **OpenAI GPT** (if `OPENAI_API_KEY` is set)
3. **Anthropic Claude** (if `ANTHROPIC_API_KEY` is set)
4. **Hybrid Mode** (no LLM required, still fully functional)

## 📊 Processing Modes Available

### 1. Full CrewAI (Needs LLM) - **Enhanced with Gemini**
- **What it does**: Complete multi-agent pipeline with LLM reasoning
- **Agents used**: All 7 agents with intelligent decision-making
- **Requirements**: Google API Key configured
- **Benefits**: 
  - Advanced context understanding
  - Intelligent classification and prioritization
  - Smart feature extraction
  - Quality assessment with detailed reasoning

### 2. Hybrid Agents (Recommended) - **Always Available**
- **What it does**: All agents with colorful logging, rule-based processing
- **Agents used**: All 7 agents with manual execution
- **Requirements**: None (works without LLM)
- **Benefits**:
  - Full agent pipeline demonstration
  - Colorful logging and progress tracking
  - Reliable and fast processing
  - Perfect for development and testing

### 3. Simple (Fast)
- **What it does**: Basic processing without agent logging
- **Requirements**: None
- **Benefits**: Fastest processing for large datasets

## 🤖 Agents Enhanced by Gemini

When using Google Gemini LLM, these agents get enhanced capabilities:

1. **CSV Reader Agent** - Smart data parsing and validation
2. **Feedback Classifier Agent** - Context-aware classification
3. **Bug Analysis Agent** - Intelligent severity and priority assessment
4. **Feature Extractor Agent** - Smart feature impact evaluation
5. **Priority Analyzer Agent** - Business-context priority decisions
6. **Technical Details Agent** - Advanced technical pattern recognition
7. **Ticket Creator Agent** - Context-rich ticket generation
8. **Quality Reviewer Agent** - Comprehensive quality scoring

## 🔧 Configuration Files

- **`.env`**: Stores your API keys securely
- **`multi_agent_system.py`**: Main system with Gemini integration
- **`setup_gemini.py`**: Interactive setup script
- **`test_gemini.py`**: Test Gemini integration

## 📈 Testing and Verification

### Test System Status:
```bash
python test_gemini.py
```

### Test with Mock Data:
```bash
python test_simple.py
```

### Run UI Application:
```bash
python -m streamlit run ui_app.py
```

## 💡 Key Features with Gemini

- **Intelligent Classification**: More accurate feedback categorization
- **Context-Aware Analysis**: Better understanding of user intent
- **Smart Prioritization**: Business-context priority decisions
- **Advanced Reasoning**: Complex pattern recognition and analysis
- **Quality Assessment**: Detailed quality scoring with explanations
- **Adaptive Processing**: Handles edge cases and ambiguous feedback better

## 🎨 Visual Features

- **Colorful Logging**: Rich console output with agent-specific colors
- **Progress Tracking**: Real-time progress bars and status updates
- **Agent Activity**: Visual representation of agent interactions
- **Error Handling**: Graceful fallback to hybrid mode if LLM fails

## 📋 Usage Examples

### In UI (Streamlit):
1. Go to "Generate Tickets" page
2. Select "Full CrewAI (Needs LLM)" processing mode
3. Configure filters and options
4. Click "Generate Tickets"
5. Watch colorful agent interactions in console

### In Code:
```python
from multi_agent_system import FeedbackAnalysisSystem

# Initialize with Gemini
system = FeedbackAnalysisSystem()

# Process with full agent pipeline
results = system.process_feedback(
    'app_store_reviews.csv',
    'support_emails.csv'
)

# Process mock data for demonstration
mock_results = system.process_mock_data_from_expected_classifications()
```

## 🚨 Troubleshooting

### "Model not found" errors:
- The system uses `gemini-pro` model (stable and widely available)
- Check your Google API key is valid and has Gemini access
- Ensure you have credits/quota available

### System falls back to Hybrid mode:
- API key not set or invalid
- Network connectivity issues
- API quota exceeded
- **This is OK!** Hybrid mode is fully functional

### No colorful logging in console:
- Make sure to run from terminal/command prompt
- Check if `colorful_logger.py` is working
- Windows encoding issues are automatically handled

## 🎯 Recommendations

1. **For Production**: Use "Full CrewAI (Needs LLM)" with Gemini for best results
2. **For Development**: Use "Hybrid Agents (Recommended)" for consistent behavior
3. **For Testing**: Use mock data processing to see all features
4. **For Performance**: Use "Simple (Fast)" for large datasets without analysis

## 📊 Expected Results

With Google Gemini configured, you should see:
- ✅ "Using Google Gemini backend" in logs
- ✅ Enhanced classification accuracy
- ✅ Smarter bug priority assessment
- ✅ Better feature impact evaluation
- ✅ More detailed ticket descriptions
- ✅ Improved quality scoring

The system is now ready to provide intelligent, context-aware feedback analysis powered by Google Gemini! 🚀