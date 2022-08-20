import pandas as pd
import plotly.express as px
import streamlit as st

from feature_engineering import load_data, clean_data, filter_by_year

st.set_page_config(
    page_title="Explorateur d'OVNIs",
    page_icon='./images/logo_ovni.jpeg',
    layout='wide',
    initial_sidebar_state='auto',
)
st.title("Explorateur d'OVNIs")

# Loading
df = load_data()
df = clean_data(df)

selected_year_min, selected_year_max = st.sidebar.slider(
    label='Dates',
    min_value=int(df['event_date_year'].min()),
    max_value=int(df['event_date_year'].max()),
    value=(1950, 2000)
)

df_filtered = filter_by_year(df, selected_year_min, selected_year_max)

# # Feature Engineering
df_grouped_by_accident_severity_and_year = pd.DataFrame(df_filtered.groupby(by=['event_date_year', 'shape']).size(),
                                                        columns=['count']).reset_index()
df_grouped_by_accident_severity_and_dayname = pd.DataFrame(
    df_filtered.groupby(by=['event_date_day_name', 'shape']).size(),
    columns=['count']).reset_index()

# Display
## Dataframe
st.write(df)

## Map
st.subheader('Carte')
latitude = 40
longitude = -95
map_graph = px.scatter_mapbox(
    df_filtered,
    lat='latitude',
    lon='longitude',
    color='shape',
    hover_data={'latitude': True,
                'longitude': True,
                'event_date': True,
                'shape': True
                },
    color_continuous_scale=px.colors.sequential.Blackbody_r,
    size_max=15,
    zoom=3,
    opacity=1,
    center={'lat': latitude, 'lon': longitude},
    mapbox_style='carto-positron',
)
st.plotly_chart(map_graph, use_container_width=True)

## Line graph
st.subheader("Évolution du nombre d'OVNIs par année")
line_graph = px.line(df_grouped_by_accident_severity_and_year,
                     x='event_date_year',
                     y='count',
                     color='shape',
                     )
st.plotly_chart(line_graph, use_container_width=True)

## Histogram
st.subheader("Nombre d'OVNIs par jour de la semaine")
day_order = {'Date_Day_Name': ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']}
histogram_chart = px.histogram(df_grouped_by_accident_severity_and_dayname,
                               x='event_date_day_name',
                               y='count',
                               color='shape',
                               category_orders=day_order)
st.plotly_chart(histogram_chart, use_container_width=True)

# Final word
# is_button_clicked = st.sidebar.button(label='Display balloons')
# if is_button_clicked:
#     st.balloons()
