'''This module creates the graph for a presidents approval rating
   using 95% and 66% confidence intervals'''

import altair as alt
import pandas as pd
from scipy import stats

def create_approval_lines(df: pd.DataFrame, color: str, x_column: str, y_column: str) -> alt.Chart:
    '''
    Creates line chart for approval ratings across a date spectrum
    
    Parameters:
    df (pd.Dataframe): Either approval or disapproval Dataframe
    color (str): Any hex color code
    x_column (str): Date column name from Dataframe
    y_column (str): Predicted rating column name

    Returns:
    Altair Chart object     
    '''

    linechart=alt.Chart(df).mark_line(color=color).encode(
        x=alt.X(x_column + ':T',title="Date",axis=alt.Axis(labelAngle=45,format="%B %Y")),
        y=alt.Y(y_column + ':Q',title='Rating Percentage',scale=alt.Scale(domain=[25,70])),
        tooltip=[y_column,x_column + ':T']).interactive()
    return linechart

def create_approval_dots(df: pd.DataFrame, color: str, x_column: str, y_column: str) -> alt.Chart:
    '''
    Creates dot chart for individual poll results.

    Parameters:
    df (pd.Dataframe): Either approval or disapproval Dataframe
    color (str): Any hex color code
    x_column (str: Date column name from Dataframe
    y_column (str): Individual poll value column name

    Returns:
    Altair Chart object    
    '''

    dots=alt.Chart(df).mark_point(color=color,opacity=.25,filled=True,size=15).encode(
        x=x_column + ':T',
        y=alt.Y(y_column + ':Q',scale=alt.Scale(domain=[25,70])))
    return dots

def create_approval_bands(df: pd.DataFrame, color: str, x_column: str,
                          y1: str, y2: str) -> alt.Chart:
    '''
    Creates confidence interval bands for line chart based off of dataframe data.

    Parameters:
    df (pd.Dataframe): Either approval or disapproval Dataframe
    color (str): Any hex color code
    x_column (str): Date column name from Dataframe
    y1 (str): Upper Bound column name
    y2 (str): Lower Bound column name

    Returns:
    Altair Chart object
    '''

    bands=alt.Chart(df).mark_area(color=color,opacity=.3).encode(
        x=x_column + ':T',
        y=y1,
        y2=y2)
    return bands

def create_approval_graph(df1: pd.DataFrame,df2: pd.DataFrame) -> alt.Chart:
    '''
    Creates approval graph using line charts, 99% conf. interval charts and dot charts.

    Parameters:
    df1 (pd.Dataframe): Approval Dataframe
    df2 (pd.DataFrame): Disapproval Dataframe

    Returns:
    Altair Chart object
    '''

    line1=create_approval_lines(df1,'#11ad52','modeldate','approve_estimate')
    line2=create_approval_lines(df1,'#ff7e21','modeldate','disapprove_estimate')
    dot1=create_approval_dots(df2,'#11ad52','enddate','adjusted_approve')
    dot2=create_approval_dots(df2,'#ff7e21','enddate','adjusted_disapprove')
    band1=create_approval_bands(df1,'#11ad52','modeldate','approve_hi','approve_lo')
    band2=create_approval_bands(df1,'#ff7e21','modeldate','disapprove_hi','disapprove_lo')

    chart=(line1 + line2 + dot1 + dot2 + band1 + band2).properties(
    width=900,height=300,title="How Popular is Donald Trump?").configure_title(
    fontSize=16).configure_axis(titleFontSize=14)
    return chart

def create_66perc_ci(df1: pd.DataFrame ,df2: pd.DataFrame) -> alt.Chart:
    '''
    Creates 66% confidence interval of approval ratings by reverse engineering standard error
    from the dataset.

    Parameters:
    df1 (pd.Dataframe): Approval Dataframe
    df2 (pd.DataFrame): Disapproval Dataframe

    Returns:
    Altair Chart object
    '''

    df2=df2.groupby('enddate')[['enddate','samplesize']].sum(numeric_only=True)
    merged_df=df1.merge(df2,left_on = 'modeldate',right_on = 'enddate',how='inner')

    #Creating column that has a t-value of 95th percentile for each row, dependent on
    # the sample size of that day
    merged_df['tval_90']=merged_df.apply(lambda row: stats.t.ppf(.95,row.samplesize-1),axis=1)

    merged_df["approve_SE"]=\
        (merged_df['approve_hi']-merged_df['approve_estimate'])/merged_df['tval_90']
    merged_df["disapprove_SE"]=\
        (merged_df['disapprove_hi']-merged_df['disapprove_estimate'])/merged_df['tval_90']

    #Creating column that has a t-value at 83.35th percentile for each row, dependent on
    # the sample size of that day. This is for the creation of a 66% confidence interval
    merged_df['tval_66']=merged_df.apply(lambda row: stats.t.ppf(.833335,row.samplesize-1),axis=1)

    #creating columns for upper and lower bounds of approval rating
    merged_df['approve_upper66']=\
        merged_df['approve_estimate']+merged_df['tval_66']*merged_df['approve_SE']
    merged_df['approve_lower66']=\
        merged_df['approve_estimate']-merged_df['tval_66']*merged_df['approve_SE']

    #creating columns for upper and lower bounds of disapproval rating
    merged_df['disapprove_upper66']=\
        merged_df['disapprove_estimate']+merged_df['tval_66']*merged_df['disapprove_SE']
    merged_df['disapprove_lower66']=\
        merged_df['disapprove_estimate']-merged_df['tval_66']*merged_df['disapprove_SE']

    approve_bands66 = create_approval_bands(merged_df,'blue','modeldate',
                                            'approve_upper66','approve_lower66')
    disapprove_bands66 = create_approval_bands(merged_df,'purple','modeldate',
                                               'disapprove_upper66','disapprove_lower66')
    return approve_bands66 + disapprove_bands66
