from collections import Counter

def analyze_logs(log_file_path, top_responses=3, top_errors=2):
    """
    Analyze log file and generate a structured report.
    
    Args:
        log_file_path (str): Path to the log file
        top_responses (int): Number of top responses to include
        top_errors (int): Number of top errors to include
        
    Returns:
        str: Formatted report string with log summary,
             top AI responses, and most common errors
    """
    content = read_file(log_file_path)
    
    lines = content.split('\n')
    log_entries = []
    for line in lines:
        # Remove the timestamp at the start of each line
        line = line[22:]
        # Process each line
        parts = line.split(' ', 1)
        if len(parts) > 1:
            first_word = parts[0]
            rest_of_string = parts[1][2:]
            
            if first_word == "INFO" and rest_of_string.startswith("Agent Response: "):
                rest_of_string = rest_of_string[len("Agent Response: "):]
            
            log_entry = {
                "type": first_word,
                "message": rest_of_string
            }

            log_entries.append(log_entry)   
    
    # Count log types
    log_type_counts = Counter(entry['type'] for entry in log_entries)
    
    # Extract top AI responses
    ai_responses = [entry['message'] for entry in log_entries if entry['type'] == 'INFO']
    top_ai_responses = Counter(ai_responses).most_common(top_responses)
    
    # Extract most common errors
    errors = [entry['message'] for entry in log_entries if entry['type'] == 'ERROR']
    top_errors_list = Counter(errors).most_common(top_errors)
    
    # Generate report
    report = f"Log Summary:\n"
    report += f"- INFO messages: {log_type_counts['INFO']}\n"
    report += f"- ERROR messages: {log_type_counts['ERROR']}\n"
    report += f"- WARNING messages: {log_type_counts['WARNING']}\n\n"
    
    report += f"Top {top_responses} AI Responses:\n"
    for i, (response, count) in enumerate(top_ai_responses, 1):
        report += f"{i}. {response} ({count} times)\n"
    
    report += f"\nMost Common Errors:\n"
    for i, (error, count) in enumerate(top_errors_list, 1):
        report += f"{i}. {error} ({count} times)\n"
    
    return report

def read_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()

if __name__ == "__main__":
    report = analyze_logs("sample.log")
    print(report)

