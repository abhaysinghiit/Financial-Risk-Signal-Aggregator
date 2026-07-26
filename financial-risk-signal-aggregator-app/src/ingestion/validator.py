import pandas as pd
from .schemas import *

def validate_dataframe(df, required_columns):

    errors = []

    if df.empty:

        errors.append("Dataset is empty.")

    missing = set(required_columns) - set(df.columns)

    if missing:

        errors.append(
            f"Missing columns: {list(missing)}"
        )

    return len(errors) == 0, errors

def validate_alerts(alerts):

    errors = []

    if len(alerts) == 0:

        errors.append("No alerts found.")

        return False, errors

    keys = set(alerts[0].keys())

    missing = set(ALERT_COLUMNS) - keys

    if missing:

        errors.append(
            f"Missing keys: {list(missing)}"
        )

    return len(errors) == 0, errors

def validate_news(text):

    if len(text.strip()) == 0:

        return False, ["News file is empty."]

    return True, []