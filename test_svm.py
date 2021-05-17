import pandas as pd
from sklearn import model_selection
from sklearn import svm
import pickle

# Read dataset into pandas dataframe
df = pd.read_csv('moments_data_0to1.csv',names=['Person','M00','M01','M10','M11'])
features = ['M00','M01','M10','M11']

X = df.loc[:, features].values

Y = df.loc[:, ['Person']].values


X_train, X_test, Y_train, Y_test = model_selection.train_test_split (X, Y, test_size=0.05, random_state=0)


linear = svm.SVC(kernel='linear', C=1, decision_function_shape='ovo').fit(X_train, Y_train.ravel())

# filename = 'trained_model.sav'
# pickle.dump(linear, open(filename, 'wb'))

accuracy_lin = linear.score(X_test, Y_test.ravel())

print("Accuracy Linear Kernel:", accuracy_lin)