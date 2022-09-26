# Importing packages
import pandas as pd
import plotly.graph_objs as go
import plotly.offline as offline
import streamlit as st
#offline.init_notebook_mode(connected=True)

# Title
st.title("Funnel Charts")

# Funnel Charts
st.markdown("""
* Funnel charts are often used to represent data in different stages of a business process. 
* It’s an important mechanism in Business Intelligence to identify potential problem areas of a process.
* For example, it’s used to observe the revenue or loss in a sales process for each stage. 
* A funnel chart has multiple phases and values associated with them.
* Here is a table that represents a user flow funnel for a app.
* The column named 'Values' represents the total number of users at that Phase
""")

st.write(
    "you can see code here [Repo](https://github.com/AhmedMMahrous/Deploy-Funnel-Charts-with-Streamlit-)")


# Loading dataset
app_data = pd.read_csv('app_info.csv')
st.write(app_data)

# storing the phases and no of people in the variable and
# also chosing the color that we are going to use in the plot
phases = app_data['Phases']
values = app_data['Values']
colors = ['blue', 'yellow', 'green', 'red']

num_phases = len(phases)

# setting value for plot width, section height and section gap
plot_width = 200
section_height = 50
section_gap = 10

# calculating the unit width and phase width of the funnel and
# then showing the width of the various section of the funnel
unit_width = plot_width / max(values)
phase_widths = [int(value * unit_width) for value in values]

# calculating the height of the funnel which is equal to the
# sum of all the height of the sections and section gaps
height = section_height * num_phases + section_gap * (num_phases - 1)
points = [phase_widths[0] / 2, height,
          phase_widths[1] / 2, height - section_height]


# extending the same thing for plotting the each section of the funnel
shapes = []
path_list = []
y_labels = []

# here we are using for loop for iterating through the section of the funnel
for i in range(num_phases):

    if (i == num_phases - 1):
        points = [phase_widths[i] / 2, height,
                  phase_widths[i] / 2, height - section_height]

    else:
        points = [phase_widths[i] / 2, height,
                  phase_widths[i + 1] / 2, height - section_height]

    path = 'M {0},{1} L {2},{3} L -{2},{3} L -{0},{1} Z'.format(*points)
    path_list.append(path)

    y_labels.append(height - (section_height / 2))

    height = height - (section_height + section_gap)


for i in range(num_phases):

    shape = {'type': 'path',
             'path': path_list[i],
             'fillcolor': colors[i],
             'line': {'color': colors[i]}
             }

    shapes.append(shape)


# setting trace for text labels for each section
label_trace = go.Scatter(x=[-170] * num_phases,

                         y=y_labels,

                         mode='text',

                         text=phases)
# setting trace for text values for each section
value_trace = go.Scatter(x=[170] * num_phases,

                         y=y_labels,

                         mode='text',

                         text=values)

data = [label_trace, value_trace]

layout = go.Layout(title='<i><b>App Purchase Funnel</i></b>',
                   titlefont=dict(size=15),
                   shapes=shapes,
                   showlegend=False,

                   xaxis=dict(showticklabels=False,
                              zeroline=True),
                   yaxis=dict(showticklabels=False,
                              zeroline=True)
                   )
fig = go.Figure(data=data,
                layout=layout)

#visu = offline.iplot(fig)
st.plotly_chart(fig)
