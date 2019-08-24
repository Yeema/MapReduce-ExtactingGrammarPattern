# MapReduce-ExtactingGrammarPattern

1. goal: Extracting grammar pattern of a headword 
  ```
      ABANDON	V n	abandons the policy | abandons the faith | abandon rash inclinations
      FEED	V n	feed the hungry dream | feeds hundreds | feeding material part
  ```
2. input: A corpus is POS tagged by [geniatagger](https://github.com/d2207197/geniatagger-python)
  ```
      original:
      All that remains for me to do is to say good-bye.
      All the commune members young and old, went out to hervest the crops.
      
      POS tagging with allignment preprocessing:
      [('all that', 'remains', 'for', 'me', 'to', 'do is', 'to', 'say', 'good-bye', '.'), 
      ('all that', 'remain', 'for', 'me', 'to', 'do be', 'to', 'say', 'good-bye', '.'), 
      ('PDT DT', 'VBZ', 'IN', 'PRP', 'TO', 'VB VBZ', 'TO', 'VB', 'NN', '.'), 
      ('I-NP H-NP', 'H-VP', 'H-PP', 'H-NP', 'H-TO', 'I-VP H-VB', 'H-TO', 'H-VP', 'H-NP', 'O')]
      [('all the commune members', ',', 'young and old', ',', 'went', 'out', 'to', 'hervest', 'the crops', '.'), 
      ('all the commune member', ',', 'young and old', ',', 'go', 'out', 'to', 'hervest', 'the crop', '.'), 
      ('PDT DT JJ NNS', ',', 'JJ CC JJ', ',', 'VBD', 'RP', 'TO', 'VB', 'DT NNS', '.'), 
      ('I-NP I-NP I-NP H-NP', 'O', 'I-NP I-NP H-NP', 'O', 'H-VP', 'H-PRT', 'H-TO', 'H-VP', 'I-NP H-NP', 'O')]
  ```
3. environment: HDFS
4. usage cmd: sh execute.sh
    * remember to change the filepath in execute.sh
