Design Document: eSim AI Debugging Tool
This document provides a detailed explanation of the internal architecture, workflow, and technical implementation of the AI-Based Debugging Tool for eSim.

1. Tool Architecture and Workflow
1.1 High-Level Architecture
The application is architected as a monolithic, event-driven desktop application using Python and the Tkinter GUI framework. The internal structure is highly modular, following a Model-View-Controller (MVC) pattern to ensure a clean separation of concerns:

Model: This layer consists of the backend analysis modules (analyzer.py, error_analyzer.py) and the data assets (error_classifier.joblib, error_data.csv). These components contain all the business logic and data processing and are completely independent of the user interface.

View: The gui.py script is responsible for constructing the entire GUI. It defines the layout (sidebar, tabs), styling (dark theme), and all visual widgets.

Controller: The controller logic is implemented as methods within the DebuggerApp class in gui.py. These methods (analyze_netlist_file, Messages, etc.) act as the bridge, responding to user events, calling the appropriate Model functions, and passing the results back to the View for display.

1.2 Workflow
The application's workflow is initiated by user events within the GUI:

User Action: The user clicks a button (e.g., "Analyze Netlist File") or sends a chat message.

Controller Trigger: The corresponding event handler method in the DebuggerApp class is called.

Input Gathering: The method gathers necessary input, either by opening a filedialog to get a file path or by getting text from the chat input widget.

Backend Processing: The controller calls the relevant function from one of the imported backend modules (e.g., run_full_analysis(filepath)).

Model Execution: The backend module performs its task:

The Netlist Analyzer parses the file and applies its rule-based checks.

The Error Log Analyzer loads the file and uses the ML model to predict the error category.

The Chatbot sends an HTTP request to the local Ollama server.

Return Value: The backend function returns a formatted string containing the report or suggestion.

View Update: The controller method receives the string and calls a helper method (_display_report or _append_to_chat) to update the appropriate widget in the GUI.

2. How AI/ML is Utilized in the Tool
The tool leverages two distinct forms of AI and Machine Learning.

2.1 Learning-Based Error Log Classification
This feature is powered by a classic supervised machine learning pipeline, implemented using Python's scikit-learn library.

Training (ml_trainer.py):

Data Source: A manually curated CSV file (error_data.csv) provides labeled training examples of error message snippets and their corresponding categories.

Data Loading: The pandas library is used to load the CSV into a DataFrame.

Pipeline Creation: A scikit-learn Pipeline is created to chain two steps:

TfidfVectorizer: This converts the raw text of the error messages into a numerical matrix based on term frequency-inverse document frequency. This allows the model to learn which words are most significant for each error type.

MultinomialNB: A Multinomial Naive Bayes classifier is used as the "brain." It's a highly efficient and effective algorithm for text classification tasks.

Model Training & Serialization: The pipeline is trained on the data using the .fit() method. The final, trained model object is then serialized and saved to a single file, error_classifier.joblib, using the joblib library.

Inference (error_analyzer.py):

Model Loading: When the application starts, the error_classifier.joblib file is loaded into memory.

Prediction: When the user analyzes a log file, its entire content is read and passed to the loaded model's .predict() method. The model automatically performs the vectorization and classification, returning the predicted error category (e.g., 'CONVERGENCE_ERROR').

Suggestion Mapping: The predicted category is used as a key to look up a detailed, human-readable suggestion from a Python dictionary.

2.2 AI Chatbot Integration
The interactive chatbot is powered by a large language model (LLM) running locally on the user's machine via Ollama.

Backend: The Ollama application serves the qwen:4b LLM, making it available via a local REST API endpoint.

Communication: The gui.py script uses the requests library to communicate with this API.

Workflow:

When the user sends a message, the Messages method constructs a JSON payload containing the user's prompt and the model name.

An HTTP POST request is sent to http://localhost:11434/api/generate.

The script waits for the response, which is also in JSON format.

The AI's text reply is extracted from the "response" key of the JSON and displayed in the chat history.

Robust error handling is included to manage cases where the connection to the Ollama server fails.