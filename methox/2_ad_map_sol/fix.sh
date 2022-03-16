needfix=(part_0_5 part_4_9 part_4_10 part_5_0 part_5_1 part_5_2 part_5_3 part_5_4 part_5_5 part_5_6 part_5_7 part_5_8 part_5_9 part_6_7 part_6_10 part_7_0 part_7_7 part_10_3)
for item in "${needfix[@]}"
do
    echo $item
    cd $item
    #-- fix frames --
    rm -rf frames/
    mkdir frames
    cd frames
    cp ../../run_frames_splitter.inp .
    /usr3/graduate/tanmoy/packages/c43a1/exec/em64t_M/charmm < run_frames_splitter.inp > run_frames_splitter.out
    rm run_frames_splitter*
    cd ../
    #-- run DFTB --
    bash sub_dftb.sh
    #-- submit DFT job --
    cp ../sub_dft.sh .
    cp ../run_qmmm_dft.inp .
    qsub sub_dft.sh
    cd ../
done
