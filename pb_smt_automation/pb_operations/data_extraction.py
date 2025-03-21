import pandas as pd
import os
import yaml

def load_yaml_config(config_path):
    with open(config_path, 'r') as file:
        return yaml.safe_load(file)

def extract_data(file_path):
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return None
    try:
        df = pd.read_csv(file_path, delimiter=';', header=1)
        return df
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return None
