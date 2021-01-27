import re
import os, glob
import pandas as pd
import numpy as np
import scipy.stats as st
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.utils import resample

# Loading data and extracting information

def extract_name_pattern(file_path, prefix = 'a'):
    '''
    From file path it returns info about an angle and subject id.
    Assumes file name pattern: '<prefix><angle>_<id>.csv'
    '''
    file_name = file_path.split('/')[-1]
    rx = re.compile(prefix + r'([0-9][0-9])_([0-9]+)\.')
    angle, subj_id = rx.findall(file_name)[0]
    return (int(angle), int(subj_id))

def extract_data_from_part2(dfp2, column_name, condition_tuple):
    '''
    IN:
      *dfp2* data frame from Part 2 of 2d RDK (must have *cohfix* column with tuples)
      *column_name* str with column name with observation of interests
      *condition_tuple* is coherencies you want to extract in a tuple, eg. (0, 0.6)
    OUT:
      vector with extracted data
    '''
    assert 'cohfix' in dfp2.columns, 'dfp2 lacks cohfix column'
    return dfp2[dfp2.cohfix.map(lambda x: list(x) == sorted(condition_tuple))][column_name].to_numpy()*1.

def compute_mean_sterr_from_vector(vect):
    'Returns tuple with mean and sterr from *vect*'
    return np.mean(vect), np.std(vect)/np.sqrt(len(vect))

def get_avg_conditions_part2(dfp2, delta, stair_coh1, stair_coh2, column = 'correct', control = 0.6):
    '''
    Extracts average summaries from all coditions from dfp2 matrix
    IN:
      *dfp2* data frame from Part 2 of 2d RDK
      *delta, stair_coh1, stair_coh2, control* coherencies for conditions
         (control has default 0.6)
      *column* column with data of interests
    OUT:
      dictionary with extracted data from part of of experiment
    '''
    v_ = extract_data_from_part2(dfp2, column, [delta, stair_coh1])
    cong_m, cong_s = compute_mean_sterr_from_vector(v_)
    v_ = extract_data_from_part2(dfp2, column, [0, stair_coh2])
    cong_true_m, cong_true_s = compute_mean_sterr_from_vector(v_)
    v_ = extract_data_from_part2(dfp2, column, [delta, stair_coh2])
    incong_m, incong_s = compute_mean_sterr_from_vector(v_)
    v_ = extract_data_from_part2(dfp2, column, [0, stair_coh1])
    incong_true_m, incong_true_s = compute_mean_sterr_from_vector(v_)
    if not control is None:
        v_ = extract_data_from_part2(dfp2, column, [0, control])
        contr_m, contr_s = compute_mean_sterr_from_vector(v_)
    else:
        contr_m, contr_s = 0, 0
    return {'cong_m':cong_m, 'cong_s':cong_s, 'cong_true_m':cong_true_m, 'cong_true_s': cong_true_s,\
            'incong_m':incong_m, 'incong_s':incong_s, 'incong_true_m':incong_true_m, 'incong_true_s':incong_true_s,\
            'contr_m':contr_m, 'contr_s':contr_s}

