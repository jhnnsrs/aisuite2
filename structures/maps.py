import numpy as np

from standardlibs.randcolours import rand_cmap

colorReadableMap = ["R","G","B","C1","C2","C3","C4","C5"]
availableMaps = [[0, 1, 2], [0, 2, 1], [1, 2, 0], [1, 0, 2], [2, 0, 1], [2, 1, 0]]
availableReadableMaps = [["R", "G", "B"], ["R", "B", "G"], ["G", "B", "R"], ["G", "R", "B"], ["B", "R", "G"],["B", "G", "R"]]
font = {'family': 'sans-serif', 'color':  'black','weight': 'bold','size': 9}
bbox = dict(boxstyle="circle,pad=0.2", fc="white", ec="white", lw=2, alpha=0.8)

colours = iter((rand_cmap(200)(np.linspace(0, 1, 200))))
smoothingfactor = 2