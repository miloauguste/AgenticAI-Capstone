#!/usr/bin/env python3
"""
Colorful logging utility for the Intelligent Feedback Analysis System
Provides visually appealing, colored console output for agent interactions
"""

import logging
import sys
import os
from datetime import datetime
from typing import Dict, Any
from enum import Enum
import time

# Configure console encoding for Windows Unicode support
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')
    
    # Set console to UTF-8 mode
    try:
        os.system("chcp 65001 >nul 2>&1")
    except:
        pass

# Color codes for different output types
class Colors:
    # Standard colors
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    GRAY = '\033[90m'
    
    # Bright colors
    BRIGHT_RED = '\033[1;91m'
    BRIGHT_GREEN = '\033[1;92m'
    BRIGHT_YELLOW = '\033[1;93m'
    BRIGHT_BLUE = '\033[1;94m'
    BRIGHT_MAGENTA = '\033[1;95m'
    BRIGHT_CYAN = '\033[1;96m'
    BRIGHT_WHITE = '\033[1;97m'
    
    # Background colors
    BG_RED = '\033[41m'
    BG_GREEN = '\033[42m'
    BG_YELLOW = '\033[43m'
    BG_BLUE = '\033[44m'
    BG_MAGENTA = '\033[45m'
    BG_CYAN = '\033[46m'
    
    # Special formatting
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    ITALIC = '\033[3m'
    RESET = '\033[0m'
    
    # Gradient colors
    ORANGE = '\033[38;5;208m'
    PURPLE = '\033[38;5;135m'
    PINK = '\033[38;5;213m'
    LIME = '\033[38;5;154m'
    TURQUOISE = '\033[38;5;80m'

