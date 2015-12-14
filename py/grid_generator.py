import shapefile

class GridGenerator:

    minX = 0
    maxX = 0
    minY = 0
    maxY = 0
    outputFile = ""

    def __init__(self, minX, maxX, minY, maxY, outputFile):
        self.minX = minX
        self.maxX = maxX
        self.minY = minY
        self.maxY = maxY
        self.outputFile = outputFile

    def generate_grid_by_min_max_step(self, stepX, stepY):
        writer = shapefile.Writer()
        writer.shapeType = 0 # Polygon
        writer.autoBalance = 1
        writer.field('ID','C','40')
        writer.field('MINX','C','40')
        writer.field('MAXX','C','40')
        writer.field('MINY','C','40')
        writer.field('MAXY','C','40')
        print 'ss'
        currentX = self.minX
        currentY = self.minY

        currentID = 0

        while currentX < self.maxX:
            while currentY < self.maxY:
                nextX = currentX + stepX
                nextY = currentY + stepY
                if currentX + stepX > self.maxX:
                    nextX = self.maxX
                if currentY + stepY > self.maxY:
                    nextY = self.maxY

                currentID = currentID + 1
                writer.poly(parts=[[[currentX,currentY],[nextX,currentY],[nextX,nextY],[currentX,nextY]]])
                writer.record(str(currentID),str(currentX),str(nextX),str(currentY),str(nextY))

                currentY = currentY + stepY

            currentY = self.minY
            currentX = currentX + stepX

        writer.save(self.outputFile)


        pass

    def generate_grid_by_min_max_count (self, countX, countY):
        #print self.maxX, self.minX, countX
        stepX = (self.maxX - self.minX) / (countX * 1.0)
        stepY = (self.maxY - self.minY) / (countY * 1.0)
        #print stepX, stepY
        self.generate_grid_by_min_max_step(stepX,stepY)



gridGenerator = GridGenerator (0,10,0,10,'aaa2.shp')
#gridGenerator.generate_grid_by_min_max_step(3,3)
gridGenerator.generate_grid_by_min_max_count(103,12)