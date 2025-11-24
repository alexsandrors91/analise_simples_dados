# make_sample_data.py
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def make_sample(n=1000, path="data/sample_data.csv"):
    rng = pd.date_range(end=datetime.today(), periods=n, freq="D")
    df = pd.DataFrame({
        "date": rng,
        "category": np.random.choice(["A", "B", "C", "D"], size=n, p=[0.4,0.25,0.2,0.15]),
        "value": np.round(np.random.gamma(shape=2.0, scale=50.0, size=n), 2),
        "user_id": np.random.randint(1, 200, size=n),
        "flag": np.random.choice([0,1], size=n, p=[0.85, 0.15])
    })
    df.to_csv(path, index=False)
    print(f"Sample saved to {path}")

if __name__ == "__main__":
    make_sample()
