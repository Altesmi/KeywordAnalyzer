import sys
import getopt
import itertools
from readInput import readInput
from analyzer import analyze


def helpMessages():
    print('')
    print('Usage: python keywords.py -i < input file > '
          '-l <language (en or fi) -w "< keywords to search >" '
          '-m <and/or search>'
          'AND/OR -c < number of same keywords to search >'
          'OR -h "< titles >"')
    print('')
    print('with -c option it is also possible to include'
          ' --time flag to print approximate time the calculations take.')
    print('')
    print('Käyttö: python keywords.py - t < avainsana tiedoston nimi > '
          '-k <kieli (englanti tai suomi)> '
          '-s "<haettavat avainsanat>" '
          '-m <ja/tai haku>'
          'JA/TAI -y < samojen avainsanojen lukumäärä >'
          ' TAI -o < otsakkeiden nimet >')
    print('')
    print('-y valinnan kanssa on myös mahdollista lisätä --aika valinta,'
          'jolloin ohjelma tulostaa arvion, kuinka kauan laskenta kestää.')


def quitProgram():
    helpMessages()
    sys.exit()


def main(argv):
    try:
        opts, args = getopt.getopt(argv, 'i:w:c:t:s:y:m:l:k:o:h:',
                                   ['inputfile=',
                                    'tiedosto=',
                                    'help',
                                    'words=',
                                    'common=',
                                    'sanat=',
                                    'yht=',
                                    'mode=',
                                    'outputlang=',
                                    'kieli=',
                                    'time',
                                    'aika',
                                    'otsakkeet=',
                                    'titles='])
    except getopt.GetoptError:
        helpMessages()

    fname = ''
    keywords = []
    numSame = 0
    mode = ''
    outputlang = 'en'
    titles = []
    showTime = False

    for opt, arg in opts:

        if opt in ('-i', '-t', '--inputfile', '--tiedosto'):
            fname = arg
        if opt in ('-w', '-s', '--words', '--sanat'):
            keywords = arg.replace(' ', '').split(',')
        if opt in ('-m', '-mode'):
            mode = arg
            if mode == 'ja':
                mode = 'and'

            if mode == 'tai':
                mode = 'or'
            if mode not in ('and', 'or'):
                quitProgram()
        if opt in ('-c', '-y', '--common', '--yht'):
            numSplit = ["".join(x)
                        for _, x in itertools.groupby(arg, key=str.isdigit)]
            numSame = int(numSplit[0])
        if opt in ('-l', '-k', '--outputlang', '--kieli'):
            if arg in ('fi', 'suomi'):
                outputlang = 'fi'
        if opt in ('-h', '-o', '--headers', '--otsakket'):
            titles = arg.replace(' ', '').split(',')
        if opt in ('--aika', '--time'):
            showTime = True

    # Check that enough input is given
    if len(fname) == 0:
        quitProgram()
    elif len(keywords) > 0 and len(mode) > 0 and numSame == 0:
        options = {'keyword list': keywords, 'mode': mode}
    elif (numSame > 0 and len(keywords) == 0 and len(mode) == 0
          and len(numSplit)) == 1:
        options = {'number of same': numSame, 'show time': showTime}
    elif (numSame > 0 and len(keywords) == 0 and len(mode) == 0
          and len(numSplit) > 1 and numSplit[1] == '+'):
        options = {'number of same': numSame, 'plus': True,
                   'show time': showTime}
    elif (numSame > 0 and len(keywords) > 0 and len(mode) > 0):
        options = {'number of same': numSame,
                   'keyword list': keywords,
                   'mode': mode,
                   'show time': showTime}
        if(len(numSplit) > 1 and numSplit[1] == '+'):
            options['plus'] = True
    elif(len(titles) > 0):
        options = {'titles': titles}
    else:
        quitProgram()

    input = readInput(fname)
    results = analyze(input, options)

    if len(keywords) > 0 and mode == 'or' and numSame == 0:
        if(outputlang == 'en'):
            for k, v in results.items():
                print('For keyword {} found following matches'.format(k))
                print(v['elements'])
                print('Alltogether {} occurences in input file'.format(
                    v['occurence']))
                print()
        if(outputlang == 'fi'):
            for k, v in results.items():
                print('Avainsana {} löytyy seuraavista otsikoista'.format(k))
                print(v['elements'])
                print('Avainsana löytyy yhteensä {} kertaa annetusta '
                      'tiedostosta'.format(
                          v['occurence']))
                print()

    elif len(keywords) > 0 and mode == 'and' and numSame == 0:
        if(outputlang == 'en'):
            print('The words {} are all found in titles'.format(keywords))
            print(list(results))
        if(outputlang == 'fi'):
            print('Sanat {} löytyvät kaikki otsikoista'.format(keywords))
            print(list(results))

    elif numSame > 0:
        if(outputlang == 'en'):
            for item in results:
                print('Found keywords {} from following titles'.format(
                    item['words']))
                print(item['elements'])
                print()
        if(outputlang == 'fi'):
            for item in results:
                print('Löytyi avainsanat {} seuraavista otsikoista'.format(
                    item['words']))
                print(item['elements'])
                print()

    elif len(titles) > 0:
        if(outputlang == 'en'):
            print('The keywords {} are the same in titles'.format(results))
            print(titles)
        if(outputlang == 'fi'):
            print('Avainsanat {} ovat samat otsikoissa'.format(results))
            print(titles)


if __name__ == '__main__':

    main(sys.argv[1:])
