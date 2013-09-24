import sys
from pygr import seqdb, sequtil

inputFile = sys.argv[1]
genome = seqdb.SequenceFileDB(sys.argv[2])

for n, line in enumerate(open(inputFile), start=1):
    features = line.split()
    chrom = features[0]
    start = int(features[3]) - 1
    end = start + 150
    snpid = "%s:%d" % (chrom, start)
    seq = genome[chrom][start:end]
    sequtil.write_fasta(sys.stdout, seq, id=snpid)
    if (n % 1000) == 0:
        print >> sys.stderr, '...', n
