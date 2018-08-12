#!/bin/sh
for i in 12
do
N=$i
name="N"$N"C"
echo $name
cd $name
for j in 0.00001 0.0001 0.001 0.01 0.1
do
g=$j
echo $g
echo $PWD
qsub -q workq <<END_OF_PBS
#!/bin/sh
#PBS -l walltime=72:00:00
#PBS -j oe
#PBS -k oe
#PBS -q new
#PBS -l nodes=1:ppn=32
#PBS -l mem=200gb
#PBS -m ae
#PBS -M pranav.s@theory.tifr.res.in
# The following line specifies the name of the job
#PBS -N $name$g
cd \${PBS_O_WORKDIR}
echo \${PBS_O_WORKDIR}
#########################################################################
cd \${PBS_O_WORKDIR}/$name$g
echo "eig.py" > ./output_eig.txt
echo \`hostname\` \`date\` >> ./output_eig.txt
/usr/bin/time -o time_eig ../../eig.py -N $N -g $g>> ./output_eig.txt 2>./errors_eig.txt
echo \`date\` >> ./output_eig.txt

cd \${PBS_O_WORKDIR}
exit 0

END_OF_PBS
done
cd ..
done
echo "DONE"
qstat -a
