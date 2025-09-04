"""
AI Dietitian System - Main Runner

This file runs all the necessary components of the multi-agent dietitian system.
"""

import os
import sys
import subprocess
import time

def check_dependencies():
    """Check if required packages are installed"""
    required_packages = [
        'streamlit',
        'plotly', 
        'pandas',
        'google-generativeai'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"Missing packages: {', '.join(missing_packages)}")
        print("Installing missing packages...")
        for package in missing_packages:
            subprocess.run([sys.executable, '-m', 'pip', 'install', package])
        print("All packages installed successfully!")
    else:
        print("All required packages are already installed.")

def setup_environment():
    """Setup the environment for running the system"""
    print("Setting up AI Dietitian System...")
    
    # Check if .streamlit directory exists
    if not os.path.exists('.streamlit'):
        os.makedirs('.streamlit')
        print("Created .streamlit directory")
    
    # Create config.toml if it doesn't exist
    config_path = '.streamlit/config.toml'
    if not os.path.exists(config_path):
        with open(config_path, 'w') as f:
            f.write("""[server]
port = 8501
address = "localhost"

[theme]
primaryColor = "#667eea"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"
""")
        print("Created Streamlit configuration file")
    
    # Create .env file template if it doesn't exist
    env_path = '.env'
    if not os.path.exists(env_path):
        with open(env_path, 'w') as f:
            f.write("""# AI Dietitian System Environment Variables
# Add your Gemini API key here
GEMINI_API_KEY=your_api_key_here

# Streamlit settings
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=localhost
""")
        print("Created environment file template")
        print("Please edit .env file and add your Gemini API key")

def run_streamlit():
    """Run the Streamlit application"""
    print("Starting Streamlit application...")
    print("The application will open in your browser at http://localhost:8501")
    print("Press Ctrl+C to stop the application")
    
    try:
        # Run streamlit app
        subprocess.run([
            sys.executable, '-m', 'streamlit', 'run', 'streamlit_app.py',
            '--server.port', '8501',
            '--server.address', 'localhost'
        ])
    except KeyboardInterrupt:
        print("\nApplication stopped by user")
    except Exception as e:
        print(f"Error running Streamlit: {e}")

def show_system_info():
    """Show system information and status"""
    print("\n" + "="*60)
    print("AI DIETITIAN SYSTEM - PROFESSIONAL MULTI-AGENT NUTRITION SYSTEM")
    print("="*60)
    print("\nSystem Components:")
    print("• 13 Specialized AI Agents")
    print("• Professional Streamlit Interface")
    print("• Gemini LLM Integration")
    print("• Comprehensive Nutrition Planning")
    print("• Real-time Agent Monitoring")
    
    print("\nAvailable Features:")
    print("• User Profile Management")
    print("• Personalized Meal Planning")
    print("• Nutrition Analysis")
    print("• Agent Insights Dashboard")
    print("• Cultural & Dietary Adaptation")
    print("• Safety & Allergy Checking")
    print("• Budget & Accessibility Optimization")
    
    print("\nTechnical Features:")
    print("• Modern Professional UI Design")
    print("• Responsive Layout")
    print("• Interactive Charts & Visualizations")
    print("• Real-time Data Processing")
    print("• Secure API Integration")
    
    print("\n" + "="*60)

def main():
    """Main function to run the system"""
    show_system_info()
    
    # Check dependencies
    print("\nChecking system dependencies...")
    check_dependencies()
    
    # Setup environment
    print("\nSetting up environment...")
    setup_environment()
    
    # Ask user if they want to run the system
    print("\nEnvironment setup complete!")
    response = input("Do you want to start the AI Dietitian System now? (y/n): ").lower()
    
    if response in ['y', 'yes']:
        run_streamlit()
    else:
        print("\nTo run the system later, use:")
        print("python run_system.py")
        print("\nOr run directly with:")
        print("streamlit run streamlit_app.py")
        print("\nThank you for using AI Dietitian System!")

if __name__ == "__main__":
    main()
