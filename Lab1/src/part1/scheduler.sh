rm -rf output_files
mkdir output_files
i=1
while [ $i -le $1 ]
do
python3 client.py >> ./output_files/output_$i.txt &
i=`expr $i + 1`
done