import yaml
import sys

# Load the YAML file
def load_yaml(file_path):
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

# Save the YAML file
def save_yaml(file_path, data):
    with open(file_path, 'w') as file:
        yaml.safe_dump(data, file, default_flow_style=False)

# Update the version variables in the YAML file
def update_version(file_path, commit_hash, version_num):
    data = load_yaml(file_path)
    
    # Update the specific variables
    data["Device"]["Version"] = version_num
    data["Device"]["Hash"] = commit_hash
    
    # Add or update other variables as needed
    # data['another_variable'] = 'some_value'
    
    save_yaml(file_path, data)

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: update_version.py <yaml_file_path> <commit_hash> <version_num>")
        sys.exit(1)
    
    yaml_file_path = sys.argv[1]
    commit_hash = ""sys.argv[2]""
    version_num = sys.argv[3]
    
    update_version(yaml_file_path, commit_hash, version_num)