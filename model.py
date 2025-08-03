import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import IsolationForest

def read_and_process_data(path):
    data = pd.read_csv(path, header=None, names=["id", "dlc", "payload"])
    data['id'] = data['id'].apply(lambda x: int(str(x), 16) if isinstance(x, str) else x)
    data['payload'] = data['payload'].apply(lambda x: int(str(x), 16) if isinstance(x, str) else x)
    X = data[['id', 'dlc', 'payload']].copy()
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    return pd.DataFrame(X_scaled, columns=X.columns)

def detect_anomalies(data, algo='IsolationForest'):
    if algo == 'IsolationForest':
        model = IsolationForest(contamination=0.1, random_state=199)
    else:
        raise ValueError(f"Unsupported algorithm: {algo}")
    
    model.fit(data)
    data['anomaly'] = model.predict(data)
    return data[data['anomaly'] == -1]  # Return only anomalies

def show_anomalies(anomalies):
    print(f"Detected {len(anomalies)} anomalies.")
    print(anomalies.head())
    
def detect_anomaly(row, algo='IsolationForest'):
    data = pd.DataFrame([row])
    data = read_and_process_data(data)
    anomalies = detect_anomalies(data, algo)
    return anomalies

def main():
    data = read_and_process_data('can_log.csv')
    anomalies = detect_anomalies(data)
    show_anomalies(anomalies)

if __name__ == "__main__":
    main()