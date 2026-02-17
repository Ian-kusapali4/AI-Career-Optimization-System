import yaml
import os

def yaml_extraction(filename):
    project_root = os.path.dirname(os.path.dirname(__file__))

    yaml_file_path = os.path.join(project_root, '..','core', 'prompts', filename)
    config_data = None

    try:
        
        with open(yaml_file_path, 'r') as file:
            config_data = yaml.safe_load(file)
            
        print("Yaml file loaded successfully.")
        
        

    except FileNotFoundError:
        print(f"Error: The file '{yaml_file_path}' was not found.")
    except yaml.YAMLError as e:
        print(f"Error parsing YAML file: {e}")
    return config_data
