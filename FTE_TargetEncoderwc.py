import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, RegressorMixin, TransformerMixin

# Declare Global variables that will be used at multiple places within the code
#CATEGORICALS_fewdim = ['SEGMENT'] 
# CATEGORICALS_manydim = ['CUST_ID', 'CLIENT', 'GLBU']
# TIME_VARIABLES = ['invoice_month', 'due_month']
# CATEGORICALS = CATEGORICALS_fewdim + CATEGORICALS_manydim + TIME_VARIABLES
TARGET = 'After 20% Overlay'
CATEGORICALS = ['Region','Country']

class FTE_TargetEncoderwc(BaseEstimator, TransformerMixin):
    
    '''
    Build a class to encode targets and inherit these two params to fit the class as a sklearn estimator
    '''
    
    def __init__(self, noise_level=0.1, smoothing=0.2, randomseed=42):        
        '''
        Constructor for the class
        
        Parameters
        ----------
        
        cols: list of str
            Columns to encode
        noise_level: float
            Standard deviation of the Guassian Noise to add to the encoded values
        smoothing: float
            Regularization to control the trandeoff between group mean and prior probability   
        randomseed: int
            Helps persist the encoding 
        '''
        self.cols = CATEGORICALS
        self.noise_level = noise_level
        self.smoothing = smoothing
        self.target_means = None
        self.randomseed = randomseed
        
    def fit(self, X, y):
        '''
        Compute the mean target value for each unique value in each column
        
        Parameters
        ----------
        X: pandas.DataFrame 
            Training data
        y: pd.Series 
            Target values
        
        Returns
        -------
        
        self: TargetEncoder with the fitted transfomer 
        '''
        
        self.target_means = {}
        self.randomseed = np.random.seed(42)
        
        for col in self.cols:
            data = pd.concat([X[col], y], axis=1)
            # Compute the mean, stddev and count for each unique value in the column
            group_mean = data.groupby(col).agg(np.mean)
            group_stdev = data.groupby(col).agg(np.std)
            group_count = data.groupby(col).agg("count")
            
            # Compute the mean and smooth it using the stdev and nomalized count 
            mean_smoother = ((group_count * group_mean) + self.smoothing * y.mean()) / (group_count+self.smoothing)
            
            # Then the magic happens of adding the Guassian noise to the categoricals 
            mean_smoother[TARGET] += self.noise_level + np.random.randn(len(mean_smoother))             
            # Convert the smoothed mean target values into a dict for easy lookup when encoding  
            self.target_means[col] = mean_smoother.to_dict()[TARGET]
        
        self.target_means['target_mean'] = np.mean(y)
        
        return self
    
    def transform(self, X):
        '''
        Encode the columns using the mean target value for each unique value
        
        Parameters
        ----------
        X: pandas.DataFrame 
            Data to encode 
        
        Returns
        -------
        
        X_encoded: pandas.DataFrame
            Encoded data
        '''
        
        X_encoded = X.copy()
        
        for col in self.cols:
            
            # Replace each value in the column with its corresponding target mean            
            X_encoded[col] = X_encoded[col].map(self.target_means[col])
            # Take care of the nulls as well
            X_encoded[col] = X_encoded[col].fillna(self.target_means['target_mean'])
            
        return X_encoded    
        