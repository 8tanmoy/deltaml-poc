for ((ii=0;ii<11;ii++)) do
    for ((jj=0;jj<11;jj++)) do
        echo $ii $jj
        poat=`echo "1.5+(${ii}*0.2)" | bc`
        polg=`echo "1.5+(${jj}*0.2)" | bc`
        echo $poat $polg
        wrk=part_${ii}_${jj}
        mkdir $wrk
        cd $wrk
        ln -s /projectnb/cui-buchem/tanmoy/projects/RL/methox/try7/delta/toppar .
        ln -s /projectnb/cui-buchem/tanmoy/projects/ML_delta/methox/datagen/confs .
        ln -s /projectnb/cui-buchem/tanmoy/projects/ML_delta/methox/2_ad_map_sol/wat .
        #-- replace dummies with numbers --
        sed "s/_@POAT@_/${poat}/g" ../1_run_umbrella_md.inp | \
        sed "s/_@POLG@_/${polg}/g" >  1_run_umbrella_md.inp
        cp ../sccdftb.dat .
        cp ../sub_dftb_md.sh .
        qsub sub_dftb_md.sh
        cd ../
    done
done