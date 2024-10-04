#!/bin/bash

# ./correct-all.sh path-to-entregas-dir

entregas=$1 # path to DIR with ONLY ZIPs of entregas

# Create CSV with corrections
echo "student,grupo,lectura,lconnect_0,lconnect_1,publish_0,publish_1,qos0_0,qos0_1,qos1,qos1,double,total" > notas.csv

# Put there just the files avoiding folder recursion
mkdir /tmp/clean-entregas

for entrega in `ls $entregas`; do
    # UNZIP submited LAB
    out_zip=/tmp/${entrega::-4}
    unzip $entregas/$entrega -d $out_zip 

    # Create correction DIR
    clean_out=/tmp/clean-entregas/${entrega::-4}
    mkdir $clean_out

    # Copy the JSONs, PCAPNG and LOGs
    for ext in `echo json pcapng log`; do
        for file in `find $out_zip -name *$ext`; do
            # Get filename: https://stackoverflow.com/a/32372307
            fname=`echo "$file" | sed "s/.*\///"`
            cp $file $clean_out/$fname
        done
    done

    # Copy the vitals signs dataset
    cp Human_vital_signs_R.csv $clean_out
done



# Correct each submission, one by one
for submission in `ls /tmp/clean-entregas`; do
    X=${submission:7:10} # get group number X
    group_dir="/tmp/clean-entregas/"$submission

    total=0

    # Print name
    echo ============
    echo = GRUPO $X =
    echo ============

    # Correct the read
    lectura=`python3 correct_lectura.py $X $group_dir`
    echo -e "\tlectura: $lectura"
    total=$(( total + lectura ))

    # Correct the connect
    connect=`python3 correct_connect.py $X "$group_dir"/captura-connect-grupo$X.pcapng $group_dir`
    connect_all=""
    i=0
    for conni in `echo $connect`; do
        echo -e "\tlconnect_$i: $conni"
        connect_all=$connect_all"$conni,"
        i=$(( i + 1 ))
        total=$(( total + conni ))
    done

    # Correct the publish
    publish=`python3 correct_publish.py $X "$group_dir"/captura-publish-grupo$X.pcapng $group_dir`
    i=0
    pub_all=""
    for pubi in `echo $publish`; do
        echo -e "\tpublish_$i: $pubi"
        pub_all=$pub_all"$pubi,"
        i=$(( i + 1 ))
        total=$(( total + pubi ))
    done

    # Correct the QoS 0
    qos0=`python3 correct_qos0.py $X "$group_dir"/qos0-grupo$X.pcapng $group_dir "$group_dir"/qos0-grupo$X.log`
    i=0
    qos0_all=""
    for qos0i in `echo $qos0`; do
        echo -e "\tqos0_$i: $qos0i"
        qos0_all=$qos0_all"$qos0i,"
        i=$(( i + 1 ))
        total=$(( total + qos0i ))
    done

    # Correct the QoS 1
    qos1=`python3 correct_qos1.py $X "$group_dir"/qos1-grupo$X.pcapng $group_dir x1`
    echo -e "\tqos1: $qos1"
    qos1double=`python3 correct_qos1.py $X "$group_dir"/qos1-x2keepalive-grupo$X.pcapng $group_dir x2`
    echo -e "\tqos1double: $qos1double"
    total=$(( total + qos1 + qos1double ))


    # Output final mark
    for student in `grep alumna $group_dir/respuestas-$X.json | cut -d'"' -f4 | sed 's/ /_/g'`; do
        echo $student,$X,$lectura,$connect_all$pub_all$qos0_all$qos1,$qos1double,$total >> notas.csv
    done
done


