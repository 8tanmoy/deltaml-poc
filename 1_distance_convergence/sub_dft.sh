#!/bin/bash -l
#$ -l h_rt=12:00:00
#$ -j y
#$ -N delta_gau
#$ -pe omp 8

INPUTFILE=run_qmmm_dft.inp
OUTPUTFILE=run_qmmm_dft.out

part=10
origin=$PWD

if [ ! -d "/scratch/tanmoy" ]
then
    mkdir -p /scratch/tanmoy/malon_part_${part}
    pushd /scratch/tanmoy/malon_part_${part}
    echo $PWD
else
    cd /scratch/tanmoy
    if [ ! -d "malon_part_${part}" ]
    then
        mkdir malon_part_${part}
    else
        rm malon_part_${part}/*
    fi
    pushd malon_part_${part}
    echo $PWD
fi

module load intel/2019
module load gaussian/16.B.01
module load openmpi/4.0.1_intel-2019

ln -s /projectnb/cui-buchem/tanmoy/projects/ML_delta/datagen/fixed_solute_md .
/usr3/graduate/tanmoy/packages/c43a1-g09/exec/em64t_M/charmm < $origin/$INPUTFILE >& $origin/$OUTPUTFILE

cp en_dft_${part}.dat   $origin
cp forces_dft.dat       $origin
cp forces_ma_dft.dat    $origin
popd