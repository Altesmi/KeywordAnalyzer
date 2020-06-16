import itertools

def analyze(data, options):
    if(options.get('keyword list') == None):
        # no keywords, looking for x num of same arguments
        return numberOfSame(data, options['number of same'])
    else:
        # looking for a specific keywords
        return keywordSearch(data, options['keyword list'], mode=options['mode'])

def numberOfSame(data, numSame):

    countOfKw = countKeywords(data)

    return findAllIntersectionsOfKeywords(countOfKw, numSame)

def countKeywords(data):
    """ Count all keywords in the input data file. """
    count = {}
    for key,value in data.items():
        for word in value:
            if(count.get(word) == None):
                count[word] = {'elements': [key], 'occurence': 1}
            else:
                count[word]['occurence'] += 1
                count[word]['elements'].append(key)
    return count

def keywordSearch(data, keywords, mode):
    """ Search for specific keyword(s) from the data. """
    countOfKw = countKeywords(data)
    for word in keywords:
        if word not in countOfKw.keys():
            countOfKw[word] = {'elements': [], 'occurence': 0}

    if mode == 'or':

        return({key: countOfKw[key] for key in keywords if key in countOfKw.keys()})

    if mode == 'and':

        return findIntersectionOfMatchingKeywords(countOfKw, keywords)

def findIntersectionOfMatchingKeywords(countOfKw, keywords):

    allElements = [countOfKw[k]['elements'] for k in keywords if k in countOfKw]
    result = set(allElements[0])
    for elements in allElements:
        result = result.intersection(set(elements))

    return result


def findAllIntersectionsOfKeywords(countOfKw, numSame):
    keywords = [k for k in countOfKw.keys()]
    keywordTuples = itertools.combinations(keywords, numSame)
    returnList = []

    for keywordTuple in keywordTuples:
        matches = findIntersectionOfMatchingKeywords(countOfKw, list(keywordTuple))
        if(len(matches)>1):  # not interested if the same two words are found in one element
            returnList.append({'words': list(keywordTuple), 'elements': list(matches)})
    return returnList