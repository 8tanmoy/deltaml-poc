for ((ii=0;ii<11;ii++)) do
    for ((jj=0;jj<11;jj++)) do
        #echo $ii $jj
        poat=`echo "1.5+(${ii}*0.2)" | bc`
        polg=`echo "1.5+(${jj}*0.2)" | bc`
        #echo $poat $polg
        wrk=part_${ii}_${jj}
        if [ -f ${wrk}/en_dft.dat ]; then
            echo "${wrk} | `cat ${wrk}/en_dft.dat | wc -l`"
        else
            echo "not found ${wrk}"
        fi
    done
done