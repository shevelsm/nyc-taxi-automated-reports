from io import BytesIO

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


fig, ax = plt.subplots(2, 2, sharey=True, figsize=(11.7, 8.3))


def make_pdf_report() -> BytesIO:
    pdf_buffer = BytesIO()
    plt.savefig(pdf_buffer, format="pdf", bbox_inches="tight")
    fig.clf()
    return pdf_buffer


def prepare_weekday_trips_fig(taxi_df: pd.DataFrame, jfk_df: pd.DataFrame):
    days = {0: "Mo", 1: "Tu", 2: "Wed", 3: "Thu", 4: "Fri", 5: "Sat", 6: "Sun"}
    week_days = list(days.values())

    counts_days_jfk = pd.crosstab(index=jfk_df["pickup_weekday"], columns="count")
    counts_days_ratio_jfk = counts_days_jfk.loc[:, "count"] / len(jfk_df)

    counts_days_all = pd.crosstab(index=taxi_df["pickup_weekday"], columns="count")
    counts_days_ratio_all = counts_days_all.loc[:, "count"] / len(taxi_df)

    df_rt_jfk = pd.DataFrame()
    df_rt_jfk_total = pd.DataFrame()

    df_rt_jfk["Weekdays"] = week_days
    df_rt_jfk["Trips Ratio"] = round(counts_days_ratio_jfk, 3) * 100
    df_rt_jfk_total["Weekdays"] = list(days.values())
    df_rt_jfk_total["Trips Ratio"] = round(counts_days_ratio_all, 3) * 100

    ax[0, 0].set_title(
        "Ratio of weekdays in the airport trips", fontsize=12, fontweight="bold"
    )
    ax[0, 1].set_title(
        "Ratio of weekdays in total trips", fontsize=12, fontweight="bold"
    )

    sns.barplot(data=df_rt_jfk, x="Weekdays", y="Trips Ratio", ax=ax[0, 0])
    sns.barplot(data=df_rt_jfk_total, x="Weekdays", y="Trips Ratio", ax=ax[0, 1])

    ax[0, 0].set_ylabel("Ratio of Trips %", fontsize=10)
    ax[0, 1].set_ylabel("")
    ax[0, 0].set_xlabel("")
    ax[0, 1].set_xlabel("")
    ax[0, 0].bar_label(ax[0, 0].containers[0])
    ax[0, 1].bar_label(ax[0, 1].containers[0])


def prepare_hour_trips_fig(taxi_df: pd.DataFrame, jfk_df: pd.DataFrame):
    count_hours_jfk = pd.crosstab(index=jfk_df["pickup_hour"], columns="count")
    counts_hours_ratio_jfk = count_hours_jfk.loc[:, "count"] / len(jfk_df) * 100

    count_hours_all = pd.crosstab(index=taxi_df["pickup_hour"], columns="count")
    counts_hours_ratio_all = count_hours_all.loc[:, "count"] / len(taxi_df) * 100

    sns.set_style("darkgrid")
    sns.lineplot(data=counts_hours_ratio_jfk, ax=ax[1, 0])
    sns.lineplot(data=counts_hours_ratio_all, ax=ax[1, 1])
    ax[1, 0].set_title(
        "Ratio of times in airport trips", fontsize=12, fontweight="bold"
    )
    ax[1, 1].set_title(
        "Ratio of times in the total trips", fontsize=12, fontweight="bold"
    )
    ax[1, 0].set_xlabel("Pick up hour")
    ax[1, 1].set_xlabel("Pick up hour")
    ax[1, 0].set_xticks(
        np.arange(min(taxi_df["pickup_hour"]), max(taxi_df["pickup_hour"]) + 1, 1.0)
    )
    ax[1, 1].set_xticks(
        np.arange(min(taxi_df["pickup_hour"]), max(taxi_df["pickup_hour"]) + 1, 1.0)
    )

    sns.set_context("notebook", font_scale=1.3, rc={"lines.linewidth": 2.5})
    ax[1, 0].set_ylabel("Ratio of Trips %")
    ax[1, 1].set_ylabel("")
