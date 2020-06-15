from readInput import readInput
from analyzer import analyze
if __name__ == '__main__':
    fname = 'sample.dat'

    input = readInput(fname)
    # options = {'number of same': 2}
    options = {'keyword list': ['taas', 'entiedä']}

    results = analyze(input,options)
    print(results)

