import matplotlib.pyplot as plt


class Vizualize:
    '''All kinds of plot'''

    def __init__(self, data, target):
        self.df = data
        self.target = target


    def scatter(self, x, y, **kwargs):
        plt.subplots()
        plt.scatter(x, y, **kwargs)
        plt.show()

