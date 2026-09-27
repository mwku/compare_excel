import pandas as pd
import numpy as np

import ui

def compare_files(data_a:pd.DataFrame,data_b:pd.DataFrame,title_equal:str,title_diffrent:str) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Compare two dataframes and return the differences.
    """
    result:list[tuple[int, int]] = []
    for i in range(len(data_a)):
        for j in range(len(data_b)):
            pass


    return_data_a = pd.DataFrame(columns=data_a.columns)
    return_data_b = pd.DataFrame(columns=data_b.columns)
    for i in range(len(result)):
        return_data_a = pd.concat([return_data_a, data_a.iloc[[result[i][0]]]])
        return_data_b = pd.concat([return_data_b, data_b.iloc[[result[i][1]]]])
    return (return_data_a, return_data_b)

                
def read_file(file_path:str) -> pd.DataFrame:
    """
    Read a file and return a dataframe.
    """
    if file_path.endswith('.csv'):
        return pd.read_csv(file_path)
    elif file_path.endswith('.xlsx'):
        return pd.read_excel(file_path)
    else:
        raise ValueError('File type not supported')


