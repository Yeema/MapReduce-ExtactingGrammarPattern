hadoop fs -rm -r yihuei/final/out
hadoop fs -rm -r yihuei/final/patterns
yarn jar $HADOOP_STREAMING -files mapper.py,reducer.py -mapper 'python3 mapper.py' -reducer 'python3 reducer.py' -input yihuei/final/UM-Corpus.en.200k.tagged.txt -output yihuei/final/out -numReduceTasks 32 && hadoop fs -getmerge yihuei/final/out patterns
hadoop fs -put patterns yihuei/final/patterns
hadoop fs -rm -r yihuei/final/out
yarn jar $HADOOP_STREAMING -files mapper1.py,reducer1.py -mapper 'python3 mapper1.py' -reducer 'python3 reducer1.py' -input yihuei/final/patterns -output yihuei/final/out -numReduceTasks 32 && hadoop fs -getmerge yihuei/final/out out
cat out | sort > result
rm out
