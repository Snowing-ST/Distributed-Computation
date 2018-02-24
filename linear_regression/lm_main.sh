#cd ~/Documents/lifeng
chmod +x lm_reducer.py
chmod +x lm_mapper.py
#python lm_mapper.py < ranMat.csv | python lm_reducer.py
hadoop fs -rm -r cufe_situxueying/lab2out2
#hadoop fs -copyFromLocal ranMat.csv cufe_situxueying/
hadoop jar /usr/lib/hadoop-current/share/hadoop/tools/lib/hadoop-streaming-2.7.2.jar -input cufe_situxueying/ranMat.csv -output cufe_situxueying/lab2out2 -file /home/lifeng/pc2017fall/cufe_situxueying/lab2/lm_mapper.py   -mapper "lm_mapper.py" -file /home/lifeng/pc2017fall/cufe_situxueying/lab2/lm_reducer.py -reducer "lm_reducer.py" -numReduceTasks 1

hadoop fs -cat cufe_situxueying/lab2out2/part-00000

#hadoop fs -copyToLocal cufe_situxueying/lab2out2 ~/pc2017fall/cufe_situxueying/lab2
#Rscript ./lm_confirm.R

