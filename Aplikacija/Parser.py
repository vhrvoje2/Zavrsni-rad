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
        for x in range(len(self.parsedData)):
            regexMatch = re.match(regex, self.parsedData[x])
            self.dataFrameList.append(list(regexMatch.groups()))

    def CreateDataFrame(self):
        self.DataFrame = pd.DataFrame(self.dataFrameList, columns=header)
        self.ModifiedDataFrame = self.DataFrame

    def ClearData(self):
        self.rawData = list()
        self.parsedData = list()
        self.dataFrameList = list()
        self.DataFrame = None
        self.ModifiedDataFrame = None

    def SearchDataFrame(self, term):
        df = self.DataFrame
        self.ModifiedDataFrame = df.loc[(df["IP klijenta"].str.contains(term)) | (df["ID korisnika"].str.contains(term)) | (df["Korisničko ime"].str.contains(term)) | (df["Datum i vrijeme"].str.contains(term)) | (df["Metoda i sadržaj"].str.contains(term)) | (df["Veličina u bajtovima"].str.contains(term)) | (df["Referrer"].str.contains(term)) | (df["Korisnički agent"].str.contains(term))]
        return self.ModifiedDataFrame

    def GetStatistics(self):
        statisticsDict = dict()
        statisticsDict["records"] = self.GetAmountOfRecords()
        statisticsDict["mbytes"] = self.GetTotalMBytes()
        statisticsDict["uniqueIPs"] = self.GetAmountOfUniqueIP()
        statisticsDict["topIP"] = self.GetTopIP()

        return statisticsDict

    def GetAmountOfRecords(self):
        df = self.DataFrame
        
        return str(len(df.index))

    def GetTotalMBytes(self):
        df = self.DataFrame["Veličina u bajtovima"]
        totalBytes = 0

        for value in df:
            if value.isdigit():
                totalBytes += int(value)

        return str(round(totalBytes/1000000, 2))

    def GetAmountOfUniqueIP(self):
        df = self.DataFrame
        uniqueIPs = df["IP klijenta"].nunique()

        return str(uniqueIPs)

    def GetTopIP(self):
        df = self.DataFrame
        topIP = df["IP klijenta"].value_counts().idxmax()
        
        return topIP
        
    def DisplayGraph(self, ind):
        plt.style.use("ggplot")

        if ind == 0:
            self.DisplayByHTTP()
        elif ind == 1:
            self.DisplayByMethod()
        else:
            self.DisplayAmountPerDay()

    def DisplayByHTTP(self):
        df = self.DataFrame

        fig, ax = plt.subplots()
        splitColumn = df["Metoda i sadržaj"].str.split(" ", expand = True)
        df["Metoda"] = splitColumn[0]

        fig.set_size_inches(8, 6)

        df["Metoda"].value_counts().plot(kind="barh")
        plt.show()

    def DisplayByMethod(self):
        df = self.DataFrame

        fig, ax = plt.subplots()

        fig.set_size_inches(8, 6)
        df["HTTP kod odgovora"].value_counts().plot(kind="bar")
        plt.show()

    def DisplayAmountPerDay(self):
        df = self.DataFrame
        
        fig, ax = plt.subplots()
        splitColumn = df["Datum i vrijeme"].str.split(":", expand = True)        
        df["Datum"] = splitColumn[0] 

        fig.set_size_inches(8, 6)

        df["Datum"].value_counts().plot(kind="pie")
        plt.show()

    def FilterColumns(self, checkboxList):
        dropList = list()

        for x in range(len(checkboxList)):
            if checkboxList[x] == 0:
                dropList.append(header[x])

        self.ModifiedDataFrame = self.DataFrame.drop(columns=dropList)
        
        return self.ModifiedDataFrame

    def SaveDataFrameAsCSV(self, dataFrame, path):
        dataFrame.to_csv(path, index = False, header=True)

#TEST
if __name__ == "__main__":
    mojParser = Parser()
    mojParser.SetFilename("access-log.txt")
    #mojParser.SetFilename("test-log.txt")
    df = mojParser.DataFrame
    #df = mojParser.DataFrame.drop(columns=["IP klijenta", "ID korisnika", "Korisničko ime", "Datum i vrijeme", "Metoda i sadržaj", "Veličina u bajtovima", "Referrer", "Korisnički agent"])
    #df = df.groupby(by="HTTP kod odgovora").size()
    #term = "140"
    #print(df.groupby(by="IP klijenta").agg({"IP klijenta": "nunique"}))
    mojParser.DisplayAmountPerDay()