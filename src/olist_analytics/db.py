import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import seaborn as sns
import pandas as pd
from sqlalchemy import text
from dotenv import load_dotenv
from olist_analytics.handler.cursor import Connection


def setup():
    load_dotenv()

    engine = Connection().get_engine()

    def q(sql):
        with engine.connect() as conn:
            return pd.read_sql(text(sql), conn)

    plt.rcParams["figure.figsize"] = (12, 5)
    plt.rcParams["axes.spines.top"] = False
    plt.rcParams["axes.spines.right"] = False
    plt.rcParams["axes.grid"] = True
    plt.rcParams["grid.alpha"] = 0.3
    sns.set_palette("husl")

    print("Connected.")
    return engine, q
