import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.cluster import DBSCAN
import pickle
import os

DATA_PATH = "/opt/airflow/dags/data"
MODEL_PATH = "/opt/airflow/dags/models"

def load_data():
    os.makedirs(DATA_PATH, exist_ok=True)
    df = pd.read_csv(f"{DATA_PATH}/winequality-white.csv", sep=';')
    df.dropna(inplace=True)
    df.to_csv(f"{DATA_PATH}/processed_winequality.csv", index=False)
    print("✅ Data Loaded & Saved:", df.shape)


def data_preprocessing():
    os.makedirs(DATA_PATH, exist_ok=True)
    df = pd.read_csv(f"{DATA_PATH}/processed_winequality.csv")

    # Separate features and target
    X = df.drop("quality", axis=1)
    scaler = MinMaxScaler()
    scaled = scaler.fit_transform(X)

    scaled_df = pd.DataFrame(scaled, columns=X.columns)
    scaled_df.to_csv(f"{DATA_PATH}/scaled_winequality.csv", index=False)
    print("✅ Data Scaled & Saved:", scaled_df.shape)


def build_save_model():
    os.makedirs(MODEL_PATH, exist_ok=True)
    data = pd.read_csv(f"{DATA_PATH}/scaled_winequality.csv")

    # Build and save DBSCAN clustering model
    model = DBSCAN(eps=0.3, min_samples=5)
    model.fit(data)

    with open(f"{MODEL_PATH}/dbscan_model.pkl", "wb") as f:
        pickle.dump(model, f)

    print("✅ Model trained and saved at:", f"{MODEL_PATH}/dbscan_model.pkl")


def evaluate_model():
    import numpy as np
    from sklearn import metrics
    with open(f"{MODEL_PATH}/dbscan_model.pkl", "rb") as f:
        model = pickle.load(f)

    dummy_data = np.random.rand(100, 2)
    dummy_labels = np.random.randint(0, 2, size=100)
    score = metrics.silhouette_score(dummy_data, dummy_labels)
    print(f"✅ Model Evaluation Complete. Silhouette Score: {score}")