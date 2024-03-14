'''This is the main module. Installs the neccessary libraries and
creates an approval rating chart.'''

import pip
import load_data
import clean
#pylint: disable=no-member
#pylint: disable=bare-except
def install(package: str):
    '''
    Attempts to install package using pip.
    
    Parameters:
    package(string): Name of library or module
    '''

    try:
        pip.main(['install', package])
    except:
        print(f'Please install {package} in terminal')

if __name__ == '__main__':
    install('altair')
    install('vl-convert-python') #converts altair charts to .png format
    install('scipy')
    import argparse
    import vl_convert as vlc
    import create_graphs

    parser = argparse.ArgumentParser()
    parser.add_argument('first_path', help="approval_topline.csv")
    parser.add_argument('second_path', help="approval_poll_list.csv")
    parser.add_argument('png_path',help='where to save the graph')
    args=parser.parse_args()

    df1= load_data.load_poll_data(args.first_path)
    df1= clean.clean_poll_df(df1, df1.columns[2:-1])
    df2= load_data.load_poll_data(args.second_path)
    df2= clean.clean_poll_df(df2, ['enddate', 'samplesize', 'adjusted_approve', 'adjusted_disapprove'])

    merged=df1.merge(df2,left_on='modeldate',right_on='enddate',how='inner')
    chart = create_graphs.create_approval_graph(df1, df2)
    chart2 = create_graphs.create_66perc_ci(df1, df2)
    final_chart=chart + chart2
    png_data = vlc.vegalite_to_png(final_chart.to_json(), scale=4)

    with open(args.png_path + '.png', "wb") as f:
        f.write(png_data)
    print(type(chart))
