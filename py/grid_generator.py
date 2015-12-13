import shapefile

class GridGenerator:

    minX = 0
    maxX = 0
    minY = 0
    maxY = 0
    stepX = 0
    stepY = 0
    countX = 0
    countY = 0

    def __init__(self, minX, maxX, minY, maxY):
        self.minX = minX
        self.maxX = maxX
        self.minY = minY
        self.maxY = maxY

    def generate_grid_by_min_max_step(self, stepX, stepY):
        pass

    def generate_grid_by_min_max_count (self, countX, countY):
        pass



