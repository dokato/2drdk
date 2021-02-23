import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

import hddm

from patsy import dmatrix

data = pd.read_csv('data/trials_all.csv')

# Preprocess the Reaction Times data for format required by hddm.

data = data[data['rt'] != data['rt'].max()] # removing outliers in the 45
data = data[data['rt'] != data['rt'].max()]

dataf = data[data['rt'] > 0]
dataf = dataf[~(dataf.rt < 250)]
#dataf = hddm.utils.flip_errors(dataf) # optional
dataf.rt = dataf.rt/1000 # rt in ms
dataf.reset_index(inplace = True, drop = True) # needed for posterior generative plots (otherwise errors out)

def single_run(dbname = 'traces_1.db', model_save = 'hddm_model_vta_no.ml',
               generative_save = 'ppc_vta1.csv'):
    '''
    INPUT:
      dbname (str) - name of the sqlite db for model params saving
      model_save (str) - name of the sqlite db for model params saving
    OUTPUT:
     save model and predictive values to specified CSV files
    '''
    m = hddm.HDDM(dataf,
              #include=['sv', 'st'], group_only_nodes=['sv', 'st'],
              #include=('st'), include=('sv', 'st', 'sz'),
              depends_on={'v': ['condition', 'angle'],
                          't': ['condition', 'angle'],
                          'a': ['condition', 'angle']},
              p_outlier=0.05)
    m.find_starting_values()
    m.sample(20000, burn=5000, thin=2, dbname=dbname, db='pickle')
    m.save(mode_save)
    ppc_data = hddm.utils.post_pred_gen(m, samples=10)
    ppc_data.to_csv(generative_save)

def multiple_run():
    '''
    OUTPUT:
        Prints out the gelman rubin stats and min and max rho values below.     
    '''
    models = []
    for i in range(5):
        m = hddm.HDDM(dataf,
                #include=['sv', 'st'], group_only_nodes=['sv', 'st'],
                #include=('st'), include=('sv', 'st', 'sz'),
                depends_on={'v': ['condition', 'angle'],
                            't': ['condition', 'angle'],
                            'a': ['condition', 'angle']},
                p_outlier=0.05)

        m.find_starting_values()
        m.sample(20000, burn=5000, thin=2)
        models.append(m)

    print('\n---\n')
    print(gelman_rubin(models))

    dd = gelman_rubin(models)

    rhos = []
    for k in dd:
        rhos.append(dd[k])

    print(min(rhos), max(rhos))

if __name__ == "__main__":
    single_run()
    #multiple_run()
