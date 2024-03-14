# Week2_Code_Crafting

This script creates an approval rating chart for a political figure using 95 and 66%  confidence intervals. It takes in two datasets, e.g. the provided datasets
'approval_topline.csv' and 'approval_poll_list.csv', and loads and cleans the data with different modules and then creates the charts with altair.
All dependencies should be installed automatically with the provided installation function just by running the script (e.g. python main.py 'approval_topline.csv' 'approval_poll_list.csv' 'chart'), but I have provided a dependencies.txt just in case. 

The script has 4 modules:
1.'main.py': installs dependencies and calls the other modules to create the chart.
2.'load_data.py': loads the data from a path name and returns the correct rows.
3.'clean.py': cleans the data by removing irrelevant columns 
4.'create_graphs': creates all of the appropriate graphs using various functions to create different layers of the final graph. 
