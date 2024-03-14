"This module loads poll data into dataframes and selects appropriate rows"
import pandas as pd

def load_poll_data(path: str) -> pd.DataFrame:
    '''
    Loads data from path and returns Dataframe with subset of rows that 
    contain the "All polls" value in the 'subgroup' column.

    Parameters:
    df (pd.DataFrame): Pandas DataFrame

    Returns:
    pd.Dataframe
    '''

    df=pd.read_csv(path)
    df=df[df['subgroup']=="All polls"]
    return df
