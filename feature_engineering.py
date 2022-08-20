import pandas as pd
import streamlit as st


@st.cache
def load_data() -> pd.DataFrame:
    df = pd.read_csv('data/clean/ufo.csv')
    return df


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    df = df.dropna().reset_index(drop=True)
    df['event_date'] = pd.to_datetime(df['event_date'])
    df['declaration_date'] = pd.to_datetime(df['declaration_date'])
    # df['event_date_day_number'] = df['event_date'].dt.day
    df['event_date_year'] = df['event_date'].dt.year
    df['event_date_day_name'] = df['event_date'].dt.day_name()
    return df

def filter_by_year(data: pd.DataFrame, min_year: int, max_year: int) -> pd.DataFrame:
    return data[(data['event_date_year'] >= min_year) & (data['event_date_year'] <= max_year)]