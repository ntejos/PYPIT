#!/usr/bin/env python

"""
Wrapper to the linetools XSpecGUI
"""


def parser(options=None):

    import argparse

    parser = argparse.ArgumentParser(description='Parse')
    parser.add_argument("file", type=str, help="Spectral file")
    parser.add_argument("--list", default=False, help="List the extensions only?", action="store_true")
    parser.add_argument("--exten", type=int, default=1, help="FITS extension")
    parser.add_argument("--extract", type=str, default='box', help="Extraction method. Default is boxcar. ['box', 'opt']")

    if options is None:
        args = parser.parse_args()
    else:
        args = parser.parse_args(options)
    return args


def main(args, unit_test=False):
    """ Runs the XSpecGui on an input file
    """
    import sys
    from pypit import arload
    import pdb

    # List only?
    if args.list:
        print("Showing object names for input file...")
        spec = arload.load_1dspec(args.file, extract=args.extract)
        for key in spec.header.keys():
            if 'EXT0' in key:
                print("{} = {}".format(key, spec.header[key]))
        sys.exit()

    from linetools.guis.xspecgui import XSpecGui
    from pypit import arload

    # Load spectrum
    spec = arload.load_1dspec(args.file, exten=args.exten, extract=args.extract)

    if unit_test is False:
        from PyQt4 import QtGui
        app = QtGui.QApplication(sys.argv)

    gui = XSpecGui(spec, unit_test=unit_test)
    if unit_test is False:
        gui.show()
        app.exec_()
