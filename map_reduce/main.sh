hadoop jar /usr/lib/hadoop-current/share/hadoop/tools/lib/hadoop-streaming-2.7.2.jar -input cufe_situxueying/LoanStats3c.csv -output cufe_situxueying/loanstatout2 -file /home/lifeng/pc2017fall/cufe_situxueying/Mapper2.py   -mapper "Mapper2.py" -file /home/lifeng/pc2017fall/cufe_situxueying/Reducer.py -reducer "Reducer.py" -numReduceTasks 1

hadoop fs -cat cufe_situxueying/loanstatout2/part-00000
