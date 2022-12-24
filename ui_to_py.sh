#!/bin/bash
files=`ls shiki_organizer/gui/ui/*.ui`
for file in $files
do
   pyside6-uic "${file%%.*}".ui -g python -o "${file%%.*}".py
done