def load_trial_data_part2(dfp2, delta, stair_coh1, stair_coh2):
    '''
    Loads single-trial data from part 2 and encodes conditions.
    IN:
      *dfp2* data frame from Part 2 of 2d RDK
      *delta, stair_coh1, stair_coh2* coherencies for conditions
    OUT:
      data frame with selected columns and encoded conditions.
    '''
    condition_tuple = [delta, stair_coh1]
    dfp2.loc[dfp2.cohfix.map(lambda x: list(x) == sorted(condition_tuple)), "axes"] = 2
    dfp2.loc[dfp2.cohfix.map(lambda x: list(x) == sorted(condition_tuple)), "cogr"] = 1
    dfp2.loc[dfp2.cohfix.map(lambda x: list(x) == sorted(condition_tuple)), "condition"] = "C2"
    condition_tuple = [0, stair_coh2]
    dfp2.loc[dfp2.cohfix.map(lambda x: list(x) == sorted(condition_tuple)), "axes"] = 1
    dfp2.loc[dfp2.cohfix.map(lambda x: list(x) == sorted(condition_tuple)), "cogr"] = 1
    dfp2.loc[dfp2.cohfix.map(lambda x: list(x) == sorted(condition_tuple)), "condition"] = "C1"
    condition_tuple = [delta, stair_coh2]
    dfp2.loc[dfp2.cohfix.map(lambda x: list(x) == sorted(condition_tuple)), "axes"] = 2
    dfp2.loc[dfp2.cohfix.map(lambda x: list(x) == sorted(condition_tuple)), "cogr"] = 0
    dfp2.loc[dfp2.cohfix.map(lambda x: list(x) == sorted(condition_tuple)), "condition"] = "I2"
    condition_tuple = [0, stair_coh1]
    dfp2.loc[dfp2.cohfix.map(lambda x: list(x) == sorted(condition_tuple)), "axes"] = 1
    dfp2.loc[dfp2.cohfix.map(lambda x: list(x) == sorted(condition_tuple)), "cogr"] = 0
    dfp2.loc[dfp2.cohfix.map(lambda x: list(x) == sorted(condition_tuple)), "condition"] = "I1"
    dfp2 = dfp2[['rt', 'correct', 'axes', 'cogr', 'condition']]
    return dfp2.dropna()

def read_part1(df):
    '''
    Reads data from Part 1 of 2d RDK experiment
    IN:
      *df* - pd.DataFrame
        dataframe with data read
    OUT:
      dictionary with all the details
    '''
    stair_coh1 = float(df.stair_coh1[df.stair_coh1>0])
    stair_coh2 = float(df.stair_coh2[df.stair_coh2>0])
    delta_st   = np.abs(stair_coh1-stair_coh2)
    stair_coh1 = np.round(stair_coh1, 5)
    stair_coh2 = np.round(stair_coh2, 5)
    delta_st   = np.round(delta_st, 5)
    part_1_start = np.where(df['stimulus'].str.contains('You are ready to start <b>PART 1</b>').to_numpy()==True)[0][0]
    part_1_end = np.where(df['stimulus'].str.contains('You successfully finished PART 1').to_numpy()==True)[0][0]
    dfp1 = df.iloc[part_1_start:part_1_end,:]
    dfp1 = dfp1[dfp1.trial_type == 'RDK']
    rx = re.compile("<font color='grey'>(.*)</font>")
    dfp1['which_stair'] = df.iloc[dfp1.index-2].stimulus.map(lambda x: rx.findall(x)[0]).to_numpy()
    stairs_c1 = [(float(c.split(',')[0]), float(c.split(',')[1])) for c in dfp1[dfp1['which_stair']=='coh1'].coherence.to_numpy()]
    stairs_c1 = [c1 if c2 == 0 else c2 for c1,c2 in stairs_c1]
    stairs_c2 = [(float(c.split(',')[0]), float(c.split(',')[1])) for c in dfp1[dfp1['which_stair']=='coh2'].coherence.to_numpy()]
    stairs_c2 = [c1 if c2 == 0 else c2 for c1,c2 in stairs_c2]
    return {'stair_coh1':stair_coh1, 'stair_coh2':stair_coh2, 'delta':delta_st, 'stairs_c1': stairs_c1, 'stairs_c2': stairs_c2}

def read_part2(df, delta, stair_coh1, stair_coh2):
    '''
    Reads data from Part 1 of 2d RDK experiment
    IN:
      *df* - pd.DataFrame
        dataframe with data read
    OUT:
      dictionary with all the details
    '''
    part_2_start = np.where(df['stimulus'].str.contains('You are ready to start PART 2').to_numpy()==True)[0][0]
    part_2_end = np.where(df['stimulus'].str.contains('You finished the last block!').to_numpy()==True)[0][0]
    dfp2 = df.iloc[part_2_start:part_2_end,:]
    dfp2 = dfp2[dfp2.trial_type == 'RDK']
    dfp2['cohfix'] = dfp2.coherence.str.split(',').map(lambda x: tuple(np.round(sorted((float(x[0]), float(x[1]))),5)))

    dfp2 = dfp2[['rt', 'correct', 'time_elapsed', 'cohfix']]

    corrects = get_avg_conditions_part2(dfp2, delta, stair_coh1, stair_coh2, 'correct')
    rts = get_avg_conditions_part2(dfp2, delta, stair_coh1, stair_coh2, 'rt')
    single_trial = load_trial_data_part2(dfp2, delta, stair_coh1, stair_coh2)
    return {'corrects': corrects, 'rts':rts, 'trials':single_trial}

