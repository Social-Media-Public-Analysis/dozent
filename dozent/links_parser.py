import json
import pandas as pd
from typing import List


def _load_json_data() -> pd.DataFrame:
    file = open('twitter-archive-stream-links.json')
    data = json.load(file)
    return pd.DataFrame(data)


def _format_dates(df: pd.DataFrame) -> pd.DataFrame:
    df['day'] = df.apply(lambda x: int(x['day']) if x['day'] != 'NaN' else 1, axis=1)
    dates = pd.to_datetime(df[['year', 'month', 'day']])
    df['date'] = dates
    del df['year'], df['month'], df['day']
    return df


def _get_days_between(df: pd.DataFrame, start_date: str, end_date: str) -> pd.DataFrame:
    df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]
    return df


def get_links(start_date: str, end_date: str) -> List:
    df = _load_json_data()
    df = _format_dates(df)
    return _get_days_between(df, start_date=start_date, end_date=end_date)['link'].to_list()
