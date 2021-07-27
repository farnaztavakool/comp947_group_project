from sklearn.tree import DecisionTreeClassifier
import customer_satisfaction as cs
import pandas as pd
from sklearn.utils import resample

def preprocessData(df_train, df_test):

    dup = cs.dropDuplicatedRowAndColumn(df_train, df_test)
    df_train = dup[0]
    df_test = dup[1]

    y_train = df_train['TARGET'].copy()
    df_train_x = df_train.drop(columns="TARGET")

    quasi_res = cs.quasiConstantRemoval(df_train_x, 0.01, df_test)
    df_train_x = quasi_res[0]
    df_test = quasi_res[1]

    correlated  = cs.dropCorrelatedFeatures(df_train_x,df_test)
    df_train_x = correlated[0]
    df_test = correlated[1]

    # use ANOVA to select k best features, the number of features is a hyperparameter which we need to test to find a best one
    num_features_ANOVA = 100
    df_train_x, df_test = cs.featureSelectionANOVA(df_train_x, y_train, df_test, num_features_ANOVA)

    # use decisionTreeClassifier for the estimator of RFE to fun the feature selection
    estimator = DecisionTreeClassifier()
    num_features_RFE = 70
    df_train_x, df_test = cs.featureSelectionRFE(df_train_x, y_train, df_test, num_features_RFE, estimator)


    df_train_x = cs.normalise(df_train_x)
    df_test = cs.normalise(df_test)
    
    df_train_x.to_csv('X_train.csv', index= False)
    y_train.to_csv('Y_train.csv', index= False)
    df_test.to_csv('X_test.csv', index= False)

    return [df_train_x, y_train, df_test]


def oversampling_dataset(data):
    count_majority, count_minority = data['TARGET'].value_counts()
    
    data_majority=data[data.TARGET==0] 
    data_minority=data[data.TARGET==1]  

    data_minority_over = data_minority.sample(count_majority, replace=True)
    data_oversampled=pd.concat([data_minority_over,data_majority])

    print(data_oversampled['TARGET'].value_counts())
    return data_oversampled

def undersampling_dataset(data):
    count_majority, count_minority = data['TARGET'].value_counts()
    
    data_majority=data[data.TARGET==0] 
    data_minority=data[data.TARGET==1]  

    data_majority_under = data_majority.sample(count_minority)
    data_underampled=pd.concat([data_majority_under,data_minority])

    print(data_underampled['TARGET'].value_counts())
    return data_underampled

df_train = cs.loadData("train.csv")
df_test = cs.loadData("test.csv")

# dropping "ID" from both training and test data
ID_train = df_train["ID"].copy()
ID_test = df_test["ID"].copy()
df_train = df_train.drop(columns = "ID")
df_test = df_test.drop(columns = "ID")

preprocessData(df_train, df_test)

