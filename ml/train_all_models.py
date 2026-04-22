import os
import numpy as np
import pandas as pd
import mlflow
import matplotlib.pyplot as plt

from sqlalchemy import create_engine, text
from sklearn.metrics import mean_squared_error, mean_absolute_error
import xgboost as xgb

# ============================================================
# 1. MLflow tracking
# ============================================================
tracking_uri = os.getenv("MLFLOW_TRACKING_URI", "http://mlflow:5000")
mlflow.set_tracking_uri(tracking_uri)
mlflow.set_experiment("TimeSeries_Models_Training")

print(f"Using MLflow server: {tracking_uri}")

# ============================================================
# 2. Connexion PostgreSQL
# ============================================================
def get_engine():
    return create_engine(
        "postgresql+psycopg2://airbyte:airbyte@postgres-airbyte:5432/airbyte"
    )

# ============================================================
# 3. Charger CA journalier
# ============================================================
engine = get_engine()

query = text("""
    SELECT
        invoice_date::date AS ds,
        SUM(net_sales_amount::numeric) AS y
    FROM analytics.fct_sales
    WHERE invoice_date IS NOT NULL
      AND net_sales_amount IS NOT NULL
    GROUP BY ds
    ORDER BY ds
""")

df = pd.read_sql(query, engine)
df["ds"] = pd.to_datetime(df["ds"])
df["y"] = df["y"].astype(float)

print(f"Nombre total de points : {len(df)}")

# ============================================================
# 4. Features time-series
# ============================================================
def build_features(df, nlags=7):
    df = df.copy()
    for l in range(1, nlags + 1):
        df[f"lag_{l}"] = df["y"].shift(l)
    df["rolling_mean_7"] = df["y"].rolling(7).mean()
    df["rolling_std_7"] = df["y"].rolling(7).std()
    df = df.dropna()
    return df

df_feat = build_features(df)

train_size = int(len(df_feat) * 0.85)
df_train = df_feat.iloc[:train_size]
df_test  = df_feat.iloc[train_size:]

X_train = df_train.drop(columns=["ds", "y"])
y_train = df_train["y"]
X_test  = df_test.drop(columns=["ds", "y"])
y_test  = df_test["y"]

print(f"Taille train : {len(X_train)}, test : {len(X_test)}")

# ============================================================
# 5. MODELE XGBOOST (Sans registry)
# ============================================================
with mlflow.start_run(run_name="XGBoost_NetSales") as run:

    model = xgb.XGBRegressor(
        n_estimators=400,
        max_depth=6,
        learning_rate=0.05,
        subsample=0.9,
        colsample_bytree=0.8,
        objective="reg:squarederror",
        random_state=42,
    )

    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    # Metrics
    rmse = float(np.sqrt(mean_squared_error(y_test, y_pred)))
    mae  = float(mean_absolute_error(y_test, y_pred))

    mlflow.log_metric("RMSE", rmse)
    mlflow.log_metric("MAE", mae)

    print(f"\nRMSE = {rmse}")
    print(f"MAE  = {mae}")

    # Save model local + log
    model_file = "xgb_model.json"
    model.save_model(model_file)

    mlflow.log_artifact(model_file, artifact_path="model")

    # CSV predictions
    pred_df = pd.DataFrame({
        "date": df_test["ds"],
        "real_value": y_test,
        "predicted_value": y_pred
    })
    pred_df.to_csv("xgboost_predictions.csv", index=False)
    mlflow.log_artifact("xgboost_predictions.csv", artifact_path="predictions")

    # Plot
    plt.figure(figsize=(12,5))
    plt.plot(df["ds"], df["y"], label="Historique")
    plt.plot(df_test["ds"], y_test, label="Test réel")
    plt.plot(df_test["ds"], y_pred, label="Prédictions XGBoost")
    plt.axvline(df_test["ds"].iloc[0], linestyle="--", color="black")
    plt.legend()
    plt.grid()
    plt.tight_layout()
    plt.savefig("xgboost_plot.png")
    mlflow.log_artifact("xgboost_plot.png", artifact_path="plots")

print("\n🎉 Training Successfully Completed — No Errors.")
