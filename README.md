eSim AI Debugging Tool

This project is a standalone GUI application built in Python to assist eSim users in debugging electronic circuits. It combines a proactive netlist analyzer, a machine learning-powered error log classifier, and an interactive AI chatbot into a single, user-friendly tool with a modern dark theme.


Features Implemented
This application successfully implements all the features outlined in the task requirements, including the optional advanced feature.

Netlist Analysis Engine: Proactively checks .cir.out files for common structural errors like dangling connections and missing .MODEL definitions before a simulation is run.

Error Log Analysis & Debugging: Reads simulation error logs and uses a trained Machine Learning model to classify the error type and provide a clear, actionable suggestion.

AI Chatbot Integration: Features a fully functional chat interface that connects to a locally-run large language model (via Ollama) for real-time, interactive troubleshooting and conceptual help.

Learning-Based Debugging Suggestions (Advanced Feature): The error log analyzer is powered by a custom-trained scikit-learn model, fulfilling the advanced feature requirement.

Aesthetic GUI: All features are integrated into a professional, modern GUI with a sidebar/tab layout, a dark theme, and SVG icons.

How to Use the Tool
1. Installation and Setup
Prerequisites:

Python 3.8 or newer.

(Optional but Recommended) git for cloning the repository.

Ollama: The AI chatbot requires the Ollama desktop application to be installed and running.

Download and install Ollama from https://ollama.com.

Run the following command in your terminal to download the AI model: ollama pull qwen:4b

Installation Steps:

Clone the repository:

git clone <your-repo-link>
cd <your-repo-folder>

Create and activate a virtual environment:

# Create the environment
python3 -m venv venv
# Activate it (Linux/macOS)
source venv/bin/activate
# Or on Windows
# venv\Scripts\activate

Install required Python libraries:

pip install -r requirements.txt

(Optional) Train the ML Model: A pre-trained model (error_classifier.joblib) is included. However, if you add new data to error_data.csv, you can retrain the model by running:

python3 ml_trainer.py

2. Running the Application
Ensure your virtual environment is active.

Make sure your Ollama application is running in the background.

Launch the tool by running the main GUI script:

python3 gui.py

The main application window will appear.

3. Interacting with the Tool
To analyze a netlist file: Click the "Analyze Netlist" button in the sidebar, and an "Open File" dialog will appear. Select your .cir.out file. The analysis will be displayed in the "Analysis Report" tab.

To analyze an error log file: Click the "Analyze Log File" button. Select your .log file. The ML-powered suggestion will be displayed in the "Analysis Report" tab.

To chat with the AI: Click the "AI Chatbot" tab. Type your question into the input box at the bottom and click "Send" or press Enter. The conversation will appear in the chat history.

Troubleshooting
Error: could not connect to ollama server appears in the chat.

Solution: The Ollama application is not running. Please start the Ollama application on your computer and try again.

Warning: Icon files not found appears in the terminal.

Solution: The application expects an icons folder in the main directory containing netlist_icon.svg and log_icon.svg. The application will still run without them, but the buttons will not have icons.

Error: FileNotFoundError: [Errno 2] No such file or directory: 'error_classifier.joblib'

Solution: The pre-trained model is missing. Run python3 ml_trainer.py to create it.
