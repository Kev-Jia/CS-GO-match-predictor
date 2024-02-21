from pathlib import Path
import json

files = [str(i) for i in Path(r"../demos/").glob("**/*") if i.is_file()]
jsonPaths = [i for i in files if "_PARSED.json" in i]

wholeDataset = []
trainingDataset = []
validationDataset = []
testDataset = []

# rough 70/15/15 split between training/validation/test dataset

for i in range(len(jsonPaths)):
    with open(jsonPaths[i], "r") as game:
        wholeDataset.append(json.load(game))

for i in range(len(jsonPaths[:141])):
    with open(jsonPaths[i], "r") as game:
        trainingDataset.append(json.load(game))

for i in range(len(jsonPaths[141:163])):
    with open(jsonPaths[i + 141], "r") as game:
        validationDataset.append(json.load(game))

for i in range(len(jsonPaths[163:])):
    with open(jsonPaths[i + 163], "r") as game:
        testDataset.append(json.load(game))

with open("../datasets/wholeDataset.json", "w") as datasetJson:
    json.dump(wholeDataset, datasetJson, indent = 4)

with open("../datasets/trainingDataset.json", "w") as datasetJson:
    json.dump(trainingDataset, datasetJson, indent = 4)

with open("../datasets/validationDataset.json", "w") as datasetJson:
    json.dump(validationDataset, datasetJson, indent = 4)

with open("../datasets/testDataset.json", "w") as datasetJson:
    json.dump(testDataset, datasetJson, indent = 4)
