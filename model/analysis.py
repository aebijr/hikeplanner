import os
from dotenv import load_dotenv
from pymongo import MongoClient
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

load_dotenv()

uri = os.getenv("MONGO_DB_CONNECTION_STRING")

client = MongoClient(uri)
db = client["tracks"]
collection = db["tracks"]

data = list(collection.find())
df = pd.DataFrame(data)

# nur numerische Features auswählen
features = [
    "min_elevation",
    "max_elevation",
    "uphill",
    "downhill",
    "max_speed",
    "length_2d",
    "length_3d",
    "moving_time"
]

df = df[features]

# Korrelation berechnen
corr = df.corr()

# Heatmap plotten
plt.figure(figsize=(10,8))
sns.heatmap(corr, annot=True, cmap="coolwarm")
plt.title("Feature Correlation Heatmap")
plt.show()