for ((ii=0;ii<11;ii++)) do
    for ((jj=0;jj<11;jj++)) do
        #echo $ii $jj
        poat=`echo "1.5+(${ii}*0.2)" | bc`
        polg=`echo "1.5+(${jj}*0.2)" | bc`
        #echo $poat $polg
        wrk=part_${ii}_${jj}
        if grep -R "\*\*\*" ${wrk}/forces_dft.dat
        then
            echo $wrk
        fi 
        #ending=`tail -1 ${wrk}/1_run_umbrella_md.out | grep "MINUTES"`
        #if [[ "$ending" == *"MINUTES"* ]]; then
        #    echo $wrk
        #fi
    done
done