# -*- coding: utf-8 -*-
"""Climate data.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1VAFy838052uv9HtXhcFeRKb-ywthJUsB
"""

# Step 1: Import necessary libraries
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import re
import string

# Step 2: Load the dataset
df = pd.read_csv('/content/project5.csv')

# Step 3: Preprocess the text data
def preprocess_text(text):
    # Convert to lowercase
    text = text.lower()
    # Remove email addresses
    text = re.sub(r'\S*@\S*\s?', '', text)
    # Remove URLs
    text = re.sub(r'http\S+', '', text)
    # Remove punctuation
    text = text.translate(str.maketrans('', '', string.punctuation))
    # Remove digits
    text = re.sub(r'\d+', '', text)
    return text

df['text'] = df['text'].apply(preprocess_text)

# Step 4: Convert text data into numerical features using TF-IDF
tfidf = TfidfVectorizer(stop_words='english')
X = tfidf.fit_transform(df['text'])
y = df['spam']
print(y)

# Step 5: Split the data into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Check for missing values in y_train and handle them
print(y_train.isnull().sum())  # Check the number of missing values

# Option 1: Drop rows with missing values in y_train, while preserving alignment with X_train
# Get the indices of rows with missing values in y_train
missing_indices = y_train[y_train.isnull()].index

# Drop those rows from both y_train and X_train
y_train = y_train.dropna()
X_train = X_train[~np.isin(np.arange(X_train.shape[0]), missing_indices)]  # Use NumPy's isin to efficiently select rows

# Step 6: Train a machine learning model
model = MultinomialNB()
model.fit(X_train, y_train)

# Step 7: Evaluate the model
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f'Accuracy: {accuracy:.4f}')

print('Classification Report:')
print(classification_report(y_test, y_pred))

print('Confusion Matrix:')
print(confusion_matrix(y_test, y_pred))