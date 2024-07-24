# -*- coding: utf-8 -*-
"""assignment4 redo

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1n2HEHhY45R7062c7gGrx8v6ThdimjuXO

## **Problem 1:** Using cancer dataset to build an SVM classifier to classify type of cancer (Malignant vs. benign). Using PCA feature extraction for training.
"""

# Importing the dataset

import pandas as pd
from google.colab import drive
drive.mount('/content/drive')

file_path = '/content/drive/My Drive/ECGR 4105/Assignment 3/cancer.csv'
cancer_dataset = pd.DataFrame(pd.read_csv(file_path))
cancer_dataset.head()

'''

Data Preprocessing

'''

# Cleaning data
# Drop the 'Unnamed: 32' column
cancer_dataset.drop(['id', 'Unnamed: 32'], axis=1, inplace=True)

# Mapping M and B values of the diagnosis to 1 and 0
cancer_dataset['diagnosis'] = cancer_dataset['diagnosis'].map({'M': 1, 'B': 0})

X = cancer_dataset.drop('diagnosis', axis=1)
y = cancer_dataset['diagnosis']

# Performing scaling/normalization on features (x values) to scale the data between 0 and 1 to achieve better accuracy

from sklearn.preprocessing import StandardScaler
X_scaler = StandardScaler()
X_standard = X_scaler.fit_transform(X)

'''

Creating a function to perform SVM Classification

'''
from sklearn.model_selection import train_test_split
from sklearn.decomposition import PCA
from sklearn import metrics
from sklearn.svm import SVC

def SVM_classifier (X, y, kernel, N_iterations):

  accuracy_list = []
  precision_list = []
  recall_list = []

  accuracy = 0
  precision = 0
  recall = 0
  best_K = 0
  best_acc = 0

  for k in N_iterations:
    pca = PCA(n_components=k)
    X_pca = pca.fit_transform(X_standard)

    # Performing 80% and 20% split between training and evaluation (test)
    X_training, X_test, y_training, y_test = train_test_split(X_pca, y, test_size = 0.2, random_state = 0)
    classifier = SVC(kernel = kernel, C=3)
    classifier.fit(X_training, y_training)
    y_prediction = classifier.predict(X_test)

    accuracy = metrics.accuracy_score(y_test, y_prediction)
    precision = metrics.precision_score(y_test, y_prediction)
    recall = metrics.recall_score(y_test, y_prediction)
    f1_score = metrics.f1_score(y_test, y_prediction)
    accuracy_list.append(accuracy)
    precision_list.append(precision)
    recall_list.append(recall)

  # Test to see if the accuracy is the best
  # If it is, set it to the best accuracy and K value
    if accuracy > best_acc:
      best_acc = accuracy
      best_K = k

  return accuracy_list, precision_list, recall_list, best_acc, best_K

'''

Creating a function to plot SVM Classification

'''

import matplotlib.pyplot as plt

# This plot function recalls the SVM_classifier function created previously
def SVM_plot (X, y, kernel, N_iterations):
  accuracy, precision, recall, highest_acc, k_val = SVM_classifier(X, y, kernel, N_iterations)
  plt.figure(figsize=(15, 5))

  plt.subplot(1, 3, 1)
  plt.plot(N_iterations, accuracy)
  plt.title(f'{kernel} Kernal Accuracy over Number of Ks')
  plt.xlabel('Number of Principal Components (K)')
  plt.ylabel('Accuracy')

  plt.subplot(1, 3, 2)
  plt.plot(N_iterations, precision)
  plt.title(f'{kernel} Kernal Precision over Number of Ks')
  plt.xlabel('Principal Component (K)')
  plt.ylabel('Precision')

  plt.subplot(1, 3, 3)
  plt.plot(N_iterations, recall)
  plt.title(f'{kernel} Kernal Recall over Number of Ks')
  plt.xlabel('Principal Component (K)')
  plt.ylabel('Recall')

  plt.tight_layout()
  plt.show()

  print(f'Optimum Number of K Principal Components: {k_val}')
  print(f'{kernel} Highest Accuracy Value: {highest_acc}')

'''

Executing SVM with different kernel tricks

'''

SVM_plot(X, y, 'linear', range(1, X.shape[1] + 1))
SVM_plot(X, y, 'rbf', range(1, X.shape[1] + 1))
SVM_plot(X, y, 'poly', range(1, X.shape[1] + 1))


'''

Function to plot SVR Classification

'''

def SVM_plot_accuracies (X, y, kernel, N_iterations):
  accuracy, precision, recall, highest_acc, k_val = SVM_classifier(X, y, kernel, N_iterations)
  plt.figure(figsize=(14, 6))

  plt.plot(N_iterations, accuracy)
  plt.title(f'{kernel} Kernal Accuracy over Number of Ks')
  plt.xlabel('Number of Principal Components (K)')
  plt.ylabel('Accuracy')

  plt.tight_layout()
  plt.show()

  print(f'Optimum Number of K Principal Components: {k_val}')
  print(f'{kernel} Highest Regression Accuracy Value: {highest_acc}')

