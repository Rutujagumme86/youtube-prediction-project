import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import pickle

# Load dataset
df = pd.read_csv("data/youtube.csv")

# Select useful columns
df = df[['category_id', 'view_count', 'like_count', 'comment_count', 'duration_seconds']]

# Feature & target
X = df[['category_id', 'like_count', 'comment_count', 'duration_seconds']]
y = df['view_count']

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Model
model = RandomForestRegressor()
model.fit(X_train, y_train)

# Save model
pickle.dump(model, open("model.pkl", "wb"))

print("Model trained & saved!")