def read_data_from_2drdk(path):
    '''
    Reads data from 2d RDK experiment and parses the most important information.
    IN:
      *path* - str
        path to the file from
    OUT:
      dictionary with all the details
    '''
    df = pd.read_csv(path)
    # decode the file name
    angle, subj_id = extract_name_pattern(path)
    subj_id = '{}_{}'.format(angle, subj_id)
    # reading data from part 1
    part1 = read_part1(df)
    # reading data from part 2
    part2 = read_part2(df, part1['delta'], part1['stair_coh1'], part1['stair_coh2'])
    return {'part1': part1, 'part2': part2, 'angle': angle, 'subj_id': subj_id}

def read_data_practise(path):
    '''
    Read data from practise part and return number of trials and accuracy
    IN:
      *path* - read path
    OUT:
     tuple with nr of trials and accuracy and angle at the end
    '''
    df = pd.read_csv(path)
    angle, subj_id = extract_name_pattern(path)
    practise_1_str = np.where(df['stimulus'].str.contains('Let\'s try a few more times to practice.').to_numpy()==True)[0][0]
    practise_1_end = np.where(df['stimulus'].str.contains('You are ready to start <b>PART 1</b>').to_numpy()==True)[0][0]

    dfpr = df.iloc[practise_1_str:practise_1_end,:]
    dfpr = dfpr[dfpr.trial_type == 'RDK']
    return (dfpr.shape[0], np.mean(dfpr.correct[-16:]*1), angle)

# Stats

def confidence_bootstrap(x, y, Nr = 1000, two_sided = False, interval = 95):
    '''
    Compute bootstraped cofidence intervals for XY mean difference.
    IN:
      *x, y* - list, np.array
        data arrays / lists
      *Nr* - int
        number of resampling
      *two_sided* - bool
        if True tests absolute difference, if False y > x
      *alpha* - int
        if True tests absolute difference, if False y > x
    OUT:
      confidence intervals
    '''
    assert interval < 100, "interval must be > 0 and < 100"
    diffs = np.zeros((Nr,))
    for i in range(Nr):
        nx = resample(x, n_samples = len(x))
        ny = resample(y, n_samples = len(y))
        sub = np.mean(ny) - np.mean(nx)
        diffs[i] = sub if two_sided else np.abs(sub)
    return (st.scoreatpercentile(diffs, 100 - interval), st.scoreatpercentile(diffs, interval))

# Plotting

def plot_barplot_two_means(avg1, ste1, avg2, ste2, p_val = None,
                           name1 = 'A', name2 = 'B',
                           y_lim = None, y_label = None, x_label = None, bar_col = 'grey',
                           shift = 0.2, alpha = 0.05):
    '''
    Plots two barplot from two means and standard errors.
    IN:
      *avg1*, *avg2* - float
        average 1 and average 2
      *ste1*, *ste2* - float
        standard errors 1 & 2
      *p_val* - float
        p value from statistical test comapring two groups
      *name1* = 'A', *name2* = 'B' - str, int
        names to display on x axis
      *y_lim* - list of 2 elements, tuple
        limits of y axis
      *y_label*, *x_label* - str
        y,x label
      *bar_col* = 'grey' - str
        barplto colour
      *shift* - float
        shift between bars
      *alpha* - float
        significance level (only if *p_val* provided)
    OUT:
      plot from matplotlib
    '''
    if y_lim:
        min_lim = y_lim[0]
        max_lim = y_lim[-1]
    else:
        min_lim = 0
        max_lim = np.max([avg1, avg2])
    plt.bar([0, 1], [avg1, avg2], yerr = [ste1, ste2], color = bar_col)
    plt.xticks([0, 1], [name1, name2])
    if y_lim:
        plt.ylim(y_lim)
    if x_label:
        plt.xlabel(x_label)
    if y_label:
        plt.ylabel(y_label)
    plt.text(0-shift, min_lim+0.5*(max_lim-min_lim), '{:.2f} +- {:.2f}'.format(avg1, ste1))
    plt.text(1-shift, min_lim+0.5*(max_lim-min_lim), '{:.2f} +- {:.2f}'.format(avg2, ste2))
    if p_val:
        plt.text(0.5-shift, 0.9*max_lim, '{} ({})'.format('*' if p_val < alpha else 'ns',
                                            "p={:.2f}".format(p_val) if p_val >= 0.01 else "p<0.01"))


