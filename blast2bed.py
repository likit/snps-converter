'''Converts BLAST output to BED format.
The script is used to convert SNPs from gal3 genome coordinates to
gal4 genome coordinates.

'''


import sys
from blastparser import read


def main():
    blast_file = sys.argv[1]  # BLAT output with BLAST format

    for query in read(blast_file):
        for hit in query:
            try:
                qpos = hit.find_matched_subject(1)
            except KeyError:
                continue
            else:
                print '%s\t%d\t%d\t%s\t1000\t.\t%s' % (
                                            hit.subject,
                                            qpos-1,
                                            qpos,
                                            hit.query,
                                            hit.query_seq[0],
                                        )
                break


if __name__=='__main__':
    main()
