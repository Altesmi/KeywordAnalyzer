import sys
import getopt
from readInput import readInput
from analyzer import analyze

def helpMessages():
    print('Usage: python keywords.py -i <inputfile> -w "<keywords to search>" -m <and/or search> OR -c <number of same keywords to search>')
    print('Käyttö: python keywords.py -t <avainsana tiedoston nimi> -s "<haettavat avainsanat>" -m <ja/tai haku> TAI -y <samojen avainsanojen lukumäärä>')

def quitProgram():
    helpMessages()
    sys.exit()

def main(argv):
    try:
        opts, args = getopt.getopt(argv, 'hi:w:c:t:s:y:m:',['inputfile=','tiedosto=','help','words=','common=','sanat=','yht=','mode='])
    except getopt.GetoptError:
        helpMessages()

    fname = ''
    keywords = []
    numSame = 0
    mode = ''
    for opt, arg in opts:
        if opt in ('-h','--help'):
            quitProgram()
        if opt in ('-i','-t','--inputfile','--tiedosto'):
            fname = arg
        if opt in ('-w','-s','--words','--sanat'):
            keywords = arg.replace(' ','').split(',')
        if opt in ('-m','-mode'):
            mode = arg
            if mode == 'ja':
                mode = 'and'

            if mode == 'tai':
                mode = 'or'
            if mode not in ('and','or'):
                quitProgram()

    print(mode)
    if len(fname) == 0:
        quitProgram()

    
    input = readInput(fname)
    options = {'number of same': 3}
    # options = {'keyword list': ['taas', 'entiedä'],'mode': 'and'}

    results = analyze(input,options)
    print(results)

if __name__ == '__main__':

    main(sys.argv[1:])

