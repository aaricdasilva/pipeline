import logging
import os
from pyaml import yaml
import pandas as pd
import gc
import re

def read_config_file(filepath):
    with open(filepath, 'r') as stream:
        try:
            return yaml.safe_load(stream)
        except yaml.YAMLerror as exc:
            logging.error(exc)
            
def col_header_val(df, table_config):
    df.columns = df.columns.str.lower()
    expected_col = list(map(lambda x: x.lower(), table_config['columns']))
    expected_col.sort()
    df.columns = list(map(lambda x: x.lower(), list(df.columns)))
    df = df.reindex(sorted(df.columns), axis = 1)
    if len(df.columns) == len(expected_col) and list(expected_col) == list(df.columns):
        print("columns name and column length validation passed")
        return 1
    else:
        print("columns name and column length validation failed")
        missmatched_column_file = list(set(df.columns).difference(expected_col))
        print("The following files are not found in the YAML file", missmatched_column_file)
        missing_YAML_file = list(set(expected_col).difference(df.columns))
        print("The following files are not uploaded in the file upload", missing_YAML_file)
        logging.info(f'df columns: {df.columns}')
        logging.info(f'expected columns: {expected_col}')
        return 0
    
