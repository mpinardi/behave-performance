from behave.model import Tag
from copy import deepcopy
import pickle

def deep_copy_features(features):
    cfs = []
    def __deepcopy(self, memo):
        result = Tag(self,self.line) # Create a new instance of the object based on extracted class
        memo[id(self)] = result
        for k, v in self.__dict__.items():
            setattr(result, k, deepcopy(v, memo)) # Copy over attributes by copying directly or in case of complex objects like lists for exaample calling the `__deepcopy()__` method defined by them. Thus recursively copying the whole tree of objects.
        return result
    
    Tag.__deepcopy__ = __deepcopy              
    for feature in features:
        cfs.append(deepcopy(feature))
    return cfs

def pickle_copy_features(features):
    cfs = []
    # def __setstate(self, state):
    #     self.__dict__.update(state)
    # def __getstate(self):
    #     return self.__dict__.copy()
    def __taggetnewarg(self):
        return (str(self),self.line)
    Tag.__getnewargs__ = __taggetnewarg
    for feature in features:
        cfs.append(pickle.loads(pickle.dumps(feature, -1)))
    return cfs