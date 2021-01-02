#!/bin/bash
for url in $(cat images.txt); do wget -P input/ -N $url & done
#for url in $(cat images.txt); do wget -P input/ -N $url ; echo $url ; done
