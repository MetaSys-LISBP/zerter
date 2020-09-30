# Zerter

## What is Zerter?
**Zerter is a scientific software dedicated to the processing of (bio)chemical experiments by NMR**.
In J-RES spectra, **zerter** zeroes the trapezia left and right of a diagonal corresponding to a particular proton, along a 45° diagonal.

It is one of the routine tools that we use at the [MetaSys team](http://www.lisbp.fr/en/research/integrated-metabolism-and-dynamics-of-metabolic-systems.html) and [MetaToul platform](https://www6.toulouse.inra.fr/metatoul_eng/) 
for quantitative analysis of 31P phosphometabolites.

The code is open-source, and available under a GPLv3 license.

## Quick-start
Zerter requires TopSpin 4.0 or higher (tested on 4.0.7) and run on all plate-forms.

To **install Zerter**:

Unpack the content of Zerter.zip somewhere on your disk, and copy the file 'zerter.py' in the python program folder of your TopSpin user directory (by default: <TopSpin installation directory>/exp/stan/nmr/py/usr)

To **use Zerter**:

Zerter requires as input a 2D J-res spectra which must be Fourier-transformed.

- Open the pseudo 2D spectra to process.

- Run the command 'zerter' in TopSpin. To process all annotated signals, use the argumenta '-a' (command: 'zerter -a').

- If processing is not based on annotation, enter the chemical shift(s) (at J=0 Hz) of signal(s) to process (in ppm, separated by a semi colon ';').

- Enter the width of the window to extract.

- Processing results will be saved as new procnos, please refers to the spectra titles for the corresponding processing information.


## Bug and feature requests
If you have an idea on how we could improve Zerter please submit a new *issue*
to [our GitHub issue tracker](https://github.com/MetaSys-LISBP/zerter/issues).


## Developers guide
### Contributions
Contributions are very welcome! :heart:

Please work on your own fork.

## Reference
Cox, N., et al. Improved NMR detection of phospho-metabolites in a complex mixture (submitted)

## Authors
Pierre Millard, Neil Cox, Guy Lippens

## Contact
:email: Pierre Millard, millard@insa-toulouse.fr
