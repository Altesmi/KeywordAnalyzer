def readInput(filename):
    returnDict = {} 
    with open(filename) as f:
        lines = f.readlines()
        for line in lines:
            keyvalueSplit = line.split(':')
            key = keyvalueSplit[0]
            keyvalueSplit[1] = keyvalueSplit[1][:-1] #remove '\n'
            returnDict[key] = keyvalueSplit[1].replace(' ','').split(',')

    return returnDict
            