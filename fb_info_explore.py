""" 
David Scales
DS3000 - HW3
Professor Rachlin
10/17/2024
"""

import panel as pn
import plotly.express as px
from fb_info_api import FBAPI
import pandas as pd

pn.extension()

api = FBAPI()

#Necessary modules are imported, panel is initialized, and an instance of 'api' is defined for use of FBAPI (other submitted file)

api.load_df('Annex_A.xlsx')
fb_df = api.make_fb_df()

api.load_df('Annex_B.xlsx', 'B8')
employment_df = api.make_employment_df()

api.load_df('Annex_B.xlsx', 'B2')
education_df = api.make_education_df()

api.load_df('Annex_C.xlsx', 'C1')
poverty_df = api.make_poverty_df()

api.load_df('Annex_E.xlsx', 'E2')
literacy_df = api.make_literacy_df()

#api is used to load several data frames, data exists across 4 files (2 tabs in Annex_B), so api is loaded for each necessary instance

category_types = ['Employment', 'Education', 'Poverty', 'Literacy']
#category_types is set to later represent tabs on dashboard

# All of the widgets that require human interaction are below;
fb_options = [x for x in list(fb_df.columns) if x != 'Country']
#list of all options for home page map are defined (no use to plot country on globe)

fb_category = pn.widgets.Select(name="Category Displayed on Globe", options=fb_options)

#Allows user to select a category to be displayed on globe, from fb_df

bar_countries = pn.widgets.CrossSelector(name='Countries to Consider', value=[], options=list(fb_df['Country']), width=300)
resident_type = pn.widgets.RadioButtonGroup(name='Resident Type', options=['Foreign Born', 'Native Born', 'Both'], button_type='success', value='Both')
#Two feautres relevant to the dashboards bar graphs, choosing which countries to evaluate, and which resident types

width_slider = pn.widgets.IntSlider(name="Plot Width", start=500, end=1250, step=50, value=800)
height_slider = pn.widgets.IntSlider(name="Plot Height", start=300, end=750, step=50, value=500)

#Really not necessary to the function of the dashboard, but allows the user to adjust the sizing of the plot

def get_relevant_countries(category, resident):
    """ Searches through dataframes to gather list of countries with data for given category and resident type, 
    designed so CrossSelector doesn't show invalid countries as options
    Arguments:
        Category (str): Name of the category or tab currently being viewed
        Resident (str): Name of the resident type currently being viewed
    Returns:
        filtered_countries (lst): list of all countries applicable
    """
    df_dict = {'Employment': employment_df, 'Education': education_df,'Poverty': poverty_df,'Literacy': literacy_df}
    df = df_dict[category]

    #df_dict represents all category types, such that df can be built from just category name

    if resident == 'Both':
        relevant_columns = [x for x in list(fb_df.columns) if x != 'Country']
    else:
        relevant_columns = [x for x in df.columns if resident in x]
    
    #conditional statement to gather list of columns that are relevant to the current resident type, if both, it's all but country

    filtered_countries = []
    for x in range(len(df)):
        row = df.iloc[x]  
        for col in relevant_columns:
            if row[col] != '..':
                
                # '..' represents the placeholder for an empty value, doesn't use nan

                filtered_countries.append(row['Country'])

                break
    
    #Using nested loops, appends to filtered_countries based on countries with values for the relevant columns
    
    return filtered_countries

def get_world_viz(fb_category):
    """ Taking a specific column name from fb_df, creates a choropleth plotly figure that is colorscaled
    Arguments:
        fb_category (str): a column name from the fb_df dataframe, to be shown in the choropleth world map
    Returns:
        fig (px): a plotly express object to be shown as a figure
    """
    fig = px.choropleth(
        fb_df, 
        locations='Country', 
        locationmode='country names',
        color=fb_category, 
        hover_name='Country',
        color_continuous_scale='Reds', 
        projection='natural earth',
        title=f'{fb_category} for OECD Countries',
        width = 1000,
        height = 600

        # f string enables category to be shown in title
    )
    
    fig.update_coloraxes(colorbar=dict(len=0.5, thickness=10, x=1.00, y=0.5,))
    #Updated the colorscale of the graph - purely visual
                    
    return fig

# The following is a markdown panel intended to be shown on the sidebar alongside the world map
world_map_text = pn.pane.Markdown("""
## Introduction to OECD and the Dataset

The Organisation for Economic Co-operation and Development (OECD) was founded in 1960 and now contains 38 countries across the world, including the U.S., Mexico, Australia, Chile, and the majority of the EU.

* The OECD has operated under the goal of approaching socioeconomic problems with firm research and data, and then making that data publicy available, such that primarily participating nations can enact policy domestically that is backed by firm evidence.
                                  
* With some of the OECD's members including countries like the U.S., Turkey, and Sweden, some of the countries  with the highest immigration rates, this provides valuable data on the quality of life of immigrants after settling into their destination countries.

* Use the selector just below this text to change the data represented on the globe to the right, to gain a general understanding of foreign-born populations
in OECD countries. After this, feel free to use the tabs to directly compare statistics comparing foreign-born populations with their native born counterparts in employment, education, poverty, and literacy.
                                  """)

