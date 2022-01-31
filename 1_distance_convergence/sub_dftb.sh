#!/bin/bash -l
#$ -l h_rt=00:30:00
#$ -j y
#$ -N mal
#$ -pe omp 1

module load intel/2019
module load openmpi/4.0.1_intel-2019
module load python3/3.7.9

/usr3/graduate/tanmoy/packages/c43a1/exec/em64t_M/charmm < run_qmmm_dftb.inp > run_qmmm_dftb.out
