for ((ii=0;ii<11;ii++)) do
    for ((jj=0;jj<11;jj++)) do
        echo $ii $jj
        poat=`echo "1.5+(${ii}*0.2)" | bc`
        polg=`echo "1.5+(${jj}*0.2)" | bc`
        echo $poat $polg
        wrk=part_${ii}_${jj}
        cd $wrk
        cp ../sccdftb.dat .
        cp ../run_qmmm_dft.inp .
        cp ../run_qmmm_dftb.inp .
        cp ../sub_dft.sh .
        cp ../sub_dftb.sh .
        #
        bash sub_dftb.sh
        qsub sub_dft.sh
        cd ../
    done
done