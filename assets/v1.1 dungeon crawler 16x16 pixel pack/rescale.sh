#!/bin/bash

IFS=$'\n'

for i in $(find . -name "*.png")
do
	convert -resize 200% $i $i
done
