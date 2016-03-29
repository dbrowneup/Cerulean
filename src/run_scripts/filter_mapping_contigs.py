# This software is Copyright 2013 The Regents of the University of
# California. All Rights Reserved.
#
# Permission to copy, modify, and distribute this software and its
# documentation for educational, research and non-profit purposes, without fee,
# and without a written agreement is hereby granted, provided that the above
# copyright notice, this paragraph and the following three paragraphs appear
# in all copies.
#
# Permission to make commercial use of this software may be obtained by
# contacting:
# Technology Transfer Office
# 9500 Gilman Drive, Mail Code 0910
# University of California
# La Jolla, CA 92093-0910
# (858) 534-5815
# invent@ucsd.edu
#
# This software program and documentation are copyrighted by The Regents of the
# University of California. The software program and documentation are supplied
# "as is", without any accompanying services from The Regents. The Regents does
# not warrant that the operation of the program will be uninterrupted or
# error-free. The end-user understands that the program was developed for
# research purposes and is advised not to rely exclusively on the program for
# any reason.
#
# IN NO EVENT SHALL THE UNIVERSITY OF CALIFORNIA BE LIABLE TO
# ANY PARTY FOR DIRECT, INDIRECT, SPECIAL, INCIDENTAL, OR
# CONSEQUENTIAL DAMAGES, INCLUDING LOST PROFITS, ARISING
# OUT OF THE USE OF THIS SOFTWARE AND ITS DOCUMENTATION,
# EVEN IF THE UNIVERSITY OF CALIFORNIA HAS BEEN ADVISED OF
# THE POSSIBILITY OF SUCH DAMAGE. THE UNIVERSITY OF
# CALIFORNIA SPECIFICALLY DISCLAIMS ANY WARRANTIES,
# INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.
# THE SOFTWARE PROVIDED HEREUNDER IS ON AN "AS IS" BASIS, AND THE UNIVERSITY OF
# CALIFORNIA HAS NO OBLIGATIONS TO PROVIDE MAINTENANCE, SUPPORT, UPDATES,
# ENHANCEMENTS, OR MODIFICATIONS.

#Author: Viraj Deshpande
#Contact: vdeshpan@eng.ucsd.edu

from PacbioMapping import PacbioMapping
from PacbioAlignment import PacbioAlignment
from illumina_graph import Graph


ig = Graph()
ig.load('../../data/spalgae/spalgae-contigs.dot',
        '../../data/spalgae/spalgae-contigs.fasta')
print 'Graph loaded'


pbm = PacbioMapping('../../data/scobliq_chloroplast/scobliq_contigs_ref_mapping.blastn',
                    'blastn', 0.9)

print 'Mapping loaded'

f = open('../../data/scobliq_chloroplast/scobliq_mapping-contigs.fa', 'w')

rr = pbm.readToContig.keys()
rr.sort()

for r in rr:
    found = False
    for m in pbm.readToContig[r]:
        a = PacbioAlignment(m, 'blastn')
        if a.align_length() > 0.9 * a.queryLen:
            found = True
            break
    if found:
        f.write('>' + r + '\n')
        f.write(ig.vs[int(a.queryID)].seq + '\n')

f.close()