def plot_paired_value_lines(group1_vals, group2_vals, p_val = None,
                           name1 = 'A', name2 = 'B',
                           y_lim = None, y_label = None, x_label = None,
                           shift = 0.2, alpha = 0.05):
    '''
    Plots paired values by dots connected with lines.
    IN:
      *group1_vals*, *group2_vals* - list
        values from the first and second groups (need to have the same length)
      *p_val* - float
        p value from statistical test comapring two groups
      *name1* = 'A', *name2* = 'B' - str, int
        names to display on x axis
      *y_lim* - list of 2 elements, tuple
        limits of y axis
      *y_label*, *x_label* - str
        y,x label
      *shift* - float
        shift between bars
      *alpha* - float
        significance level (only if *p_val* provided)
    OUT:
      plot from matplotlib
    '''
    assert len(group1_vals) == len(group2_vals), "length of groups is not the same"
    if y_lim:
        max_lim = y_lim[-1]*0.9
    else:
        max_lim = np.max([np.max(group1_vals), np.max(group2_vals)])
    for i in range(len(group1_vals)):
        plt.plot([0, 1], [group1_vals[i], group2_vals[i]], 'o-')
    plt.xticks([0, 1], [name1, name2])
    plt.xlim([-0.5, 1.5])
    if y_lim:
        plt.ylim(y_lim)
    if x_label:
        plt.xlabel(x_label)
    if y_label:
        plt.ylabel(y_label)
    if p_val:
        plt.text(0.5-shift, 0.9*max_lim, '{} ({})'.format('*' if p_val < alpha else 'ns',
                                                                "p={:.2f}".format(p_val) if p_val >= 0.01 else "p<0.01"),
                bbox=dict(boxstyle="round", fc='#ced5df', alpha=0.8))

def plot_two_violin_plots(values1, values2, p_val = None,
                          name1 = 'A', name2 = 'B',
                          y_lim = None, y_label = None, x_label = None,
                          col = 'grey', alpha = 0.05, lines = 0, p_pos = None):
    '''
    Plots two violin plots from two numpy arrays.
    IN:
      *values1*, *values2* - float
        values 1 and values 2
      *p_val* - float
        p value from statistical test comapring two groups
      *name1* = 'A', *name2* = 'B' - str, int
        names to display on x axis
      *y_lim* - list of 2 elements, tuple
        limits of y axis
      *y_label*, *x_label* - str
        y,x label
      *col* = 'grey' - str
        barplto colour
      *alpha* - float
        significance level (only if *p_val* provided)
      *lines* - bool
        flag to plot lines from underlying points
    OUT:
      plot from matplotlib
    '''
    if y_lim:
        min_lim = y_lim[0]
        max_lim = y_lim[-1]
    else:
        min_lim = 0
        max_lim = np.max([np.max(values1), np.max(values2)])
    dat = pd.DataFrame({'values' : np.concatenate((np.array(values1), np.array(values2))),
                 'x' : [name1]*len(values1) + [name2]*len(values2)})
    if lines == 1:
        for i in range(len(values1)):
            plt.plot([0, 1], [values1[i], values2[i]], 'o-', color = 'k', alpha = 0.4)
    elif lines == 2:
        sns.stripplot(x = 'x', y = 'values', data = dat, jitter=True, color = 'k', marker='o', alpha=0.4)
    sns.violinplot(x = 'x', y = 'values', data = dat, scale = 'count', color = col, cut = 0, width=0.4)
    if y_lim:
        plt.ylim(y_lim)
    if x_label:
        plt.xlabel(x_label)
    if y_label:
        plt.ylabel(y_label)
    if p_val:
        if p_pos is None:
            plt.axhline(y=0.95*max_lim, xmin=.25, xmax=.75, color = 'k')
            plt.text(0.5, 0.97*max_lim, '{}'.format('*' if p_val < alpha else 'ns'))
        else:
            plt.axhline(y= p_pos - 0.02, xmin=.25, xmax=.75, color = 'k')
            plt.text(0.5, p_pos, '{}'.format('*' if p_val < alpha else 'ns'))            

