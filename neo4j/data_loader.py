import pandas as pd

def load_data(csv_path, sample_size=None):
    print("Loading data...")
    if sample_size:
        df = pd.read_csv(csv_path, nrows=sample_size)
    else:
        df = pd.read_csv(csv_path)
    df['Vehicle_ID'] = df.apply(lambda row: f"{row['make']}_{row['model']}_{row.name}", axis=1)
    df.dropna(subset=['make', 'model'], inplace=True)
    print("Data loaded successfully")
    return df