'''

Executing SVM with different kernel tricks

'''

SVM_plot_accuracies(X, y, 'linear', range(1, X.shape[1] + 1))
SVM_plot_accuracies(X, y, 'rbf', range(1, X.shape[1] + 1))
SVM_plot_accuracies(X, y, 'poly', range(1, X.shape[1] + 1))

"""## **Problem 2:** Using housing dataset to build an SVR classifier. Using PCA feature extraction for training."""

# Importing the dataset

import pandas as pd
from google.colab import drive
drive.mount('/content/drive')

file_path = '/content/drive/My Drive/ECGR 4105/Assignment2/Housing.csv'
housing_dataset = pd.DataFrame(pd.read_csv(file_path))
housing_dataset.head()

'''

Data Preprocessing

'''

X_vars = ['area', 'bedrooms', 'bathrooms', 'stories', 'mainroad', 'guestroom', 'basement', 'hotwaterheating', 'airconditioning', 'parking', 'prefarea']
y_vars = 'price'

X = housing_dataset[X_vars]

# Changing 'yes' and 'no' to 1 and 0
X = pd.get_dummies(X, drop_first=True)
y = housing_dataset[y_vars]

from sklearn.preprocessing import StandardScaler
X_scaler = StandardScaler()
X_standard = X_scaler.fit_transform(X)

# Performing 80% and 20% split between training and evaluation (test)
X_training, X_test, y_training, y_test = train_test_split(X_standard, y, test_size = 0.2, random_state = 0)

'''

Scatter Plots

'''

###################################################
# Linear SVR Scatter Plot
###################################################

from sklearn.svm import SVR

classifier = SVR(kernel = 'linear')
classifier.fit(X_training, y_training)

y_pred = classifier.predict(X_test)

plt.figure(figsize=(14, 6))

plt.scatter(y_pred, y_test)
plt.xlabel('Data')
plt.ylabel('Targets')
plt.title('SVR Linear Kernel Predictions')
plt.show()

###################################################
# Kernel Scatter Plots
###################################################

classifier = SVR(kernel = 'linear')
classifier.fit(X_training, y_training)

y_prediction_linear = classifier.predict(X_test)

classifier = SVR(kernel = 'rbf')
classifier.fit(X_training, y_training)

y_prediction_rbf = classifier.predict(X_test)

classifier = SVR(kernel = 'poly')
classifier.fit(X_training, y_training)

y_prediction_poly = classifier.predict(X_test)

plt.figure(figsize=(14, 6))

plt.subplot(1, 3, 1)
plt.scatter(y_prediction_linear, y_test)
plt.xlabel('Data')
plt.ylabel('Targets')
plt.title('SVR Linear Kernel Predictions')

plt.subplot(1, 3, 2)
plt.scatter(y_prediction_rbf, y_test)
plt.xlabel('Data')
plt.ylabel('Targets')
plt.title('SVR RBF Kernel Predictions')

plt.subplot(1, 3, 3)
plt.scatter(y_prediction_poly, y_test)
plt.xlabel('Data')
plt.ylabel('Targets')
plt.title('SVR Poly Kernel Predictions')

plt.tight_layout()
plt.show()


'''

Function for SVR Classification

'''

def SVR_classifier (X, y, kernel, N_iterations):
  mse_list = [] # Mean squared error used accuracy metric

  mse = 0
  best_K = 0
  best_mse = float('inf')  # Initializing mse with a large value

  for k in N_iterations:
    pca = PCA(n_components=k)
    X_pca = pca.fit_transform(X_standard)

    # Performing 80% and 20% split between training and evaluation (test)
    X_training, X_test, y_training, y_test = train_test_split(X_pca, y, test_size = 0.2, random_state = 0)

    classifier = SVR(kernel = kernel, C=3)
    classifier.fit(X_training, y_training)

    y_prediction = classifier.predict(X_test)

    mse = metrics.mean_squared_error(y_test, y_prediction)

    mse_list.append(mse)

  # Test to see if the accuracy is the best
  # If it is, set it to the best accuracy and K value
    if mse < best_mse:
      best_mse = mse
      best_K = k

  return mse_list, best_mse, best_K

'''

Function to plot SVR Classification

'''

def SVR_plot (X, y, kernel, N_iterations):
  mse_values, lowest_mse, k_val = SVR_classifier(X, y, kernel, N_iterations)
  plt.figure(figsize=(14, 6))

  plt.plot(N_iterations, mse_values)
  plt.title(f'{kernel} Kernal Accuracy over Number of Ks')
  plt.xlabel('Number of Principal Components (K)')
  plt.ylabel('Accuracy')

  plt.tight_layout()
  plt.show()

  print(f'Optimum Number of K Principal Components: {k_val}')
  print(f'{kernel} Highest Regression Accuracy Value: {lowest_mse}')

'''

Executing SVM with different kernel tricks

'''

SVR_plot(X, y, 'linear', range(1, X.shape[1] + 1))
SVR_plot(X, y, 'rbf', range(1, X.shape[1] + 1))
SVR_plot(X, y, 'poly', range(1, X.shape[1] + 1))