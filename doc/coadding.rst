.. highlight:: rest

*******************
Coadding of Spectra
*******************

This document will describe how to combine the spectra
from multiple exposures of the same object.

PYPIT currently only offers the coadding of spectra in
1D and must be done outside of the data reduction pipeline,
i.e. PYPIT will not automatically coadd your spectra as
part of the data reduction process.

1D Coadding
===========

This section describes the algorithms for coadding extracted,
"1D" spectra.


Input File
++++++++++

The information PYPIT's coadder uses is contained
within a .yaml file. At the most basic level, the file must
include the names of the files to be coadded, and a series
of dicts, labeled by 'a', 'b', 'c', etc., each of
which has a  PYPIT
object identifier string (used to ID the object)
and the name of an output file.  Here is an example
case::

    'filenames': ['spec1d_1.fits', 'spec1d_2.fits', 'spec1d_3.fits']
    'a':
        'object': 'O503-S4701-D01-I0035'
        'outfile': 'tmp.hdf5'

There is only one object to be coadded in each data frame.
The 'object' tag is a object identifier string containing the
object's relative location in the slit (here, 503 with 1000 the
right edge), the slit ID which is relative on the detector (4701),
the detector number (01), and the science index (0035), in
one of the files.

The list of object identifiers in a given spec1d file can be
output with the pypit_show_1dspec script, e.g.::

    pypit_show_1dspec filename.fits --list

The coadding algorithm will attempt to match this object identifier
to those in each data file, within some tolerance on object and slit
position. 'outfile' is the filename of the coadded spectrum produced.

Additional Coadding Parameters
++++++++++++++++++++++++++++++
You can adjust the default methods by which PYPIT coadds
spectra by adding a dict named 'global'::

    'filenames': ['spec1d_1.fits', 'spec1d_2.fits', 'spec1d_3.fits']
    'global':
        'wave_grid_method': 'velocity'
    'a':
        'object': 'O503-S4701-D01-I0035'
        'outfile': 'tmp.hdf5'

The adjustable parameters and options are:

Wavelength Rebinning
--------------------
==================   =======================  ==================================================
Parameter            Option                   Description
==================   =======================  ==================================================
wave_grid_method     default: concatenate     create a new wavelength grid onto which multiple
                                              exposures are rebinned after first concatenating
                                              all wavelength grids
--                   velocity                 create a new wavelength grid of constant km/s.
                                              Default is to use the median velocity width of the
                                              input spectrum pixels but a value 'v_pix' can be
                                              provided
--                   pixel                    create a new wavelength grid of constant Angstrom
                                              specified by the input parameter 'A_pix'
==================   =======================  ==================================================

Flux Scaling
------------
==================   =======================  ==================================================
Parameter            Option                   Description
==================   =======================  ==================================================
scale_method         default: auto            scale the flux arrays based on the root mean
                                              square value (RMS) of the S/N^2 value for all
                                              spectra; if this RMS value is less than the
                                              minimum median scale value, no scaling is applied.
                                              If the RMS value is greater than the minimum but
                                              smaller than the maximum median scale value, the
                                              applied method is the median, as described below
--                   hand                     scale the flux arrays using values specified by
                                              the user in the input parameter 'hand_scale'. Must
                                              have one value per spectrum
--                   median                   scale the flux arrays by the median flux value
                                              of each spectra
==================   =======================  ==================================================

Running the Coadd Code
++++++++++++++++++++++

Once you have this .yaml file set up, you can coadd your
1d spectra by running the command::

    pypit_coadd_1dspec name_of_yaml_file.yaml

The coadder will also produce a quality assurance (QA) file
named 'root_of_outfile.pdf'. In the left panel, the QA shows the chi-
squared residuals of the coadded spectrum, and in the right
panel, the coadded spectrum (in black) is plotted over the
original spectra.