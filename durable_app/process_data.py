import dask.dataframe as dd
from pyod.models.iforest import IForest
from sklearn.preprocessing import StandardScaler
import pandas as pd

def main(blob_url: str) -> dict:
    # Simulated chunking (replace with blob download in prod)
    df = dd.read_csv("sample_data.csv")  # Use local CSV or blob client in prod

    df = df.select_dtypes(include='number')
    data = df.compute()

    scaler = StandardScaler()
    data_scaled = scaler.fit_transform(data)

    model = IForest()
    model.fit(data_scaled)

    preds = model.predict(data_scaled)
    outlier_count = sum(preds)

    return {
        "chunk": blob_url,
        "outliers": int(outlier_count),
        "total": len(preds)
    }
