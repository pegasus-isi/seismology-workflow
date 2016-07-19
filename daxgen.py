#!/usr/bin/env python
import sys
import os
from Pegasus.DAX3 import *

# API Documentation: http://pegasus.isi.edu/documentation

if len(sys.argv) != 2:
    sys.stderr.write("Usage: %s DAXFILE\n" % (sys.argv[0]))
    exit(1)

daxfile = sys.argv[1]

base_dir = os.path.abspath('.')

# Create a abstract dag
workflow = ADAG("seismology")

# Executable
e_iterdecon = Executable('iterdecon', arch='x86_64', installed=False)
e_iterdecon.addPFN(PFN('file://' + base_dir  + '/bin/iterdecon', 'local'))
workflow.addExecutable(e_iterdecon)

e_sg1iterdecon = Executable('sG1IterDecon', arch='x86_64', installed=False)
e_sg1iterdecon.addPFN(PFN('file://' + base_dir + '/bin/sG1IterDecon', 'local'))
workflow.addExecutable(e_sg1iterdecon)

t_sg1iterdecon = Transformation('sG1IterDecon')
t_sg1iterdecon.uses(e_iterdecon)
t_sg1iterdecon.uses(e_sg1iterdecon)
workflow.addTransformation(t_sg1iterdecon)

e_pysacio = Executable('pysacio.py', arch='x86_64', installed=False)
e_pysacio.addPFN(PFN('file://' + base_dir + '/bin/pysacio.py', 'local'))
workflow.addExecutable(e_pysacio)

e_pytutil = Executable('pytutil.py', arch='x86_64', installed=False)
e_pytutil.addPFN(PFN('file://' + base_dir + '/bin/pytutil.py', 'local'))
workflow.addExecutable(e_pytutil)

e_siftsstfbymisfit = Executable('siftSTFByMisfit', arch='x86_64', installed=False)
e_siftsstfbymisfit.addPFN(PFN('file://' + base_dir + '/bin/siftSTFByMisfit.py', 'local'))
workflow.addExecutable(e_siftsstfbymisfit)

t_siftsstfbymisfit = Transformation('siftSTFByMisfit')
t_siftsstfbymisfit.uses(e_pytutil)
t_siftsstfbymisfit.uses(e_pysacio)
t_siftsstfbymisfit.uses(e_siftsstfbymisfit)
workflow.addTransformation(t_siftsstfbymisfit)

# Cluster Profile
p_cluster = Profile(Namespace.PEGASUS, 'clusters.size', '50')
e_sg1iterdecon.addProfile(p_cluster)

# IterDecon Jobs
output_files = []

for base_file in os.listdir('input/EGF'):
  j_iterdecon = Job(name='sG1IterDecon')

  f_mshock = File('mshock-' + base_file)
  f_mshock.addPFN(PFN('file://' + os.path.abspath('input/MShock') + '/' + base_file, 'local'))
  workflow.addFile(f_mshock)

  f_egf = File('egf-' + base_file)
  f_egf.addPFN(PFN('file://' + os.path.abspath('input/EGF') + '/' + base_file, 'local'))
  workflow.addFile(f_egf)

  out_name = base_file + '_iter_g1.stf'
  output_files.append(out_name)
  f_decon = File(out_name)

  j_iterdecon.uses(f_mshock, link=Link.INPUT)
  j_iterdecon.uses(f_egf, link=Link.INPUT)
  j_iterdecon.uses(f_decon, link=Link.OUTPUT, transfer=False)
  j_iterdecon.addArguments(f_mshock, f_egf)
  workflow.addJob(j_iterdecon)

# siftsSTFByMisfit Job
j_siftsstfbymisfit = Job(name='siftSTFByMisfit')

for out_name in output_files:
  f_decon = File(out_name)
  j_siftsstfbymisfit.uses(f_decon, link=Link.INPUT)
  j_siftsstfbymisfit.addArguments(out_name)

f_fits = File('good-fits.tar.gz')
j_siftsstfbymisfit.uses(f_fits, link=Link.OUTPUT, transfer=True)

workflow.addJob(j_siftsstfbymisfit)

# Write the DAX to file
f = open(daxfile, "w")
workflow.writeXML(f)
f.close()
