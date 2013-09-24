import sys

class BlastHit(object):
    def __init__(self, query, subject):
        self.query = query
        self.subject = subject
        self.query_seq = []
        self.subject_seq = []
        self.query_match = {}
        self.subject_match = {}
        self.alignments = []
        self.query_start = None
        self.query_stop = None
        self.subject_start = None
        self.subject_stop = None

    def _add_match(self):
        m = self.query_start
        j = self.subject_start

        for i in self.query_seq:
            self.query_match[m] = j
            self.subject_match[j] = m
            j += 1
            if self.query_start < self.query_stop:
                m += 1
            else:
                m -= 1

    def find_matched_subject(self, query_pos):
        '''returns a subject postition that match a given query position'''

        if not self.subject_match:
            self._add_match()

        return self.query_match[query_pos]

    def find_matched_query(self, subject_pos):
        '''returns a query postition that match a given subject position'''

        if not self.query_match:
            self._add_match()

        return self.subject_match[subject_pos]

    def add_query_seq(self, line):
        assert line.startswith('Query:')
        alignment = line.split()
        self.query_seq += alignment[2].upper()

        if not self.query_start:
            self.query_start = int(alignment[1])
        self.query_stop = int(alignment[-1])

    def add_subject_seq(self, line):
        assert line.startswith('Sbjct:')
        alignment = line.split()
        self.subject_seq += alignment[2].upper()
        if not self.subject_start:
            self.subject_start = int(alignment[1])
        self.subject_stop = int(alignment[-1])

    def update_alignments(self):
            for i in range(len(self.query_seq)):
                aln = '|' if self.query_seq[i] == self.subject_seq[i] \
                        else 'X'
                self.alignments.append(aln)

    def _print(self, start, end):
        print ''.join(self.query_seq[start:end])
        print ''.join(self.alignments[start:end])
        print ''.join(self.subject_seq[start:end])
        print

    def print_alignment(self, start=0, end_pos=None, width=60):

        if not self.alignments:
            self.update_alignments()

        print 'qstart = %d, qstop = %d, sstart = %d, sstop = %d' % (
                                                    self.query_start,
                                                    self.query_stop,
                                                    self.subject_start,
                                                    self.subject_stop)
        if not end_pos:
            end_pos = len(self.query_seq)

        if width > (end_pos - start):
            self._print(start, end_pos)
        else:
            end = width
            for i in range(end_pos/width):
                self._print(start, end)
                start = end
                end += width

            if (end_pos % width) > 0:
                end = end_pos
                self._print(start ,end)

    def report_snps(self):
        for i in range(len(self.query_seq)):
            if self.query_seq[i] != self.subject_seq[i]:
                query_pos = i
                subject_pos = self.subject_start + i
                yield (self.query,
                        query_pos + 1,
                        self.subject,
                        subject_pos + 1,
                        self.query_seq[i],
                        self.subject_seq[i])


def read(input_file):
    query = None
    subject = None

    for line in open(input_file):
        if line.startswith('Query='):
            if not query:
                all_hits = []
                query = line.split()[1].lstrip()
            else:
                yield all_hits
                query = line.split()[1].lstrip()
                all_hits = []

        if line.startswith('>'):
            subject = line.replace('>', '').strip()
            hit = BlastHit(query, subject)
            all_hits.append(hit)

        if query and subject:
            if line.startswith('Query:'):
                hit.add_query_seq(line)
            if line.startswith('Sbjct:'):
                hit.add_subject_seq(line)
    yield all_hits


def main():

    for query in read(input_file):
        for hit in query:
            print hit.query, hit.subject
            # hit.query_seq[9] = 'T'
            hit.update_alignments()
            hit.print_alignment(0, 60)
            # for snp in hit.report_snps():
            #     print snp

            # print hit.find_match_subject(113026028)
            # print hit.find_match_query(60)


if __name__ == '__main__':
    input_file = sys.argv[1]
    main()

