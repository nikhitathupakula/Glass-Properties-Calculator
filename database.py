import os
import sys
import pandas as pd


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


def configure_mendeleev():
    db_path = resource_path('mendeleev/elements.db')
    os.environ['MENDELEEV_DB'] = db_path


def load_csv_file():
    csv_path = resource_path('library.csv')
    try:
        df = pd.read_csv(csv_path)
        return df
    except Exception as e:
        raise


def main():
    configure_mendeleev()
    df = load_csv_file()


if __name__ == "__main__":
    main()
