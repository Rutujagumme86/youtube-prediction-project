import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import pickle

# Load dataset
df = pd.read_csv("data/youtube.csv")

# Select columns
df = df[['view_count', 'like_count', 'comment_count', 'duration_seconds']]

# Features & Target
X = df[['like_count', 'comment_count', 'duration_seconds']]

# 🔥 IMPORTANT CHANGE (LOG SCALE)
y = np.log1p(df['view_count'])

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Model
model = RandomForestRegressor()
model.fit(X_train, y_train)

# Save model
pickle.dump(model, open("model.pkl", "wb"))

print("✅ Model trained and saved successfully!")