#!/bin/sh

CHROM=("chr31" "chr30" "chr29")
NEWCHROM=("chrZ" "chrW" "chr32")

cp $1 $1.tmp
for ((n=0; n<3; n++))
do
    printf "replacing %s with %s\n" ${CHROM[$n]} ${NEWCHROM[$n]}
    sed s/${CHROM[$n]}/${NEWCHROM[$n]}/ $1.tmp > $1.tmp2
    printf "renaming %s to %s...\n" $1.tmp2 $1.tmp
    mv $1.tmp2 $1.tmp
done
