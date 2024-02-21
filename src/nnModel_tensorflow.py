from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib
import math
import json
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Flatten, Conv1D, MaxPooling1D
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset


# flattenedData = []
#
with open("../datasets/wholeDataset.json") as wholeDataset:
    data = json.load(wholeDataset)
#
# for game in data[]:
#     for roundData in game["rounds"]:
#         flattenedRound = {
#             "map": game["map"],
#             "winner": game["winner"],
#             "loser": game["loser"],
#             "winnerScore": game["winnerScore"],
#             "loserScore": game["loserScore"]
#         }
#
# df = pd.json_normalize()
#
# print(df)

# Flatten the nested JSON structure
flat_data = []

for game in data:
    for round_data in game["rounds"]:
        ct_players = round_data["ct"]["players"]
        t_players = round_data["t"]["players"]

        for ct_player in ct_players:
            for t_player in t_players:
                flat_round = {
                    "map": game["map"],
                    # "winner": game["winner"],
                    # "loser": game["loser"],
                    "winnerScore": game["winnerScore"],
                    "loserScore": game["loserScore"],
                    "round": round_data["round"],
                    "ct_tBuyRatio": round_data["ct_tBuyRatio"],
                    "winningTeam": round_data["winningTeam"],
                    "ctWin": round_data["ctWin"],
                    # "ct_team": round_data["ct"]["team"],
                    "ct_startScore": round_data["ct"]["startScore"],
                    "ct_equipmentValue": round_data["ct"]["equipmentValue"],
                    "ct_mapControl": round_data["ct"]["mapControl"],
                    "ct_buy": round_data["ct"]["buy"],
                    # "ct_player_name": ct_player["name"],
                    "ct_player_kpr": ct_player["kpr"],
                    "ct_player_dpr": ct_player["dpr"],
                    "ct_player_adr": ct_player["adr"],
                    "ct_player_kast": ct_player["kast"],
                    "ct_player_rating": ct_player["rating"],
                    "ct_player_impact": ct_player["impact"],
                    "ct_player_utility": ct_player["utility"],
                    # "t_team": round_data["t"]["team"],
                    "t_startScore": round_data["t"]["startScore"],
                    "t_equipmentValue": round_data["t"]["equipmentValue"],
                    "t_mapControl": round_data["t"]["mapControl"],
                    "t_buy": round_data["t"]["buy"],
                    # "t_player_name": t_player["name"],
                    "t_player_kpr": t_player["kpr"],
                    "t_player_dpr": t_player["dpr"],
                    "t_player_adr": t_player["adr"],
                    "t_player_kast": t_player["kast"],
                    "t_player_rating": t_player["rating"],
                    "t_player_impact": t_player["impact"],
                    "t_player_utility": t_player["utility"],
                }
                flat_data.append(flat_round)

# Convert the flat data to a DataFrame
df = pd.DataFrame(flat_data)

for i in df.columns:
    if df[i].dtype == int:
        df[i] = df[i].astype(float)

df = pd.get_dummies(df, columns=["map", "winningTeam"])

# Now, df is a flattened representation of the JSON data suitable for use with a CNN
print(df)

X = np.asarray(df.drop("ctWin", axis = 1)).astype("float32")  # Features
y = np.asarray(df["ctWin"]).astype("float32")  # Target variable

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 42)

model = Sequential([

    # ranked in terms of highest accuracy
    # 64 filters/layer, filter size 3: 75.5%
    # 64 filters/layer, filter size 1: 72.7%
    # 64 filters/layer, filter size 5: 55.7%
    Conv1D(64, 1, activation = "relu", input_shape = (X_train.shape[1], 1)),
    MaxPooling1D(2),
    Flatten(),
    Dense(64, activation = "relu"),
    Dense(1, activation = "sigmoid")  # Binary classification, use "sigmoid" activation
])

model.compile(optimizer = "adam", loss = "binary_crossentropy", metrics = ["accuracy"])
model.fit(X_train, y_train, epochs = 4000, validation_split = 0.2)

test_loss, test_acc = model.evaluate(X_test, y_test)
print(f"Test Accuracy: {test_acc}")

# df.to_csv("../datasets/trainingDataset.csv")

# print(df)
# df = pd.get_dummies(df.drop(["round"], axis=1))
#
# # Check if "winningTeam" is present in the columns
# if "winningTeam" not in df.columns:
#     raise KeyError("Column "winningTeam" not found in the DataFrame.")
#
# # Standardize numerical features
# numerical_cols = ["ct_tBuyRatio", "ct_player_kpr", "ct_player_dpr", "ct_player_adr"]
# scaler = StandardScaler()
# df[numerical_cols] = scaler.fit_transform(df[numerical_cols])
#
# # Split into features and target variable
# X = df.drop("winningTeam", axis=1).values
# y = (df["winningTeam"] == "FaZe Clan").astype(int).values  # Binary encoding
#
# # Convert to PyTorch tensors
# X_tensor = torch.FloatTensor(X)
# y_tensor = torch.FloatTensor(y)
#
# # Split the data into training and testing sets
# X_train, X_test, y_train, y_test = train_test_split(X_tensor, y_tensor, test_size=0.2, random_state=42)
#
# # Reshape data for convolutional layer
# X_train = X_train.view(-1, 1, X_train.shape[1])
# X_test = X_test.view(-1, 1, X_test.shape[1])
#
# # Create a simple CNN model
# class CNNModel(nn.Module):
#     def __init__(self):
#         super(CNNModel, self).__init__()
#         self.conv1 = nn.Conv1d(1, 32, kernel_size=3)
#         self.pool = nn.MaxPool1d(2)
#         self.fc1 = nn.Linear(32 * ((X_train.shape[2] - 2) // 2), 64)
#         self.fc2 = nn.Linear(64, 1)
#         self.sigmoid = nn.Sigmoid()
#
#     def forward(self, x):
#         x = self.pool(F.relu(self.conv1(x)))
#         x = x.view(-1, 32 * ((X_train.shape[2] - 2) // 2))
#         x = F.relu(self.fc1(x))
#         x = self.sigmoid(self.fc2(x))
#         return x
#
# # Instantiate the model
# model = CNNModel()
#
# # Define loss function and optimizer
# criterion = nn.BCELoss()
# optimizer = optim.Adam(model.parameters(), lr=0.001)
#
# # Training loop
# num_epochs = 10
# for epoch in range(num_epochs):
#     model.train()
#     optimizer.zero_grad()
#     outputs = model(X_train)
#     loss = criterion(outputs, y_train.view(-1, 1))
#     loss.backward()
#     optimizer.step()
#
#     print(f"Epoch [{epoch+1}/{num_epochs}], Loss: {loss.item():.4f}")
#
# # Evaluation
# model.eval()
# with torch.no_grad():
#     test_outputs = model(X_test)
#     predicted_labels = (test_outputs >= 0.5).float()
#
#     # Calculate accuracy
#     accuracy = torch.sum(predicted_labels == y_test.view(-1, 1)).item() / len(y_test)
#     print(f"Test Accuracy: {accuracy:.4f}")
