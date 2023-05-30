class LostSector:
    def __init__(self, day_of_week, date, name, reward, location, shields, champions, surge):
        self.day_of_week = day_of_week
        self.date = date
        self.name = name
        self.reward = reward
        self.location = location
        self.shields = shields
        self.champions = champions
        self.surge = surge
    def display(self):
        print("Lost Sector: " + self.name + ", " + self.day_of_week + " " + self.date + ", " + self.location\
        + ", " + self.reward + ", ", end='') 
        for element in self.shields:
            print(element + ", ", end='')
        for champion in self.champions:
            print(champion + ", ", end='')
        print(self.surge + '\n')

    def getShields(self):
        return self.shields
    def getChamps(self):
        return self.champions
    def getSurge(self):
        return self.surge
    def getDate(self):
        return self.date

def initializeSeasonalLostSectors():
    date, champions, shields, seasonalSectors = [], [], [], []
    day_of_week, name, reward, location, surge = "", "", "", "", ""
    file = open('defiance_LS.txt', 'r')
    while file:
        line = file.readline()
        if(line == '\n'):
            continue
        if(not line): 
            file.close()
            break
        splitLine = line.split()
        day_of_week = splitLine[0]
        date = splitLine[1]
        name = splitLine[2]
        location = splitLine[3]
        surge = splitLine[4]
        line = file.readline()
        splitLine = line.split()
        for element in splitLine:
            shields.append(element)
        champions.append(file.readline().strip())
        champions.append(file.readline().strip())
        reward = file.readline().strip()
        shields = [x.lower() for x in shields]
        champions = [x.lower() for x in champions]
        surge = surge.lower()
        seasonalSectors.append(LostSector(day_of_week, date, name, reward, location, shields, champions, surge))
        shields = []
        champions = []
    return seasonalSectors

def getSectorByDate(date):
    sectors = initializeSeasonalLostSectors()
    for sector in sectors:
        if sector.getDate() == date:
            return sector

