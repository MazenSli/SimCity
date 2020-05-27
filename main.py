#
# main.py
#
#

from builtins import Exception
import optparse
import sys
from modules.Intersection import Intersection
from modules.Street import Street


class TestModule:
    """
    # base class for all traffic elements
    """

    # constructor
    def __init__(self):
        pass

    # string representation for class data
    def __str__(self):
        pass


#
# Main entry point
#
def main(argv=None):
    if argv is None:
        argv = sys.argv
        
    try:
        #
        # get command-line options
        #
        parser = optparse.OptionParser()
        parser.add_option("-i", "--input", action="store", dest="inputFileName", help="input filename", default=None)
        parser.add_option("-q", "--quiet", action="store_true", dest="quietMode", help="quiet mode", default=False)
        parser.add_option("-d", "--debug", action="store_true", dest="debugMode", help="debug mode", default=False)
        (options, args) = parser.parse_args(argv)
        
        #validate options
        if options.inputFileName is None:
            raise Exception("Must specify input file name using -i or --input option.")

        Inter1 = Intersection()
        Inter2 = Intersection()
        Inter3 = Intersection()
        Inter4 = Intersection()
        Street1 = Street()
        Street2 = Street()
        Street3 = Street()
        Street4 = Street()

        if not options.quietMode:                    
            print('Main Completed!')
    
    except Exception as info:
        if 'options' in vars() and options.debugMode:
            from traceback import print_exc
            print_exc()
        else:
            print(info)
    

if __name__ == '__main__':
    main()