def get_bar_viz(countries, category, resident, width, height):
    """ 
    Arguments:
        countries (lst): A list of relevant countries to be included in a bar chart
        category (str): A category name to locate appropriate df
        resident (str): A resident type, to show which columns in the df are applicable
        width (int): width of graph
        height (int): height of graph
    Returns:
        fig (px): a plotly express object, to be shown
    
    """
    if len(countries) == 0:
        return "No countries currently selected, use the selector in the sidebar!"
    #As the CrossSelector starts without anything selected, this allows the graph to not just be empty upon opening

    df_dict = {'Employment': employment_df, 'Education': education_df, 'Poverty': poverty_df, 'Literacy': literacy_df}
    df = df_dict[category]
    #Again, allows df to be established just based on inputted category string

    filtered_df = df[df['Country'].isin(countries)]
    
    #Filters df such that only countries selected by the CrossSelector are shown

    if resident == 'Both':
        columns = [x for x in list(filtered_df.columns) if x != 'Country']
        title = f'Foreign and Native Born {category} Comparison for Selected Countries'
        
        # if resident type is both, takes all columns besides country, and generates title

        melt_df = filtered_df.melt(id_vars=['Country'], value_vars=columns, var_name='Resident Type', value_name='Value')
        
        # melt_df is created by using .melt method; such that from different countries' FB and NB values can be plotted side by side

        fig = px.bar(
            melt_df,
            x='Country',
            y='Value',
            color='Resident Type',
            barmode='group',
            title=title,
            text='Value'
        )
        #Bar graph figure is created, with melt_df, title is added accordingly
    else:
        relevant_columns = [x for x in filtered_df.columns if str(resident) in x]
        title = f'{resident} {category} Comparison for Selected Countries'
        
        #Columns are generated differently, only including if resident type in in it's name, title is constructed.

        fig = px.bar(
            data_frame=filtered_df,
            x='Country',
            y=relevant_columns[0],
            title=title,
            text=relevant_columns[0]
        )
        #Plotly bar graph is again created, titled respectively, with x axis as country names

    fig.update_layout(
        width=width,  
        height=height,  
        xaxis_title="Country",
        yaxis_title="Value",
    )
    # figure is updated according to inputted width and height, and is labeled, for the fig to be returned
    return fig

#manual creation of each of the tabs of the dashboard, bound to their relevant columns and category, .param.value allowing particular value to be sent
tb_world_map = pn.bind(get_world_viz, fb_category)
tb_employment = pn.bind(get_bar_viz, bar_countries.param.value, 'Employment', resident_type.param.value, width_slider.param.value, height_slider.param.value)
tb_education = pn.bind(get_bar_viz, bar_countries.param.value, 'Education', resident_type.param.value, width_slider.param.value, height_slider.param.value)
tb_poverty = pn.bind(get_bar_viz, bar_countries.param.value, 'Poverty', resident_type.param.value, width_slider.param.value, height_slider.param.value)
tb_literacy = pn.bind(get_bar_viz, bar_countries.param.value, 'Literacy', resident_type.param.value, width_slider.param.value, height_slider.param.value)

#Only way I was able to add this into layout with making more complex layout variable, found through panel's website, .Tabs acts as almost dictionary of tabs to be inputted to layout
tabs = pn.Tabs(
    ("World Map", tb_world_map),
    ("Employment", tb_employment),
    ("Education", tb_education),
    ("Poverty", tb_poverty),
    ("Literacy", tb_literacy),
    active=0
)

# The following are markdown panes, each representing a string to be included in each tab's sidebar
sidebar_note1 = pn.pane.Markdown("""
# Employment Data
* Represents unemployment percentage across OECD countries
* Use the below options to select countries to be included, and resident types
* Note the inclusion of 'EU Total' and 'OECD Total' in the countries list
                                """)
sidebar_note2 = pn.pane.Markdown("""
# Education Data
* Represents ISCED across OECD countries, standing for International Standard Classification of Education
* ISCED score of 0-2 is capping at lower secondary education, 3-4 at post-secondary education, while 5+ represents some measure beyond high school (trade, bachelors, phd, ect)
* Use the below options to select countries to be included, and resident types
* Note the inclusion of 'EU Total' and 'OECD Total' in the countries list
                                 """)
sidebar_note3 = pn.pane.Markdown("""
# Poverty Data
* Represents the percentage of populations living below the poverty line across OECD countries
* Use the below options to select countries to be included, and resident types
* Note the inclusion of 'EU Total' and 'OECD Total' in the countries list                              
                                                                  """)
sidebar_note4 = pn.pane.Markdown("""
# Literacy Data
* Represents the PISA score across OECD countries, a test-based indication of how well educated and literate a populous is.
* Use the below options to select countries to be included, and resident types
* Note the inclusion of 'EU Total' and 'OECD Total' in the countries list
                                 """)

def get_sidebar(active_tab):
    """ Takes a specific tab, and returns the releveant sidebar panel Column object
    Arguments:
        active_tab (int): the integer relating to a specific tab
    Returns:
        pn.Column (pn): a pn column relating to a specific tab's sidebar
    """
    if active_tab == 0:  
        return pn.Column(world_map_text, fb_category)
    elif active_tab == 1:
        return pn.Column(sidebar_note1, bar_countries, resident_type, width_slider, height_slider)
    elif active_tab == 2:
        return pn.Column(sidebar_note2, bar_countries, resident_type, width_slider, height_slider)
    elif active_tab == 3:
        return pn.Column(sidebar_note3, bar_countries, resident_type, width_slider, height_slider)
    elif active_tab == 4:
        return pn.Column(sidebar_note4, bar_countries, resident_type, width_slider, height_slider)
    
#using .param.active to relay which tab's object is currently visible, builds sidebar according to tab
sidebar = pn.bind(get_sidebar, tabs.param.active)

layout = pn.template.FastListTemplate(
    title="Immigrant Equality Analysis for OECD Countries",
    sidebar=sidebar,
    theme_toggle=False,
    main=tabs,
    header_background='#00008B'
)
#Layout is built, using sidebar and tabs, and is titled and 

layout.servable()
layout.show()

#Layout is shown.