import pandas as pd
import re


def clean_values(value, column_name=None):
    if pd.isna(value) or value == "":
        return None

    value = str(value).strip()

    if column_name and "date" in column_name.lower():
        try:
            parsed_date = pd.to_datetime(value, errors="coerce", dayfirst=True)
            if not pd.isna(parsed_date):
                return parsed_date.strftime("%Y-%m-%d")
        except Exception:
            pass

    value = value.replace("'", "''")
    value = value.replace("\\", "\\\\")
    value = re.sub(r"[\n\r\t]+", " ", value)

    return value


def read_csv_with_fallback(file):
    try:
        df = pd.read_csv(file, delimiter="\t")
        if len(df.columns) == 1:
            file.seek(0)
            df = pd.read_csv(file, delimiter=",")
        return df
    except Exception as e:
        raise ValueError(f"CSV read error: {str(e)}")
