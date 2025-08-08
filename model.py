import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import IsolationForest
from sklearn.svm import OneClassSVM
import pickle

def save_pickle(obj, path):
    with open(path, 'wb') as f:
        pickle.dump(obj, f)

def load_pickle(path):
    with open(path, 'rb') as f:
        return pickle.load(f)

def read_and_process_data(path):
    data = pd.read_csv(path, header=None, names=["id", "dlc", "payload", "time"])
    data['id'] = data['id'].apply(lambda x: int(str(x), 16) if isinstance(x, str) else x)
    data['payload'] = data['payload'].apply(lambda x: int(str(x), 16) if isinstance(x, str) else x)
    X = data[['id', 'dlc', 'payload', 'time']].copy()
    return pd.DataFrame(X, columns=X.columns)

def train_and_save(data, algo='IsolationForest'):
    if algo == 'IsolationForest':
        model = IsolationForest(contamination=0.1, random_state=199)
    elif algo == 'OneClassSVM':
        model = OneClassSVM(gamma='scale', nu=0.1)
    else:
        raise ValueError(f"Unsupported algorithm: {algo}")
    
    model.fit(data)
    save_pickle(model, f'{algo}_model.pkl')
    
def predict_anomalies(data, algo='IsolationForest'):
    model = load_pickle(f'{algo}_model.pkl')
    data['anomaly'] = model.predict(data)
    return data[data['anomaly'] == -1]

def show_anomalies(anomalies):
    print(f"Detected {len(anomalies)} anomalies.")
    print(anomalies.head())
    
def detect_anomaly(row, algo='IsolationForest'):
    data = pd.DataFrame([row])
    print(row['payload'])
    # data = read_and_process_data("can_log.csv")
    anomalies = predict_anomalies(data, algo)
    return anomalies

def main():
    data = read_and_process_data('can_log.csv')
    train_and_save(data, algo='IsolationForest')

if __name__ == "__main__":
    main()