class LogLevel(Enum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"
    SUCCESS = "SUCCESS"
    AGENT = "AGENT"
    TASK = "TASK"
    CREW = "CREW"

class AgentColors:
    """Color schemes for different agent types"""
    CSV_READER = Colors.BRIGHT_CYAN
    CLASSIFIER = Colors.BRIGHT_GREEN
    BUG_ANALYZER = Colors.BRIGHT_RED
    FEATURE_ANALYZER = Colors.BRIGHT_BLUE
    TICKET_CREATOR = Colors.BRIGHT_YELLOW
    QUALITY_REVIEWER = Colors.BRIGHT_MAGENTA
    SYSTEM = Colors.BRIGHT_WHITE
    DEFAULT = Colors.WHITE

class Symbols:
    """Unicode symbols for different operations with Windows fallbacks"""
    try:
        # Try to use Unicode symbols
        SUCCESS = "✅"
        ERROR = "❌"  
        WARNING = "⚠️"
        INFO = "ℹ️"
        DEBUG = "🐛"
        AGENT = "🤖"
        TASK = "📋"
        CREW = "👥"
        PROCESSING = "⚙️"
        COMPLETED = "🎉"
        STARTED = "🚀"
        THINKING = "🤔"
        WRITING = "📝"
        READING = "📖"
        ANALYZING = "🔍"
        ARROW_RIGHT = "➤"
        BULLET = "•"
        CLOCK = "🕐"
        CHART = "📊"
        FILE = "📄"
        DATABASE = "🗄️"
        NETWORK = "🌐"
        GEAR = "⚙️"
    except UnicodeEncodeError:
        # ASCII fallbacks for Windows
        SUCCESS = "[OK]"
        ERROR = "[ERR]"
        WARNING = "[WARN]"
        INFO = "[INFO]"
        DEBUG = "[DEBUG]"
        AGENT = "[AGENT]"
        TASK = "[TASK]"
        CREW = "[CREW]"
        PROCESSING = "[PROC]"
        COMPLETED = "[DONE]"
        STARTED = "[START]"
        THINKING = "[THINK]"
        WRITING = "[WRITE]"
        READING = "[READ]"
        ANALYZING = "[ANALYZE]"
        ARROW_RIGHT = "->"
        BULLET = "*"
        CLOCK = "[TIME]"
        CHART = "[CHART]"
        FILE = "[FILE]"
        DATABASE = "[DB]"
        NETWORK = "[NET]"
        GEAR = "[GEAR]"

class ColorfulLogger:
    """Enhanced logger with colorful output and agent-specific formatting"""
    
    def __init__(self, name: str = "FeedbackSystem", enable_colors: bool = True):
        self.name = name
        self.enable_colors = enable_colors
        self.start_time = time.time()
        self.agent_counters = {}
        
        # Configure the logger
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        
        # Remove existing handlers
        for handler in self.logger.handlers[:]:
            self.logger.removeHandler(handler)
        
        # Create console handler with custom formatter
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(self.ColoredFormatter(enable_colors=enable_colors))
        self.logger.addHandler(handler)
        
        # Disable propagation to avoid duplicate logs
        self.logger.propagate = False
    
    class ColoredFormatter(logging.Formatter):
        """Custom formatter for colored log messages"""
        
        def __init__(self, enable_colors: bool = True):
            self.enable_colors = enable_colors
            super().__init__()
        
        def format(self, record):
            if not self.enable_colors:
                return f"[{record.levelname}] {record.getMessage()}"
            
            # Color mapping for log levels
            level_colors = {
                'DEBUG': Colors.GRAY,
                'INFO': Colors.WHITE,
                'WARNING': Colors.YELLOW,
                'ERROR': Colors.RED,
                'CRITICAL': Colors.BRIGHT_RED,
                'SUCCESS': Colors.GREEN,
                'AGENT': Colors.CYAN,
                'TASK': Colors.BLUE,
                'CREW': Colors.MAGENTA
            }
            
            color = level_colors.get(record.levelname, Colors.WHITE)
            timestamp = datetime.now().strftime("%H:%M:%S")
            
            formatted_msg = f"{Colors.GRAY}[{timestamp}]{Colors.RESET} {color}[{record.levelname}]{Colors.RESET} {record.getMessage()}"
            return formatted_msg
    
    def _log(self, level: LogLevel, message: str, symbol: str = "", color: str = Colors.WHITE):
        """Internal method to log with color and symbol"""
        if self.enable_colors:
            formatted_message = f"{symbol} {color}{message}{Colors.RESET}"
        else:
            formatted_message = f"{symbol} {message}".strip()
        
        # Map custom levels to standard logging levels
        level_mapping = {
            LogLevel.DEBUG: logging.DEBUG,
            LogLevel.INFO: logging.INFO,
            LogLevel.WARNING: logging.WARNING,
            LogLevel.ERROR: logging.ERROR,
            LogLevel.CRITICAL: logging.CRITICAL,
            LogLevel.SUCCESS: logging.INFO,
            LogLevel.AGENT: logging.INFO,
            LogLevel.TASK: logging.INFO,
            LogLevel.CREW: logging.INFO
        }
        
        self.logger.log(level_mapping[level], formatted_message)
    
    def debug(self, message: str):
        """Log debug message"""
        self._log(LogLevel.DEBUG, message, Symbols.DEBUG, Colors.GRAY)
    
    def info(self, message: str):
        """Log info message"""
        self._log(LogLevel.INFO, message, Symbols.INFO, Colors.WHITE)
    
    def warning(self, message: str):
        """Log warning message"""
        self._log(LogLevel.WARNING, message, Symbols.WARNING, Colors.YELLOW)
    
    def error(self, message: str):
        """Log error message"""
        self._log(LogLevel.ERROR, message, Symbols.ERROR, Colors.BRIGHT_RED)
    
    def critical(self, message: str):
        """Log critical message"""
        self._log(LogLevel.CRITICAL, message, Symbols.ERROR, Colors.BG_RED + Colors.BRIGHT_WHITE)
    
    def success(self, message: str):
        """Log success message"""
        self._log(LogLevel.SUCCESS, message, Symbols.SUCCESS, Colors.BRIGHT_GREEN)
    
    def agent_start(self, agent_name: str, task: str):
        """Log agent start message"""
        agent_color = self._get_agent_color(agent_name)
        self._log(LogLevel.AGENT, f"{Colors.BOLD}{agent_name}{Colors.RESET} {agent_color}started: {task}{Colors.RESET}", 
                 Symbols.STARTED, agent_color)
        
        # Track agent activity
        if agent_name not in self.agent_counters:
            self.agent_counters[agent_name] = 0
        self.agent_counters[agent_name] += 1
    
    def agent_thinking(self, agent_name: str, message: str):
        """Log agent thinking process"""
        agent_color = self._get_agent_color(agent_name)
        self._log(LogLevel.AGENT, f"{Colors.BOLD}{agent_name}{Colors.RESET} {agent_color}thinking: {message}{Colors.RESET}", 
                 Symbols.THINKING, agent_color)
    
    def agent_action(self, agent_name: str, action: str, details: str = ""):
        """Log agent action"""
        agent_color = self._get_agent_color(agent_name)
        full_message = f"{Colors.BOLD}{agent_name}{Colors.RESET} {agent_color}{action}"
        if details:
            full_message += f": {details}"
        full_message += Colors.RESET
        
        symbol = self._get_action_symbol(action)
        self._log(LogLevel.AGENT, full_message, symbol, agent_color)
    
    def agent_complete(self, agent_name: str, result: str):
        """Log agent completion"""
        agent_color = self._get_agent_color(agent_name)
        self._log(LogLevel.AGENT, f"{Colors.BOLD}{agent_name}{Colors.RESET} {Colors.BRIGHT_GREEN}completed: {result}{Colors.RESET}", 
                 Symbols.COMPLETED, Colors.BRIGHT_GREEN)
    
    def agent_error(self, agent_name: str, error: str):
        """Log agent error"""
        agent_color = self._get_agent_color(agent_name)
        self._log(LogLevel.ERROR, f"{Colors.BOLD}{agent_name}{Colors.RESET} {Colors.BRIGHT_RED}error: {error}{Colors.RESET}", 
                 Symbols.ERROR, Colors.BRIGHT_RED)
    
    def task_start(self, task_name: str, description: str = ""):
        """Log task start"""
        message = f"{Colors.BOLD}{task_name}{Colors.RESET}"
        if description:
            message += f" {Colors.CYAN}- {description}{Colors.RESET}"
        self._log(LogLevel.TASK, message, Symbols.TASK, Colors.BRIGHT_BLUE)
    
    def task_progress(self, task_name: str, progress: float, details: str = ""):
        """Log task progress"""
        progress_bar = self._create_progress_bar(progress)
        message = f"{Colors.BOLD}{task_name}{Colors.RESET} {progress_bar} {progress:.1f}%"
        if details:
            message += f" {Colors.GRAY}- {details}{Colors.RESET}"
        self._log(LogLevel.TASK, message, Symbols.PROCESSING, Colors.BLUE)
    
    def task_complete(self, task_name: str, duration: float = None):
        """Log task completion"""
        message = f"{Colors.BOLD}{task_name}{Colors.RESET} {Colors.BRIGHT_GREEN}completed"
        if duration:
            message += f" in {duration:.2f}s"
        message += Colors.RESET
        self._log(LogLevel.TASK, message, Symbols.SUCCESS, Colors.BRIGHT_GREEN)
    
    def crew_start(self, crew_name: str, agent_count: int):
        """Log crew start"""
        self._log(LogLevel.CREW, f"{Colors.BOLD}{crew_name}{Colors.RESET} {Colors.BRIGHT_MAGENTA}started with {agent_count} agents{Colors.RESET}", 
                 Symbols.CREW, Colors.BRIGHT_MAGENTA)
    
    def crew_progress(self, crew_name: str, completed_tasks: int, total_tasks: int):
        """Log crew progress"""
        progress = (completed_tasks / total_tasks) * 100 if total_tasks > 0 else 0
        progress_bar = self._create_progress_bar(progress)
        self._log(LogLevel.CREW, f"{Colors.BOLD}{crew_name}{Colors.RESET} {progress_bar} {completed_tasks}/{total_tasks} tasks", 
                 Symbols.PROCESSING, Colors.MAGENTA)
    
    def crew_complete(self, crew_name: str, duration: float = None):
        """Log crew completion"""
        message = f"{Colors.BOLD}{crew_name}{Colors.RESET} {Colors.BRIGHT_GREEN}completed"
        if duration:
            message += f" in {duration:.2f}s"
        message += Colors.RESET
        self._log(LogLevel.CREW, message, Symbols.COMPLETED, Colors.BRIGHT_GREEN)
    
    def data_processing(self, operation: str, count: int, data_type: str = "items"):
        """Log data processing operations"""
        self._log(LogLevel.INFO, f"{Colors.BOLD}{operation}{Colors.RESET} {Colors.CYAN}{count} {data_type}{Colors.RESET}", 
                 Symbols.DATABASE, Colors.CYAN)
    
    def metrics_update(self, metric_name: str, value: Any, unit: str = ""):
        """Log metrics updates"""
        self._log(LogLevel.INFO, f"{Colors.BOLD}{metric_name}:{Colors.RESET} {Colors.YELLOW}{value}{unit}{Colors.RESET}", 
                 Symbols.CHART, Colors.YELLOW)
    
    def system_status(self, status: str, details: str = ""):
        """Log system status"""
        color = Colors.BRIGHT_GREEN if status.lower() in ['ready', 'ok', 'healthy'] else Colors.YELLOW
        message = f"{Colors.BOLD}System Status:{Colors.RESET} {color}{status.upper()}{Colors.RESET}"
        if details:
            message += f" {Colors.GRAY}- {details}{Colors.RESET}"
        self._log(LogLevel.INFO, message, Symbols.GEAR, color)
    
    def print_banner(self, title: str, subtitle: str = ""):
        """Print a colorful banner with safe Unicode handling"""
        width = 80
        border = "=" * width
        
        # Safe Unicode handling for Windows
        try:
            safe_title = title.encode('utf-8').decode('utf-8')
            safe_subtitle = subtitle.encode('utf-8').decode('utf-8') if subtitle else ""
        except (UnicodeEncodeError, UnicodeDecodeError):
            # Fallback: remove problematic characters
            safe_title = title.encode('ascii', errors='ignore').decode('ascii')
            safe_subtitle = subtitle.encode('ascii', errors='ignore').decode('ascii') if subtitle else ""
        
        print(f"\n{Colors.BRIGHT_CYAN}{border}{Colors.RESET}")
        print(f"{Colors.BRIGHT_WHITE}{Colors.BOLD}{safe_title.center(width)}{Colors.RESET}")
        if safe_subtitle:
            print(f"{Colors.GRAY}{safe_subtitle.center(width)}{Colors.RESET}")
        print(f"{Colors.BRIGHT_CYAN}{border}{Colors.RESET}\n")
    
    def print_summary(self):
        """Print execution summary"""
        duration = time.time() - self.start_time
        
        self.print_banner("🎯 EXECUTION SUMMARY", f"Total Duration: {duration:.2f}s")
        
        if self.agent_counters:
            print(f"{Colors.BRIGHT_WHITE}Agent Activity:{Colors.RESET}")
            for agent, count in self.agent_counters.items():
                agent_color = self._get_agent_color(agent)
                print(f"  {Symbols.AGENT} {agent_color}{agent}:{Colors.RESET} {Colors.YELLOW}{count} tasks{Colors.RESET}")
            print()
    
    def _get_agent_color(self, agent_name: str) -> str:
        """Get color for specific agent type"""
        agent_lower = agent_name.lower()
        
        if 'csv' in agent_lower or 'reader' in agent_lower:
            return AgentColors.CSV_READER
        elif 'classif' in agent_lower:
            return AgentColors.CLASSIFIER
        elif 'bug' in agent_lower:
            return AgentColors.BUG_ANALYZER
        elif 'feature' in agent_lower:
            return AgentColors.FEATURE_ANALYZER
        elif 'ticket' in agent_lower:
            return AgentColors.TICKET_CREATOR
        elif 'quality' in agent_lower or 'review' in agent_lower:
            return AgentColors.QUALITY_REVIEWER
        elif 'system' in agent_lower:
            return AgentColors.SYSTEM
        else:
            return AgentColors.DEFAULT
    
    def _get_action_symbol(self, action: str) -> str:
        """Get appropriate symbol for action type"""
        action_lower = action.lower()
        
        if 'read' in action_lower:
            return Symbols.READING
        elif 'writ' in action_lower or 'creat' in action_lower:
            return Symbols.WRITING
        elif 'analyz' in action_lower or 'classif' in action_lower:
            return Symbols.ANALYZING
        elif 'process' in action_lower:
            return Symbols.PROCESSING
        else:
            return Symbols.ARROW_RIGHT
    
    def _create_progress_bar(self, progress: float, width: int = 20) -> str:
        """Create a visual progress bar"""
        if not self.enable_colors:
            return f"[{progress:.1f}%]"
        
        filled = int((progress / 100.0) * width)
        bar = "█" * filled + "░" * (width - filled)
        
        # Color the progress bar based on completion
        if progress >= 100:
            color = Colors.BRIGHT_GREEN
        elif progress >= 75:
            color = Colors.GREEN
        elif progress >= 50:
            color = Colors.YELLOW
        elif progress >= 25:
            color = Colors.ORANGE
        else:
            color = Colors.RED
        
        return f"{color}[{bar}]{Colors.RESET}"

# Global logger instance
logger = ColorfulLogger()

# Convenience functions
def log_agent_start(agent_name: str, task: str):
    logger.agent_start(agent_name, task)

def log_agent_action(agent_name: str, action: str, details: str = ""):
    logger.agent_action(agent_name, action, details)

def log_agent_complete(agent_name: str, result: str):
    logger.agent_complete(agent_name, result)

def log_agent_error(agent_name: str, error: str):
    logger.agent_error(agent_name, error)

def log_task_start(task_name: str, description: str = ""):
    logger.task_start(task_name, description)

def log_task_progress(task_name: str, progress: float, details: str = ""):
    logger.task_progress(task_name, progress, details)

def log_task_complete(task_name: str, duration: float = None):
    logger.task_complete(task_name, duration)

def log_data_processing(operation: str, count: int, data_type: str = "items"):
    logger.data_processing(operation, count, data_type)

def log_metrics_update(metric_name: str, value: Any, unit: str = ""):
    logger.metrics_update(metric_name, value, unit)

def log_system_status(status: str, details: str = ""):
    logger.system_status(status, details)

def print_banner(title: str, subtitle: str = ""):
    logger.print_banner(title, subtitle)

def print_summary():
    logger.print_summary()

# Test function to demonstrate colors
def test_colors():
    """Test function to demonstrate all color capabilities"""
    logger.print_banner("🎨 COLORFUL LOGGING TEST", "Testing all color schemes and symbols")
    
    # Test basic log levels
    logger.debug("Debug message with technical details")
    logger.info("General information message")
    logger.warning("Warning about potential issues")
    logger.error("Error occurred during processing")
    logger.success("Operation completed successfully")
    
    # Test agent interactions
    logger.agent_start("CSV Reader Agent", "Reading feedback data files")
    logger.agent_thinking("CSV Reader Agent", "Parsing CSV structure and validating data")
    logger.agent_action("CSV Reader Agent", "reading", "app_store_reviews.csv (1,500 rows)")
    logger.agent_complete("CSV Reader Agent", "Successfully loaded 1,500 reviews")
    
    logger.agent_start("Feedback Classifier", "Categorizing user feedback")
    logger.agent_action("Feedback Classifier", "analyzing", "sentiment and intent classification")
    logger.agent_complete("Feedback Classifier", "Classified 1,500 items with 94.2% confidence")
    
    # Test task progress
    logger.task_start("Data Processing Pipeline", "Processing all feedback sources")
    for i in range(0, 101, 25):
        logger.task_progress("Data Processing Pipeline", i, f"Processing batch {i//25 + 1}/4")
        time.sleep(0.5)
    logger.task_complete("Data Processing Pipeline", 12.3)
    
    # Test crew operations
    logger.crew_start("Feedback Analysis Crew", 6)
    logger.crew_progress("Feedback Analysis Crew", 3, 6)
    logger.crew_complete("Feedback Analysis Crew", 45.7)
    
    # Test data operations
    logger.data_processing("Loaded", 1500, "reviews")
    logger.data_processing("Classified", 1500, "feedback items")
    logger.data_processing("Generated", 342, "tickets")
    
    # Test metrics
    logger.metrics_update("Classification Accuracy", 94.2, "%")
    logger.metrics_update("Processing Speed", 125, " items/sec")
    logger.metrics_update("Memory Usage", 847, " MB")
    
    # Test system status
    logger.system_status("Ready", "All systems operational")
    logger.system_status("Processing", "Analyzing feedback data")
    logger.system_status("Complete", "All tasks finished successfully")
    
    # Print summary
    logger.print_summary()

if __name__ == "__main__":
    test_colors()