import os
import sys
base_path = os.path.dirname(__file__)
sys.path.append(base_path)

one_up_path=os.path.abspath(os.path.join(os.path.dirname(__file__),'..'))
sys.path.append(one_up_path)

import util_functions
import essay_set
import feature_extractor
import numpy

from sklearn.ensemble import GradientBoostingClassifier

if not base_path.endswith("/"):
    base_path=base_path+"/"

FILENAME="sa_data.tsv"


all_err=[]
all_kappa=[]

for t_len in [0,50,100,200,300]:
    sa_val = file(FILENAME)
    scores=[]
    texts=[]
    lines=sa_val.readlines()
    eset=essay_set.EssaySet(type="train")
    for i in xrange(1,len(lines)):
        score,text=lines[i].split("\t\"")
        if len(text)>t_len:
            scores.append(int(score))
            texts.append(text)
            eset.add_essay(text,int(score))
            #if int(score)==0:
            #    eset.generate_additional_essays(text,int(score))
    extractor=feature_extractor.FeatureExtractor()
    extractor.initialize_dictionaries(eset)
    train_feats=extractor.gen_feats(eset)
    clf=GradientBoostingClassifier(n_estimators=100, learn_rate=.05,max_depth=4, random_state=1,min_samples_leaf=3)
    cv_preds=util_functions.gen_cv_preds(clf,train_feats,scores)
    err=numpy.mean(numpy.abs(cv_preds-scores))
    print err
    kappa=util_functions.quadratic_weighted_kappa(list(cv_preds),scores)
    print kappa
    all_err.append(err)
    all_kappa.append(kappa)

    """
    outfile=open("full_cvout.tsv",'w+')
    outfile.write("cv_pred" + "\t" + "actual")
    for i in xrange(0,len(cv_preds)):
        outfile.write("{0}\t{1}".format(cv_preds[i],scores[i]))
    """



