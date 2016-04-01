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

#Author: Son Pham
#Contact: kspham@eng.ucsd.edu

#Re-written by Dan Browne on 04/01/2016

from utils import rc
import subprocess
from pyfaidx import Fasta

#parse graph vertices

def graph_vertices(filename):
    proc = subprocess.Popen(["grep", "'l='", filename], stdout=subprocess.PIPE)
    graph = proc.communicate()[0].split('\n')[:-1]
    graph = [x.split(' ') for x in graph[::2]]
    for x in graph:
        vid = int(x[0][1:-2])
        vid_conj = -1 * vid
        length = int(x[1][3:])
        cov = int(x[2][2:-1])
        yield vid, vid_conj, length, cov


#parse graph edges

def graph_edges(filename):
    proc = subprocess.Popen(["grep", "'>'", filename], stdout=subprocess.PIPE)
    graph = proc.communicate()[0].split('\n')[:-1]
    graph = [x.split(' ') for x in graph]
    proc = subprocess.Popen(["grep", "'edge'", filename], stdout=subprocess.PIPE)
    defaultoverlap = int(proc.communicate()[0].translate(None, "edge[] \n"))
    for x in graph:
        v1id = lambda x: -1 * int(x[0][1:-2]) if x[0][-2] == '-' else int(x[0][1:-2])
        v2id = lambda x: -1 * int(x[2][1:-2]) if x[2][-2] == '-' else int(x[2][1:-2])
        newoverlap = lambda x: int(x[3][3:-1]) if len(x) == 4 else defaultoverlap
        yield v1id, v2id, newoverlap



def contigs_sequence(filename):
    contigs = Fasta(filename)
    for x in range(len(contigs)):
        yield int(contigs[x].name), contigs[x]
        yield int(-1 * contigs[x].name), rc(contigs[x])


