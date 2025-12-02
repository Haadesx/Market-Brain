import torch
import torch.nn as nn
import pandas as pd
import numpy as np
from app.ml.base import BaseModel

class LSTMNet(nn.Module):
    def __init__(self, input_dim, hidden_dim, output_dim=1, num_layers=1):
        super(LSTMNet, self).__init__()
        self.lstm = nn.LSTM(input_dim, hidden_dim, num_layers, batch_first=True)
        self.fc = nn.Linear(hidden_dim, output_dim)

    def forward(self, x):
        # x shape: (batch, seq_len, input_dim)
        out, _ = self.lstm(x)
        # Take last time step
        out = self.fc(out[:, -1, :])
        return out

class LSTMModel(BaseModel):
    def __init__(self, input_dim=10, hidden_dim=32, num_layers=1, seq_len=10, epochs=5):
        self.input_dim = input_dim
        self.hidden_dim = hidden_dim
        self.num_layers = num_layers
        self.seq_len = seq_len
        self.epochs = epochs
        self.model = LSTMNet(input_dim, hidden_dim, 1, num_layers)
        self.criterion = nn.MSELoss()
        self.optimizer = torch.optim.Adam(self.model.parameters(), lr=0.001)

    def _create_sequences(self, X: pd.DataFrame, y: pd.Series):
        xs, ys = [], []
        data = X.values
        target = y.values
        for i in range(len(data) - self.seq_len):
            x_seq = data[i:i+self.seq_len]
            y_val = target[i+self.seq_len]
            xs.append(x_seq)
            ys.append(y_val)
        return torch.tensor(np.array(xs), dtype=torch.float32), torch.tensor(np.array(ys), dtype=torch.float32).view(-1, 1)

    def train(self, X: pd.DataFrame, y: pd.Series, **kwargs):
        self.model.train()
        X_seq, y_seq = self._create_sequences(X, y)
        
        for epoch in range(self.epochs):
            self.optimizer.zero_grad()
            outputs = self.model(X_seq)
            loss = self.criterion(outputs, y_seq)
            loss.backward()
            self.optimizer.step()

    def predict(self, X: pd.DataFrame) -> np.ndarray:
        self.model.eval()
        # Note: Prediction requires sequence creation. 
        # For simplicity here, we assume X is passed in a way that we can form at least one sequence
        # or we handle the last sequence.
        # In a real pipeline, we'd need careful handling of the sliding window for inference.
        
        # Hack for now: just predict on the last sequence available in X
        if len(X) < self.seq_len:
            return np.array([0.0])
            
        data = X.values
        x_seq = torch.tensor(data[-self.seq_len:].reshape(1, self.seq_len, -1), dtype=torch.float32)
        with torch.no_grad():
            pred = self.model(x_seq)
        return pred.numpy().flatten()

    def save(self, path: str):
        torch.save(self.model.state_dict(), path)

    def load(self, path: str):
        self.model.load_state_dict(torch.load(path))
        self.model.eval()
