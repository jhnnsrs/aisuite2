[![DOI](https://zenodo.org/badge/223964939.svg)](https://zenodo.org/badge/latestdoi/223964939)


# AISuite

Johannes Roos, Maren Engelhardt

Institute of Neuroanatomy, Medical Faculty Mannheim, Heidelberg University


AISuite is a GUI program aiming to provide aid on identifying and processing structures from immunofluorescence files. It is powered by pyton-bioformats and is therefore able to handle data from most microscopes and uses OpenCV and Numpy to unleash Python's potential image processing capabilities. Visualization is provided by PyQT and matplotlib-bindings and data-storage is handled by HDF-Files.

## Installation

AISuite should run on every platform supporting Python 3.5.4 and Java 1.11. The authors have tested the program on Windows 7,8,10 with a standard Anaconda 4 installation and the modules provided in the environment.

Due to AISuites dependency on Bioformats and its Java libraries, we advise you to take care that you have a suitable C compiler installed. You can install the Windows SDK 7.1 and .Net Framework 4.0 to perform the compilation steps.

The Windows build is tested with Oracle JDK 1.11. You also need to install the Java Runtime Environment (JRE). Note that the bitness needs to match your Python version: if you use a 32-bit Python, then you need a 32-bit JDK; if you use a 64-bit Python, then you need a 64-bit JDK.

This repository comes provided with an Anaconda Environment Dump (environment.yml) that should help with installing the dependencies.

## API Interface

Reusable routines have been refactored into the logic modules and are pure functions that need to be provided with the according structures.

## Contributers


AISuite was designed to be easily extensible. If you have any suggestions or find bugs, please file accordingly. Contributions are always welcome.


## License
If you are using parts of this work for academic research please make sure to cite the authors (a link to a publication will be posted once available): Roos and Engelhardt, 2017.

AISelect is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

AISelect is distributed in the hope that it will be useful,but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details. You should have received a copy of the GNU General Public License along with AISelect.  If not, see http://www.gnu.org/licenses/
