#!/bin/bash
for((ii=5;ii<70;ii++))
do
    echo $ii
    mkdir part_${ii}
    cd part_${ii}
    ln -s /projectnb/cui-buchem/tanmoy/projects/ML_delta/methox/datagen/fixed_solute_md .
    ln -s ../sccdftb.dat .
    sed "s/_RNUM_/${ii}/g" ../run_qmmm_dft.inp > run_qmmm_dft.inp
    sed "s/_RNUM_/${ii}/g"  ../run_qmmm_dftb.inp > run_qmmm_dftb.inp
    sed "s/_PART_/${jj}/g" ../sub_dft.sh > sub_dft.sh
    cp ../sub_dftb.sh .
    qsub sub_dft.sh
    bash sub_dftb.sh
    cd ../  
done