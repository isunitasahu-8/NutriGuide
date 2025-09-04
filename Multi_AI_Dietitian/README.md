# AI Dietitian Pro - Professional Multi-Agent Nutrition System

## Overview

A sophisticated, professional multi-agent AI system designed to provide personalized nutrition planning and dietary guidance. The system features 13 specialized AI agents working collaboratively to create comprehensive, safe, and culturally adapted meal plans.

## System Architecture

### 13 Specialized AI Agents

1. **Preference Agent** - User preference management and profile building
2. **Goal Agent** - Nutrition goal planning and target calculation
3. **Food Knowledge Agent** - Recipe database and nutrition science
4. **Restriction & Safety Agent** - Allergy checking and safety validation
5. **Adaptation Agent** - Plan adaptation based on feedback and progress
6. **Motivation & Education Agent** - User engagement and nutrition education
7. **Cultural & Lifestyle Agent** - Cultural adaptation and lifestyle integration
8. **Budget & Accessibility Agent** - Cost optimization and availability checking
9. **Meal Timing & Habit Agent** - Schedule optimization and habit formation
10. **Sustainability & Environment Agent** - Eco-friendly food choices
11. **Medical & Biomarker Agent** - Health data integration and analysis
12. **Feedback & Learning Agent** - User feedback processing and learning
13. **Emergency & Risk Agent** - Risk assessment and medical alerts

## Features

- **Professional Interface**: Modern, classy design with beautiful gradient backgrounds
- **Real-time Monitoring**: Live agent status and performance tracking
- **Personalized Planning**: AI-generated meal plans based on individual preferences
- **Safety First**: Comprehensive allergy and medical condition checking
- **Cultural Adaptation**: Respects cultural, religious, and lifestyle preferences
- **Interactive Analytics**: Real-time charts and visualizations
- **Responsive Design**: Optimized for desktop and mobile devices

## Quick Start

### 1. Run the System

```bash
# Single command to run everything
python run_system.py
```

### 2. Manual Setup (Alternative)

```bash
# Install dependencies
pip install -r requirements.txt

# Run Streamlit app
streamlit run streamlit_app.py
```

### 3. Access the Interface

Open your browser and navigate to: `http://localhost:8501`

## System Requirements

- Python 3.8+
- 4GB RAM minimum
- Internet connection for Gemini API
- Modern web browser

## Configuration

### Environment Variables

Create a `.env` file in the project root:

```bash
# Required
GEMINI_API_KEY=your_gemini_api_key_here

# Optional
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=localhost
```

### Gemini API Setup

1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Add the key to your `.env` file

## Usage

### 1. Initialize System
- Click "Initialize System" in the sidebar
- Add your Gemini API key in settings

### 2. Create User Profile
- Fill out comprehensive profile information
- Include dietary preferences, allergies, and medical conditions
- Set nutrition goals and lifestyle preferences

### 3. Generate Meal Plan
- Create personalized nutrition plans
- View detailed meal breakdowns
- Analyze individual dishes for nutrition

### 4. Monitor System
- Real-time agent status dashboard
- Performance metrics and insights
- System health monitoring

## File Structure

```
Multi_AI_Dietitian/
├── run_system.py              # Main system runner
├── streamlit_app.py           # Professional web interface
├── requirements.txt           # Essential dependencies
├── README.md                  # This file
└── multi_ai_dietitian/
    └── a2a/
        ├── protocol.py        # A2A communication protocol
        ├── orchestrator.py    # Main system orchestrator
        └── agents/            # Individual agent files
            ├── preference_agent.py
            ├── goal_agent.py
            ├── food_knowledge_agent.py
            ├── restriction_safety_agent.py
            ├── adaptation_agent.py
            ├── motivation_education_agent.py
            ├── cultural_lifestyle_agent.py
            ├── budget_accessibility_agent.py
            ├── meal_timing_habit_agent.py
            ├── sustainability_environment_agent.py
            ├── medical_biomarker_agent.py
            ├── feedback_learning_agent.py
            └── emergency_risk_agent.py
```

## Technical Details

### Technology Stack
- **Backend**: Python with multi-agent architecture
- **Frontend**: Streamlit with custom CSS styling
- **AI Integration**: Google Gemini LLM
- **Data Visualization**: Plotly interactive charts
- **State Management**: Streamlit session state

### Design Features
- **Typography**: Cormorant Garamond (serif) + Inter (sans-serif)
- **Color Scheme**: Professional gradient backgrounds
- **Layout**: Responsive grid system with glassmorphism effects
- **Animations**: Smooth hover effects and transitions

## Safety Features

- **Medical Validation**: Checks for contraindications and interactions
- **Allergy Screening**: Comprehensive allergen detection
- **Risk Assessment**: Monitors for dangerous conditions
- **Professional Standards**: Clinical-style safety protocols

## Support

For technical support or questions:
1. Check the system logs in the Streamlit interface
2. Verify your Gemini API key is correctly configured
3. Ensure all dependencies are properly installed

## License

This project is licensed under the MIT License.

## Disclaimer

This system is designed for educational and informational purposes. It is not a substitute for professional medical advice, diagnosis, or treatment. Always consult with qualified healthcare professionals for medical decisions.

---

**Ready to revolutionize your nutrition planning?**

Start your journey with AI Dietitian Pro today!
