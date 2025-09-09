import joblib

try:
    model = joblib.load('error_classifier.joblib')
except FileNotFoundError:
    model = None

suggestion_map = {
    'CONVERGENCE_ERROR': "Suggestion: The simulation failed to converge. This can be caused by an unstable circuit or incorrect simulation parameters.",
    'UNKNOWN_PARAMETER': "Suggestion: An 'unknown parameter' error means a component has a property the simulator doesn't recognize. Check for typos.",
    'MISSING_NODE_ERROR': "Suggestion: A 'missing node' error means a component is referring to a connection point that doesn't exist. Check your netlist for typos."
}

def analyze_log_with_ml(filepath):
    if model is None:
        return ["Error: Model file 'error_classifier.joblib' not found. Please run ml_trainer.py to create it."]
    
    with open(filepath, 'r') as file:
        log_content = file.read()
    
    prediction = model.predict([log_content])
    
    error_type = prediction[0]
    
    suggestion = suggestion_map.get(error_type, "Error: Could not classify this error type.")
    
    return [suggestion]

def run_error_analysis(filepath):
    report_lines = [f"--- ML Analysis Report for {filepath} ---"]
    
    suggestions = analyze_log_with_ml(filepath)
    
    report_lines.extend(suggestions)
    
    return "\n".join(report_lines)

if __name__ == "__main__":
    report = run_error_analysis('test_error.log')
    print(report)