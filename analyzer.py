def analyze(data, options):
    if(options.get('keyword list') == None):
        # no keywords, looking for x num of same arguments
        return numberOfSame(data, options['number of same'])
    else:
        # looking for specific keywords
        return keywordSearch(data, options['keyword list'], mode=options['mode'])

def numberOfSame(data, numsame):

    countOfKw = countKeywords(data)

    return dict((keys,values) for keys,values in countOfKw.items() if values['occurence'] == numsame)

def countKeywords(data):
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
    countOfKw = countKeywords(data)
    if mode == 'or':

        return({key: countOfKw[key] for key in keywords if key in countOfKw.keys()})

    if mode == 'and':
        seen = set()
        repeated = set()
        for l in [countOfKw[k]['elements'] for k in keywords if k in countOfKw]:
            for i in set(l):
                if i in seen:
                    repeated.add(i)
                else:
                    seen.add(i)
        return(repeated)