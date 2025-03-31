# -*- coding: utf-8 -*-
"""mlp_eg.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1H6TxOjdmH7l7OxVRh041qPZId_PBu1fs

1. Load the Required Libraries
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.utils import to_categorical
from sklearn.metrics import classification_report, confusion_matrix

"""Load IRIS Data"""

from google.colab import drive
drive.mount('/content/gdrive')
csvfile = 'gdrive/My Drive/_2024/MLOPS/programs/dataset/iris.csv'
df=pd.read_csv(csvfile)
df = df.dropna()
df.head()

"""Check the statistics"""

df.describe()

X = df[['SepalLengthCm', 'SepalWidthCm', 'PetalLengthCm', 'PetalWidthCm']]
y = df['Species']

"""Use scaler to have the data in the normal range"""

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

"""Label Encoding for target variable"""

le = LabelEncoder()
y_encoded = le.fit_transform(y)

"""Convert to one hot encoding"""

y_one_hot = to_categorical(y_encoded, num_classes=3)

X_train, X_test, y_train, y_test = train_test_split(X_scaled, y_one_hot, test_size=0.2, random_state=42)

model = Sequential([
    Dense(12, activation='relu', input_dim=4),
    Dense(8, activation='relu'),
    Dense(3, activation='softmax')  # 3 output classes
])

model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

mlp = model.fit(X_train, y_train, epochs=100, batch_size=5, validation_data=(X_test, y_test))

loss, accuracy = model.evaluate(X_test, y_test)
print(f"Test Accuracy: {accuracy:.4f}")

import matplotlib.pyplot as plt
plt.plot(mlp.history['accuracy'], label='Train Accuracy')
plt.plot(mlp.history['val_accuracy'], label='Validation Accuracy')
plt.xlabel('Epochs')
plt.ylabel('Accuracy')
plt.title('Model Accuracy vs. Epoch')
plt.legend()
plt.show()

y_pred_probs = model.predict(X_test)  #  probability distributions
y_pred_classes = np.argmax(y_pred_probs, axis=1)  # Convert to class labels

# Convert y_test from one-hot to class labels
y_test_classes = np.argmax(y_test, axis=1)

print("\nClassification Report:")
print(classification_report(y_test_classes, y_pred_classes, target_names=le.classes_))

cm = confusion_matrix(y_test_classes, y_pred_classes)

plt.figure(figsize=(6, 5))
sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", xticklabels=le.classes_, yticklabels=le.classes_)
plt.xlabel("Predicted Label")
plt.ylabel("True Label")
plt.title("Confusion Matrix")
plt.show()

print("Confusion Matrix:\n", cm)

"""Saving as .h5 *file*"""

import joblib
from tensorflow.keras.models import load_model

model.save("mlp_model.h5")

"""Predict the value of Xtest"""

from tensorflow.keras.models import load_model
import numpy as np

loaded_model = load_model("mlp_model.h5")

y_pred_probs = loaded_model.predict(X_test)  # Probability distributions
y_pred_classes = np.argmax(y_pred_probs, axis=1)
print(y_test_classes)
print(y_pred_classes)

sample_input = np.array([[5.1, 3.5, 1.4, 1.2]])

y_pred_probs = loaded_model.predict(sample_input)
y_pred_probs

y_pred_class = np.argmax(y_pred_probs, axis=1)
y_pred_class

print(f"Predicted class: {y_pred_class[0]}")

import streamlit as st
import numpy as np
import joblib
from tensorflow.keras.models import load_model
from sklearn.preprocessing import StandardScaler
import pandas as pd

# Load the trained model
model = load_model("mlp_model.h5")

# Load dataset to fit scaler (Ensure the same dataset is used for consistency)
df = pd.read_csv("iris.csv")  # Provide the correct dataset file
df = df.dropna()
X = df[['SepalLengthCm', 'SepalWidthCm', 'PetalLengthCm', 'PetalWidthCm']]

scaler = StandardScaler()
scaler.fit(X)
joblib.dump(scaler, "scaler.pkl")  # Save the scaler
scaler = joblib.load("scaler.pkl")  # Load the scaler

# Function to get user inputs
def get_input():
    sepal_length = st.number_input("Sepal Length (cm)", min_value=0.0, format="%.2f")
    sepal_width = st.number_input("Sepal Width (cm)", min_value=0.0, format="%.2f")
    petal_length = st.number_input("Petal Length (cm)", min_value=0.0, format="%.2f")
    petal_width = st.number_input("Petal Width (cm)", min_value=0.0, format="%.2f")
    return [sepal_length, sepal_width, petal_length, petal_width]

# Prediction function
def predict_species(features):
    scaled_features = scaler.transform([features])  # Apply scaling
    prediction_probs = model.predict(scaled_features)
    predicted_class = np.argmax(prediction_probs, axis=1)[0]
    species_mapping = {0: "Setosa", 1: "Versicolor", 2: "Virginica"}
    return species_mapping[predicted_class]

st.title("Iris Species Prediction with MLP Model")

user_input = get_input()

if st.button("Predict"):
    prediction = predict_species(user_input)
    st.write(f"Predicted Species: {prediction}")

