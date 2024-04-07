# Given the datasets table history and status changes,
# create a new dataset that shows the start and end of each membership.
import os
from pathlib import Path
import re

import pandas as pd


def extract_value(x, name):
    matches = re.findall(r'(?P<attribute>[a-zA-Z_]*)-\^!\^!\^-(?P<oldValue>[a-zA-Z-\s\:\d]*)\s?-\^!\^!\^-(?P<newValue>[a-zA-Z-\s\:\d]*)\s?@#@#@#', x)
    if matches:
        for attr, old_value, new_value in matches:
            if attr == name:
                return old_value, new_value


def attempt_1(status_changes_df, table_history_df):
    # only look at rows with start dates
    valid_table_history_df = table_history_df[table_history_df["changes"].str.contains("membership_start_date")]
    final_table = pd.DataFrame(columns=['customer_id', 'status', 'start_date', 'end_date'])
    for index, row in valid_table_history_df.iterrows():
        old_start_date, start_date = extract_value(row["changes"], "membership_start_date")
        print(start_date)
        if start_date.strip() != "0000-00-00":
            customer_id_status_changes = status_changes_df[status_changes_df["customer_id"] == row["customer_id"]]
            customer_id_status_changes = customer_id_status_changes[customer_id_status_changes["status"] != "OK"]
            customer_id_status_changes["start_date"] = pd.to_datetime(customer_id_status_changes["start_date"])
            customer_id_status_changes = customer_id_status_changes[(customer_id_status_changes["start_date"] > start_date)]
            val = customer_id_status_changes.iloc[0]
            final_table.loc[len(final_table.index)] = [val['customer_id'], val['status'], start_date, val['start_date']]
    print(final_table)


def attempt_2(status_changes_df: pd.DataFrame, table_history_df: pd.DataFrame) -> pd.DataFrame:
    """Using the status-changes.csv and table-history.csv data tables
    find the customers whose membership expired or cancelled and the reason

    :param status_changes_df: DataFrame of the status-changes.csv
    :param table_history_df: DataFrame of the table-history.csv
    :return: The dataframe of the customers that membership ended
    """
    # Creates the final table with the column names we want to display
    final_table = pd.DataFrame(columns=['customer_id', 'start_date', 'end_date', 'end_reason'])
    # gets all the starting date rows in the status-change table
    start_dates = status_changes_df[status_changes_df["status"] == "OK"]
    for index, row in start_dates.iterrows():
        # Filters the table to find the same customer and
        # looks for a status change that would cause cancellation or freeze
        customer_id_status_changes = status_changes_df[status_changes_df["customer_id"] == row["customer_id"]]
        customer_id_status_changes = customer_id_status_changes[customer_id_status_changes["status"] != "OK"]
        # customer_id_status_changes["start_date"] = pd.to_datetime(customer_id_status_changes["start_date"])
        # Only grabs the status' that changed after the start date
        customer_id_status_changes = customer_id_status_changes[(customer_id_status_changes["start_date"] > row["start_date"])]
        if len(customer_id_status_changes.index):
            # we grab the most recent one after the start date
            val = customer_id_status_changes.iloc[0]
            # if terminated, check customer_id and post date in table history and find row with mem_exp_date
            # if that row exists then the membership expired else we can say it was cancelled
            if val["status"].strip() == "TERMINATE":
                terminate_df = table_history_df[(table_history_df["customer_id"] == val["customer_id"]) & (table_history_df["postdate"].str.contains(row["postdate"].split(" ")[0]))]
                if len(terminate_df.index):
                    terminate_df = terminate_df[terminate_df["changes"].str.contains("membership_exp_date")]
                    end_reason = "expire" if len(terminate_df.index) else "cancel"
                else:
                    end_reason = "cancel"
            else:
                end_reason = "freeze"
            final_table.loc[len(final_table.index)] = [val['customer_id'], row["start_date"], val['start_date'], end_reason]
    return final_table


if __name__ == "__main__":
    dir_path = os.path.dirname(os.path.realpath(__file__))
    parent_path = Path(dir_path).parent

    status_changes_df = pd.read_csv(os.path.join(parent_path, "data-sources/status-changes.csv"))
    table_history_df = pd.read_csv(os.path.join(parent_path, "data-sources/table-history.csv"))

    result = attempt_2(status_changes_df, table_history_df)
    print(result)
