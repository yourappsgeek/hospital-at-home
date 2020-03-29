# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np
import pandas as pd
from bokeh.io import show, output_file
from bokeh.models import ColumnDataSource, Legend, LegendItem, Scatter
from bokeh.plotting import figure, output_file, show, output_notebook
from bokeh.models.tools import HoverTool
from bokeh.core.properties import value
from bokeh.models.widgets import DataTable, TableColumn

path = 'dash.csv'

dtype = {'Overall_Risk_Status': str, 'Patient_ID': str, 'age': str, 'Location': str, 'since_diagnosis': str, 'SpO2': str, 'heart_rate': str, 'resp_rate': str, 'live_data': str,'trends': str, 'low': str,'Text': str, 'Call': str, 'Emergency_Dispatch': str, 'Notepad': str, 'Last_interaction': str, 'Medical_History': str, 'Medical_History': str, 'on_home_oxygen?': str, 'PAP-device': str}


patient_info_df = pd.read_csv(path, usecols=dtype.keys(), dtype=dtype)


patient_info_df.head()

TOOLS = "pan, wheel_zoom, box_zoom, box_select,reset, save"


source = ColumnDataSource(patient_info_df)


columns = [TableColumn(field = "Overall_Risk_Status", title = "Overall_Risk_Status"),TableColumn(field = "Patient_ID", title = "Patient_ID"), TableColumn(field = "age", title = "age"), TableColumn(field = "Location", title = "Location"), TableColumn(field = "since_diagnosis", title = "since_diagnosis"), TableColumn(field = "SpO2", title = "SpO2"), TableColumn(field = "heart_rate", title = "heart_rate"), TableColumn(field = "resp_rate", title = "resp_rate"), TableColumn(field = "live_data", title = "live_data"), TableColumn(field = "trends", title = "trends"), TableColumn(field = "low", title = "low"), TableColumn(field = "Text", title = "Text"), TableColumn(field = "Call", title = "Call"), TableColumn(field = "Emergency_Dispatch", title = "Emergency_Dispatch"), TableColumn(field = "Notepad", title = "Notepad"), TableColumn(field = "Last_interaction", title = "Last_interaction"), TableColumn(field = "Medical_History", title = "Medical_History"),TableColumn(field = "on_home_oxygen?", title = "on_home_oxygen?"), TableColumn(field = "PAP-device", title = "PAP-device")]


data_table = DataTable(source = source, columns = columns, width = 1500, height = 1500, editable = False)

show(data_table)
