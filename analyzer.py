import itertools
import time
import statistics
import numpy as np
from math import comb


def analyze(data, options):
    if(options.get('exclude') is not None
       and options.get('excludemode') is not None):
        # need to exclude titles with certain keywords
        if(options['excludemode'] == 'and'):
            excludeFun = all
        elif(options['excludemode'] == 'or'):
            excludeFun = any
        newData = {}
        for k, v in data.items():
            if not excludeFun(elem in v for elem in options['exclude']):
                newData[k] = v
        data = newData
    if(options.get('number of same') is not None
       and options.get('keyword list') is None):
        # no keywords, looking for x num of same arguments
        plus = True if options.get('plus') else False
        showTime = True if options.get('show time') else False
        return numberOfSame(data, options['number of same'], plus=plus,
                            showTime=showTime)
    elif(options.get('keyword list') is not None
         and options.get('number of same') is None):
        # looking for a set of specific keywords
        return keywordSearch(data, options['keyword list'],
                             mode=options['mode'])
    elif (options.get('keyword list') is not None
          and options.get('number of same') is not None
          and options.get('mode') is not None):
        # looking for number of same and with specific keywords
        # filter out those headers that do not contain given keywords
        results = list(keywordSearch(data, options['keyword list'],
                                     mode=options['mode']))
        # create new data from results
        ind = [list(data.keys()).index(i) for i in results]
        words = list(data.values())
        filteredData = {}
        for i, _ in enumerate(ind):
            filteredData[results[i]] = words[ind[i]]

        plus = True if options.get('plus') else False
        showTime = True if options.get('show time') else False
        return numberOfSame(filteredData, options['number of same'], plus=plus,
                            showTime=showTime)
    elif(options.get('titles') is not None):
        # Looking for the number of same words in the specified headers/titles
        # filter the headers that are wanted
        filteredData = {key: data[key] for key in options['titles']}

        # run keywordSearch
        return findSame(filteredData)


def findSame(data):
    data = list(data.values())
    result = set(data[0])
    for elements in data:
        result = result.intersection(set(elements))
    return result


def numberOfSame(data, numSame, plus=False, showTime=False):
    countOfKw = countKeywords(data)
    results = findAllIntersectionsOfKeywords(countOfKw, numSame, showTime)
    if plus:
        # find all unique set of headers
        keywords = [result['words'] for result in results]
        headers = [result['elements'] for result in results]
        headers = list(map(sorted, headers))
        uniqueHeaders = []
        check = set()
        for headerlist in headers:
            hsh = tuple(sorted(headerlist))
            if hsh not in check:
                uniqueHeaders.append(headerlist)
                check.add(hsh)

        # find multiple keywords from elements which were the same
        # take only the unique keywords

        returnResult = [{'elements': e} for e in uniqueHeaders]
        for i, headerlist in enumerate(uniqueHeaders):
            ind = [j for j, x in enumerate(headers) if x == headerlist]
            if len(ind) == 1:
                returnResult[i]['words'] = keywords[ind[0]]
            else:
                allKeywords = [keywords[j] for j in ind]
                returnResult[i]['words'] = list(
                    set([item for kwlist in allKeywords for item in kwlist]))
        return returnResult
    else:
        return results


def countKeywords(data):
    """ Count all keywords in the input data file. """
    count = {}
    for key, value in data.items():
        for word in value:
            if(count.get(word) is None):
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

        return({key: countOfKw[key] for key in keywords
                if key in countOfKw.keys()})

    if mode == 'and':

        return findIntersectionOfMatchingKeywords(countOfKw, keywords)


def findIntersectionOfMatchingKeywords(countOfKw, keywords):

    allElements = [countOfKw[k]['elements']
                   for k in keywords if k in countOfKw]
    result = set(allElements[0])
    for elements in allElements:
        result = result.intersection(set(elements))

    return result


def findAllIntersectionsOfKeywords(countOfKw, numSame, showTime=False):
    keywords = [k for k in countOfKw.keys()]
    keywordTuples = itertools.combinations(keywords, numSame)
    returnList = []
    t = []
    t.append(time.time())
    # count number of combinations for show time options
    totalIterations = comb(len(keywords), numSame)
    counter = 0
    percentagePoints = [int(totalIterations*i) for i in np.linspace(0, 1, 21)]
    # edit the first one so that enough calculation takes place
    percentagePoints[0] = 300
    for keywordTuple in keywordTuples:
        if counter < 300:
            t.append(time.time())
        if showTime and counter in percentagePoints:
            meanExTime = statistics.mean(np.diff(t))
            eta = (1-counter/totalIterations)*totalIterations*meanExTime
            print('{}%: Estimated calculation time is {} s '
                  '(which is {} h or {} days)'.format(
                      int(counter/totalIterations*100),
                      int(eta),
                      int(eta/3600),
                      int(eta/3600/24)
                  ))
        matches = findIntersectionOfMatchingKeywords(
            countOfKw, list(keywordTuple))
        if(len(matches) > 1):
            # not interested if the same two words are found in one element
            returnList.append({'words': list(keywordTuple),
                               'elements': list(matches)})
        counter = counter + 1
    return returnList
