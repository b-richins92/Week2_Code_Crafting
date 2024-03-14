'''This module cleans the poll dataframes'''
import pandas as pd

def clean_poll_df(df: pd.DataFrame, cols: list) -> pd.DataFrame:
    '''
    Returns dataframe with desired columns.
    
    Parameters:
    path (str): path of csv file
    cols (list): list of desired columns

    Returns:
    Pandas Dataframe
    '''
    df=df[cols]
    return df
