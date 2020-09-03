import re
import pandas as pd
import matplotlib.pyplot as plt

regex = r"([(\d\.)]+) (.*) (.*) \[(.*?)\] \"(.*?)\" (\d+) (\d+|.*) \"(.*)\" \"(.*)\""
header = ["IP klijenta", "ID korisnika", "Korisničko ime", "Datum i vrijeme", "Metoda i sadržaj", "HTTP kod odgovora", "Veličina u bajtovima", "Referrer", "Korisnički agent"]

class Parser():

    def __init__(self):
        self.rawData = list()
        self.parsedData = list()
        self.dataFrameList = list()

    def SetFilename(self, filename):
        self.filename = filename
        self.ReadFile()

    def ReadFile(self):
        self.ReadData()
        self.ParseData()
        self.CreateDataFrameList()   
        self.CreateDataFrame()     

    def ReadData(self):
        with open(self.filename, "r") as file:
            self.rawData = file.readlines()

    def ParseData(self):      
        for x in range(len(self.rawData)):
            line = self.rawData[x].replace("\n", "")
            self.parsedData.append(line)

    def CreateDataFrameList(self):
        for x in range(len(self.parsedData)-1):
            regexMatch = re.match(regex, self.parsedData[x])
            self.dataFrameList.append(list(regexMatch.groups()))

    def CreateDataFrame(self):
        self.DataFrame = pd.DataFrame(self.dataFrameList, columns=header)

#TEST
if __name__ == "__main__":
    mojParser = Parser()
    mojParser.SetFilename("access-log.txt")
    df = mojParser.DataFrame.drop(columns=["IP klijenta", "ID korisnika", "Korisničko ime", "Datum i vrijeme", "Metoda i sadržaj", "Veličina u bajtovima", "Referrer", "Korisnički agent"])
    df = df.groupby(by="HTTP kod odgovora").size()
    print(df)