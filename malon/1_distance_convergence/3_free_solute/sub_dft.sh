#!/bin/bash -l
#$ -l h_rt=24:00:00
#$ -j y
#$ -N delta_gau
#$ -pe omp 8

module load intel/2019
module load gaussian/16.B.01
module load openmpi/4.0.1_intel-2019

/usr3/graduate/tanmoy/packages/c43a1-g09/exec/em64t_M/charmm < run_qmmm_dft.inp > run_qmmm_dft.out
