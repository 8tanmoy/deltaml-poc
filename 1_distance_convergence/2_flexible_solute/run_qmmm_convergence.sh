#!/bin/bash
jj=70
for((ii=5;ii<70;ii++))
do
    echo $ii
    mkdir part_${ii}
    cd part_${ii}
    ln -s /projectnb/cui-buchem/tanmoy/projects/ML_delta/datagen/flexible_solute_md ./trajdir
    ln -s ../sccdftb.dat .
    ln -s /projectnb/cui-buchem/tanmoy/projects/water_clusters/parameters/3ob/3ob-3-1/ .
    sed "s/_PART_/${jj}/g" ../run_qmmm_dft.inp  | sed "s/_RNUM_/${ii}/g" > run_qmmm_dft.inp
    sed "s/_PART_/${jj}/g" ../run_qmmm_dftb.inp | sed "s/_RNUM_/${ii}/g" > run_qmmm_dftb.inp
    sed "s/_PART_/${jj}/g" ../sub_dft.sh > sub_dft.sh
    cp ../sub_dftb.sh .
    qsub sub_dft.sh
    bash sub_dftb.sh
    cd ../  
done