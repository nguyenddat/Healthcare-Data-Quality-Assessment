# factory.py

import random
import string
from datetime import timedelta
from sqlalchemy import create_engine

import numpy as np
import pandas as pd
# ID / FOREIGN KEY
def sequential_ids(n, start=1):
    return np.arange(start, start + n)
def sample_fk(ids, size, replace=True):
    return np.random.choice(ids, size=size, replace=replace)
# RANDOM
def random_choice(values, size, replace=True):
    return np.random.choice(values, size=size, replace=replace)
def random_datetime(start, end, size=None):
    """
    size=None  -> trả về 1 Timestamp
    size=int   -> trả về list Timestamp
    """
    start = pd.Timestamp(start)
    end = pd.Timestamp(end)

    if size is None:
        return start + pd.to_timedelta(
            random.randint(0, int((end - start).total_seconds())),
            unit="s",
        )

    seconds = np.random.randint(
        0,
        int((end - start).total_seconds()) + 1,
        size=size,
    )

    return [
        start + pd.to_timedelta(s, unit="s")
        for s in seconds
    ]
def random_datetime_after(base, min_days=0, max_days=None, days=None):
    if days is not None:
        min_days = days
        max_days = days
    if max_days is None:
        max_days = min_days

    def _one(dt, min_d=min_days, max_d=max_days):
        if isinstance(min_d, (np.ndarray, list, pd.Series)):
            min_d = int(np.min(min_d))
        if isinstance(max_d, (np.ndarray, list, pd.Series)):
            max_d = int(np.max(max_d))
        return dt + pd.Timedelta(days=np.random.randint(int(min_d), int(max_d) + 1))

    if isinstance(base, (list, np.ndarray, pd.Series)):
        return [_one(x) for x in base]

    return _one(base)
# PERSON
_FIRST = [
    "Nguyễn", "Trần", "Lê", "Phạm",
    "Hoàng", "Huỳnh", "Võ", "Đặng",
    "Bùi", "Đỗ"
]

_MIDDLE = [
    "Văn", "Thị", "Minh",
    "Quốc", "Thanh", "Ngọc"
]

_LAST = [
    "An", "Bình", "Hương", "Trang",
    "Lan", "Hà", "Nam", "Khánh",
    "Phúc", "Long", "Linh", "Mai"
]
def random_person_name():
    return " ".join([
        random.choice(_FIRST),
        random.choice(_MIDDLE),
        random.choice(_LAST),
    ])
# NULL
def inject_null(df, column, rate):
    mask = np.random.rand(len(df)) < rate
    df.loc[mask, column] = pd.NA
    return df
# OUTPUT
def preview(df, name, n=5):
    print(f"\n{name}")
    print(df.head(n))
    print(df.shape)
def export_csv(df, name, folder="output"):
    import os

    os.makedirs(folder, exist_ok=True)
    df.to_csv(
        f"{folder}/{name}.csv",
        index=False,
        encoding="utf-8-sig",
    )

engine = create_engine("postgresql://user:pass@localhost:5432/healthcare_sim")
def export_db(df, name):
    df.to_sql(name, engine, if_exists="replace", index=False)