def plot_two_boxplots(values1, values2, p_val = None,
                   name1 = 'A', name2 = 'B',
                   y_lim = None, y_label = None, x_label = None, col = 'grey', alpha = 0.05):
    '''
    Plots two box-plots from two numpy arrays.
    IN:
      *values1*, *values2* - float
        values 1 and values 2
      *p_val* - float
        p value from statistical test comapring two groups
      *name1* = 'A', *name2* = 'B' - str, int
        names to display on x axis
      *y_lim* - list of 2 elements, tuple
        limits of y axis
      *y_label*, *x_label* - str
        y,x label
      *col* = 'grey' - str
        barplto colour
      *alpha* - float
        significance level (only if *p_val* provided)
    OUT:
      plot from matplotlib
    '''
    if y_lim:
        min_lim = y_lim[0]
        max_lim = y_lim[-1]
    else:
        min_lim = 0
        max_lim = np.max([np.max(values1), np.max(values2)])
    dat = pd.DataFrame({'values' : np.concatenate((np.array(values1), np.array(values2))),
                 'x' : [name1]*len(values1) + [name2]*len(values2)})
    sns.boxplot(x = 'x', y = 'values', data = dat, color = col, width = 0.65)
    if y_lim:
        plt.ylim(y_lim)
    if x_label:
        plt.xlabel(x_label)
    if y_label:
        plt.ylabel(y_label)
    if p_val:
        plt.axhline(y=0.91*max_lim, xmin=.25, xmax=.75, color = 'k')
        plt.text(0.48, 0.93*max_lim, '{}'.format('*' if p_val < alpha else 'ns'))
        
def plot_paired_barplots(group1_vals, group2_vals, p_val = None,
                           name1 = 'A', name2 = 'B',
                           y_lim = None, y_label = None, x_label = None,
                           bar_col = 'red', shift = 0.2, alpha = 0.05, p_pos = None):
    '''
    Plots two barplots from two means and standard errors.
    IN:
      *group1_vals*, *group2_vals* - list
        values from the first and second groups (need to have the same length)
      *p_val* - float
        p value from statistical test comapring two groups
      *name1* = 'A', *name2* = 'B' - str, int
        names to display on x axis
      *y_lim* - list of 2 elements, tuple
        limits of y axis
      *y_label*, *x_label* - str
        y,x label
      *shift* - float
        shift between bars
      *bar_col* - str
        colour of the bars
      *alpha* - float
        significance level (only if *p_val* provided)
      *p_pos* - float
        position of p value marker
    OUT:
      plot from matplotlib
    '''
    assert len(group1_vals) == len(group2_vals), "length of groups is not the same"
    if y_lim:
        max_lim = y_lim[-1]
    else:
        max_lim = np.max([np.max(group1_vals), np.max(group2_vals)])
    avg1 = np.mean(group1_vals)
    avg2 = np.mean(group2_vals)
    for i in range(len(group1_vals)):
        plt.plot([0, 1], [group1_vals[i], group2_vals[i]], 'o-', color = 'grey', alpha = 0.7)
    plt.bar([0, 1], [avg1, avg2], color = bar_col, alpha = 0.7, width = 0.65, zorder=9999)
    plt.xticks([0, 1], [name1, name2])
    plt.xlim([-0.5, 1.5])
    if y_lim:
        plt.ylim(y_lim)
    if x_label:
        plt.xlabel(x_label)
    if y_label:
        plt.ylabel(y_label)
    if p_val:
        if p_pos is None:
            plt.axhline(y=0.91*max_lim, xmin=.25, xmax=.75, color = 'k')
            plt.text(0.48, 0.93*max_lim, '{}'.format('*' if p_val < alpha else 'ns'))
        else:
            plt.axhline(y=p_pos - 0.02, xmin=.25, xmax=.75, color = 'k')
            plt.text(0.48, p_pos, '{}'.format('*' if p_val < alpha else 'ns'))

