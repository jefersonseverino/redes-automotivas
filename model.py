import pandas as pd
from sklearn.metrics import classification_report, roc_curve, auc
from sklearn.ensemble import IsolationForest
from sklearn.svm import OneClassSVM
import pickle
import matplotlib.pyplot as plt

def save_pickle(obj, path):
    with open(path, 'wb') as f:
        pickle.dump(obj, f)

def load_pickle(path):
    with open(path, 'rb') as f:
        return pickle.load(f)

def read_and_process_data(path):
    data = pd.read_csv(path, header=None, names=["id", "dlc", "payload", "time"], dtype=str)
    data['id'] = data['id'].apply(lambda x: int(str(x), 16) if isinstance(x, str) else x)
    data['payload'] = data['payload'].apply(lambda x: int(str(x), 16) if isinstance(x, str) else x)
    return data

def read_and_process_data_with_label(path):
    data = pd.read_csv(path, header=None, names=["id", "dlc", "payload", "time", "label"])
    data['id'] = data['id'].apply(lambda x: int(str(x), 16) if isinstance(x, str) else x)
    data['payload'] = data['payload'].apply(lambda x: int(str(x), 16) if isinstance(x, str) else x)
    return data

def train_and_save(data, algo='IsolationForest'):
    if algo == 'IsolationForest':
        model = IsolationForest(contamination=0.1, random_state=199)
    elif algo == 'OneClassSVM':
        model = OneClassSVM(kernel="rbf", nu=0.01)
    else:
        raise ValueError(f"Unsupported algorithm: {algo}")
    
    model.fit(data)
    save_pickle(model, f'{algo}_model.pkl')
    
def predict_anomalies(data, algo='IsolationForest'):
    model = load_pickle(f'{algo}_model.pkl')
    data['anomaly'] = model.predict(data)
    return data[data['anomaly'] == -1]

def predict_model(data, algo='IsolationForest'):
    model = load_pickle(f'{algo}_model.pkl')
    data['anomaly'] = model.predict(data)
    return data

def test_model(path, algo='IsolationForest'):
    test_data = read_and_process_data_with_label(path)
    print(test_data.shape)

    y_true = test_data['label']
    y_true = y_true.replace(0, -1)

    X_test = test_data.drop(columns=['label'])

    model = load_pickle(f'{algo}_model.pkl')

    y_pred = model.predict(X_test)

    print("\nClassification Report:")
    print(classification_report(y_true, y_pred, zero_division=0))

    scores = model.decision_function(X_test)
    fpr, tpr, _ = roc_curve(y_true, scores)
    roc_auc = auc(fpr, tpr)

    plt.figure()
    plt.plot(fpr, tpr, color='blue', lw=2, label=f'ROC curve (AUC = {roc_auc:.2f})')
    plt.plot([0, 1], [0, 1], color='gray', lw=2, linestyle='--')
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title(f'ROC Curve - {algo}')
    plt.legend(loc='lower right')
    plt.grid(True)
    plt.show()

    print(f"AUC: {roc_auc:.4f}")

def show_anomalies(anomalies):
    print(f"Detected {len(anomalies)} anomalies.")
    print(anomalies.head())
    
def detect_anomaly(row, algo='IsolationForest'):
    data = pd.DataFrame([row])
    anomalies = predict_anomalies(data, algo)
    return anomalies

def main():
    data = read_and_process_data('can_log.csv')
    train_and_save(data, algo='OneClassSVM')
    test_model('can_log_test.csv')

if __name__ == "__main__":
    main()