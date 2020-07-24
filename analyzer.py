import itertools
import time
import statistics


def analyze(data, options):

    if(options.get('number of same') is not None
       and options.get('keyword list') is None):
        # no keywords, looking for x num of same arguments
        plus = True if options.get('plus') else False
        return numberOfSame(data, options['number of same'], plus)
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
        return numberOfSame(filteredData, options['number of same'], plus)


def numberOfSame(data, numSame, plus):
    countOfKw = countKeywords(data)
    results = findAllIntersectionsOfKeywords(countOfKw, numSame)
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


def findAllIntersectionsOfKeywords(countOfKw, numSame):
    keywords = [k for k in countOfKw.keys()]
    keywordTuples = itertools.combinations(keywords, numSame)
    returnList = []
    for keywordTuple in keywordTuples:
        matches = findIntersectionOfMatchingKeywords(
            countOfKw, list(keywordTuple))
        if(len(matches) > 1):
            # not interested if the same two words are found in one element
            returnList.append({'words': list(keywordTuple),
                               'elements': list(matches)})

    return returnList
