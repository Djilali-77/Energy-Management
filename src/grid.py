class Grid:
    def __init__(self, price, max_import):
        self.price = price
        self.max_import = max_import

    def calcule_cost(self, grid_import):
        if grid_import <= self.max_import:
            cost = grid_import * self.price
            return cost