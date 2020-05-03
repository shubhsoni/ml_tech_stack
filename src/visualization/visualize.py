import matplotlib.pyplot as plt
from matplotlib import rcParams


class Visualize:
    '''All kinds of plot'''

    def __init__(self, data, target):
        '''
        Args:
            data: training data
            target: target name
        '''
        self.df = data
        self.target = target
    import pandas as pd
    pd.options.display.max_columns = None
    pd.options.display.max_rows = None
    
    def scatter(self, x, y, **kwargs):
        plt.subplots()
        plt.scatter(self.df[x], self.df[y], **kwargs)
        plt.show()
