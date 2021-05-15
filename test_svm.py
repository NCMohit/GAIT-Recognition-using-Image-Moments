import pandas as pd
from sklearn import model_selection
from sklearn import svm
import pickle

# Read dataset into pandas dataframe
df = pd.read_csv('moments_data.csv',names=['Person','M00','M01','M02','M10','M11','M12','M20','M21','M22'])
features = ['M00','M01','M02','M10','M11','M12','M20','M21','M22']

# Extract features
X = df.loc[:, features].values

# Extract target i.e. iris species
Y = df.loc[:, ['Person']].values

# Now using scikit-learn model_selection module, split the iris data into train/test data sets

# keeping 40% reserved for testing purpose and 60% data will be used to train and form model.
X_train, X_test, Y_train, Y_test = model_selection.train_test_split (X, Y, test_size=0.05, random_state=0)




filename = 'trained_model.sav'
pickle.dump(clf_ob, open(filename, 'wb'))
