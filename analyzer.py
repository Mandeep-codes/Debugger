def read_and_print_file(filepath):
    results = []
    with open(filepath, 'r') as file:
        for line in file:
            clean_line = line.strip()
            if clean_line.startswith('*') or clean_line.startswith('.'):
                continue
            parts = clean_line.split()
            results.append(parts)
    return results

def find_dangling_nets(component_list):
    node_counts = {}
    for component in component_list:
        nodes_for_this_component = component[1:-1]
        for node in nodes_for_this_component:
            node_counts[node] = node_counts.get(node,0) + 1

    error_reports = []
    for node, count in node_counts.items():
        if count == 1:
            report = f"Dangling Net Found: Node '{node}' is only connected to one component."
            error_reports.append(report)
    return error_reports

def check_for_missing_models(component_list,filepath):
    required_models = set()
    for component in component_list:
        component_name = component[0]
        if component_name.startswith('Q'):
            model_name = component[-1]
            required_models.add(model_name)

    defined_models = set()
    with open(filepath  , 'r') as file:
        for line in file:
            clean_line = line.strip()
            if clean_line.upper().startswith('.MODEL'):
                parts = clean_line.split()
                defined_models.add(parts[1])

    missing_models = required_models - defined_models
    error_reports = []
    for model in missing_models:
        report = f"Missing Model Definition: Model '{model}' is used but not defined."
        error_reports.append(report)
    return error_reports


def run_full_analysis(filepath):
    report_lines = []

    parsed_data = read_and_print_file(filepath)
    all_errors = []

    dangling_net_erros = find_dangling_nets(parsed_data)
    all_errors.extend(dangling_net_erros)

    missing_model_errors = check_for_missing_models(parsed_data, filepath)
    all_errors.extend(missing_model_errors)

    if all_errors: 
        report_lines.append("Issues Found:")
        report_lines.extend(all_errors)
    else:
        report_lines.append("No issues found.")

    final_report = "\n".join(report_lines)
    return all_errors
            


if __name__ == "__main__":
    report = run_full_analysis("test_netlist.txt")
    print(report)
    

