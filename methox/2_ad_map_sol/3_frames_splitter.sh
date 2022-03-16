for ((ii=0;ii<11;ii++)) do
    for ((jj=0;jj<11;jj++)) do
        echo $ii $jj
        poat=`echo "1.5+(${ii}*0.2)" | bc`
        polg=`echo "1.5+(${jj}*0.2)" | bc`
        echo $poat $polg
        wrk=part_${ii}_${jj}
        cd $wrk
        mkdir frames
        cd frames
        cp ../../run_frames_splitter.inp .
        /usr3/graduate/tanmoy/packages/c43a1/exec/em64t_M/charmm < run_frames_splitter.inp > run_frames_splitter.out
        rm run_frames_splitter*
        cd ../../
    done
done