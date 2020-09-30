##############
### zerter ###
##############
# zerter.py
#
# This script processes J-RES 2D spectra by setting to 0 (ZERT command) 
# left and right areas of peaks of interest.
#
####################
### Changes log  ###
####################
#
#    v0.2 (03/07/2020)
#        - add '-a' argument to use annotated peaks list
#        - in F1 dimension, parameters ABSF1 and SIGF1 are set to 1000, 
#          and parameters ABSF2 and SIGF2 are set to -1000 
#        - processing parameters and integral of the processed spectra are
#          saved in TITLE 
#    v0.1 (02/07/2020)
#        - initial release
#
####################
#
#    Author: Pierre Millard, pierre.millard@insa-toulouse.fr
#    Copyright 2020, INRAE
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
####################


##############################
# import modules & functions #
##############################
 
import os, sys

# set coordinates and zert the left side
def zert_left(s, width):
  PUTPAR("1 ABSF1", "1000")
  PUTPAR("1 ABSF2", "-1000")
  PUTPAR("1 SIGF1", "1000")
  PUTPAR("1 SIGF2", "-1000")
  absf1_f2 = float(GETPAR("OFFSET", 2)) #float(GETPAR("O1P", 2)) + float(GETPAR("SW", 2))/2
  PUTPAR("2 ABSF1", str(absf1_f2))
  #print(absf1_f2)
  #absf2_f2 = s + width/float(GETPAR("SFO1", 2)) - float(GETPAR("SW", 1))/2
  absf2_f2 = s + width/float(GETPAR("SFO1", 2)) - float(GETPAR("OFFSET", 1))
  PUTPAR("2 ABSF2", str(absf2_f2))
  #print(absf2_f2)
  sigf1_f2 = float(GETPAR("OFFSET", 2))
  #print(sigf1_f2)
  PUTPAR("2 SIGF1", str(sigf1_f2))
  sigf2_f2 = s + width/float(GETPAR("SFO1", 2)) + float(GETPAR("OFFSET", 1))
  #print(sigf2_f2)
  PUTPAR("2 SIGF2", str(sigf2_f2))
  ZERT2()

# set coordinates and zert the right side
def zert_right(s, width):
  PUTPAR("1 ABSF1", "1000")
  PUTPAR("1 ABSF2", "-1000")
  PUTPAR("1 SIGF1", "1000")
  PUTPAR("1 SIGF2", "-1000")
  absf2_f2 = float(GETPAR("OFFSET", 2)) - float(GETPAR("SW", 2))
  PUTPAR("2 ABSF2", str(absf2_f2))
  absf1_f2 = s - width/float(GETPAR("SFO1", 2)) - float(GETPAR("OFFSET", 1))
  PUTPAR("2 ABSF1", str(absf1_f2))
  sigf2_f2 = float(GETPAR("OFFSET", 2)) - float(GETPAR("SW", 2))
  PUTPAR("2 SIGF2", str(sigf2_f2))
  sigf1_f2 = s - width/float(GETPAR("SFO1", 2)) + float(GETPAR("OFFSET", 1))
  PUTPAR("2 SIGF1", str(sigf1_f2))
  ZERT2()

# copy current dataset to a new procno
def increment_procno(current_dataset):
  # get current procno
  ie = int(current_dataset[2])
  # identify next available procno
  while os.path.exists(os.path.join(current_dataset[3], current_dataset[0], current_dataset[1], "pdata", str(ie))):
    ie += 1
  if ie > 999:
    ERRMSG(message = "Too many procnos (> 999).", title="Error", details=None, modal=1)
    EXIT()
  current_dataset[2] = str(ie)
  WR(current_dataset)
  RE(current_dataset, show="y")
  return(current_dataset)

# get chemical shifts (F2) of annotated peaks
def get_peaks(current_dataset):
  peak_list = []
  file = os.path.join(current_dataset[3], current_dataset[0], current_dataset[1], "pdata", current_dataset[2], "peaklist.xml")
  if not os.path.exists(file):
    return([])
  f = open(file, "r")
  for l in f.readlines():
    if "<Peak2D F1=" in l:
      F2ppm = float(l.split(" F2=")[1].split(" ")[0].strip('"'))
      peak_list.append(F2ppm)
  f.close()
  return(peak_list)

# update title
def upd_title(current_dataset, ppm, width, integral):
  file = os.path.join(current_dataset[3], current_dataset[0], current_dataset[1], "pdata", current_dataset[2], "title")
  if os.path.exists(file):
    f = open(file, "r")
    txt = f.read()
    f.close()
  else:
    txt = ""
  txt += "\nchemical shift: " + str(ppm) + " ppm"
  txt += "\nwidth: " + str(width) + " Hz"
  txt += "\nintegral: " + str(integral) + " AU"
  f = open(file, "w")
  f.write(txt)
  f.close()

def get_integral():
  result = GETPROCDATA2D(-1000, 1000, -1000, 1000)
  integral = sum([sum(i) for i in result])
  return(integral)

##################
# run processing #
##################

# check if multiple display is active
if SELECTED_WINDOW().isMultipleDisplayActive():
  ERRMSG(message = "Please exit multiple display before running zerter.", title="Error", details=None, modal=1)
  EXIT()

# check spectrum dimension
if GETPROCDIM() != 2:
  ERRMSG(message = "The spectrum to process must have 2 dimensions.", title="Error", details=None, modal=1)
  EXIT()

# get current dataset
current_dataset = CURDATA()

# create peak list
if "-a" in sys.argv:
  # use annotation to get F2 chemical shifts if '-a' argument
  peak_list = get_peaks(current_dataset)
else:
  # otherwise, ask (F2) chemical shift(s) of signal(s) to process (semicolon-separated chemical shifts, in ppm)
  ask_n = INPUT_DIALOG("zerter", "", ["chemical shift(s) in ppm: ppm_1[;ppm_2;ppm_3]"], [""], [""], [""])
  if ask_n == None:
    EXIT()
  try:
    peak_list = [float(i) for i in ask_n[0].split(";")]
  except:
    ERRMSG(message = "Chemical shifts must be provided as floating point numbers separated by ';'.", title="Error", details=None, modal=1)
    EXIT()

# check the list of peaks is not empty
if len(peak_list) == 0:
  ERRMSG(message = "No signal to process.", title="Error", details=None, modal=1)
  EXIT()
 
# get width of the band in F2 dimension (along J=0 axis)
ask_w = INPUT_DIALOG("zerter", "", ["width in F2 dimension (hz)"], [""], [""], [""])
if ask_w == None:
  EXIT()
try:
  width = float(ask_w[0])/2
except:
  ERRMSG(message = "Width must be a positive number.", title="Error", details=None, modal=1)
  EXIT()
if width <= 0:
  ERRMSG(message = "Width must be a positive number.", title="Error", details=None, modal=1)
  EXIT()

# process all signals
for s in peak_list: 
  # increment procno
  current_dataset = increment_procno(current_dataset)
  # zert both sides of the spectra
  XFB()
  zert_left(s, width)
  zert_right(s, width)
  # integrate zerted spectra
  integral = get_integral()
  # save processing parameters and integral in TITLE
  upd_title(current_dataset, s, width, integral)


