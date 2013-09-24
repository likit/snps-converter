#Protocol

##Obtain sequences of SNPs from an old assembly
Suppose line6_snps.gff3 contains SNPs from the old assembly and chick.fa contains sequences of
all chromosomes of the old assembly.

    python gff-to-seq.py line6_snps.gff3 chick.fa > line6_snps.fa

##BLAT sequences against a new genome assembly
Suppose gal4selected.2bit is a 2bit file of the new assembly.

    blat -noHead -out=blast gal4selected.2bit line6_snps.fa line6_snps.fa.blast

##Convert BLAT results to BED
    python blast2bed.py line6_snps.fa.blast > line6_snps_gal4.bed
