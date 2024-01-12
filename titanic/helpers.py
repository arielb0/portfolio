'''
Here I will put the application logic.

model: There are a model to train on
 entire application. I need a to create a 
 Logistic regression model that classify user 
 on surviver or not.

user: There are several users that application
 try to predict if survive or not.

'''
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from scull_suite.settings import BASE_DIR

class TitanicSurvivorModel:
    
    def __init__(self):
        '''Initialize the object to classify if user will survive or not.'''
        
        # Load the dataset
        dataset = pd.read_excel(BASE_DIR / 'titanic/titanic3.xls')
        
        #Select the rows used to make prediction
        dataset = dataset[['pclass', 'sex', 'age', 'sibsp', 'parch', 'fare', 'embarked', 'survived']]

        # Clean dataset (remove empty values)
        dataset.dropna(inplace=True)
        
        # Transform string categorical columns to numerical columns on dataset
        dataset['sex'] = pd.Categorical(dataset['sex']).codes
        dataset['embarked'] = pd.Categorical(dataset['embarked']).codes

        # Split dataset into features and target variables
        features = dataset[['pclass', 'sex', 'age', 'sibsp', 'parch', 'fare', 'embarked']]
        target = dataset[['survived']]        
        
        # Split features and target dataset into train and test datasets.
        features_train, features_test, target_train, target_test = train_test_split(features, target, test_size = 0.25, random_state = 16)
        
        # Train the model        
        self.model = LogisticRegression(random_state = 16)
        self.model.fit(features_train, target_train.values.ravel())        

        # We don't test the accuracy of the model because I did it previously
        # on Jupyter Notebook.

    
    def predict(self, user_data: dict) -> bool:
        '''Predict if a user will survive or not'''

        # Create a row of user features
        
        user_features = pd.DataFrame(data = {
            'pclass': int(user_data['passenger_class']),
            'sex': int(user_data['sex']),
            'age': int(user_data['age']),
            'sibsp': int(user_data['number_of_slibings_or_spouses']),
            'parch': int(user_data['number_of_parents_or_children']),
            'fare': int(user_data['fare']),
            'embarked': int(user_data['embarked'])
        }, index=[0])

        # Make a prediction using the model
        is_survivor = self.model.predict(user_features)
        
        if is_survivor:
            return True
        
        return False
