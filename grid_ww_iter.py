import time
import numpy as np 
import matplotlib.pyplot as plt 
from scipy import integrate
import warnings
from hyperopt import fmin, tpe, hp
import sys

a           = 270.
b           = 108.
d           = 0.154
gamma       = 0.641 / 1000
tau_s       = 100. #ms
tau_noise   = 2.   #ms
Jll = Jrr   = 0.2601 # 0.1561
Jlr = Jrl   = 0.0497 # 0.0264
J_ext       = 0.00052 # 0.2243e-3
I_o         = 0.321
sigma_noise = 1*I_o / 16.275
mu_o        = 35
threshold   = 16

t_steps = 1600 # ms

xtime = np.linspace(0., t_steps,  int(1*t_steps))

r = lambda I_i: (a*I_i - b)/(1 - np.exp(-d*(a*I_i - b)))

def euler(func, x0, t):
    dt = t[1] - t[0]
    x = np.zeros((len(t), len(x0)))
    x[0] = x0
    for i in range(1, len(t)):
        x[i] = x[i-1] + dt * func(x[i-1], t[i]) 
    return x

def euler_fast(func, x0, t, threshold):
    dt = t[1] - t[0]
    x = np.zeros((len(t), len(x0)))
    x[0] = x0
    for i in range(1, len(t)):
        x[i] = x[i-1] + dt * func(x[i-1], t[i])
        sal,sar,_,_ = x[i]
        svecs = rescale_to_frequency(np.array([sal, sar]))
        if np.any(svecs > threshold):
            break
    return x

def rescale_to_frequency(svec):
    return svec *1./ ((1 - svec)*gamma * tau_s)

def calculate_input_A_mu(coherence, mu = mu_o):
    I_mot_l = J_ext * mu * (1 + coherence *1. / 100)
    I_mot_r = J_ext * mu * (1 - coherence *1. / 100)
    return I_mot_l, I_mot_r

def calculate_input_B_cong(coherence, mu = mu_o):
    I_mot_l = J_ext * mu * (1 + coherence *1. / 100)
    I_mot_r = J_ext * mu * (1 - coherence *1. / 100)
    return I_mot_l, I_mot_r

def calculate_input_B_incon(coherence, mu = mu_o):
    I_mot_l = J_ext * mu * (1 - coherence *1. / 100)
    I_mot_r = J_ext * mu * (1 + coherence *1. / 100)
    return I_mot_l, I_mot_r

def model(x, t):
    global I_o, cA, cB
    sl, sr, I_n1, I_n2 = x

    I_mot_l_A, I_mot_r_A = calculate_input_A(cA)
    I_mot_l_B, I_mot_r_B = calculate_input_B(cB)

    I_l = Jll * sl - Jlr*sr + I_mot_l_A + I_mot_l_B + I_o + I_n1
    I_r = Jrr * sr - Jrl*sl + I_mot_r_A + I_mot_r_B + I_o + I_n2
    ds1 = -sl*1./ tau_s + (1 - sl) * gamma * r(I_l)
    ds2 = -sr*1./ tau_s + (1 - sr) * gamma * r(I_r)
    eta = np.random.normal()
    dI_n1 = (- I_n1 + eta * np.sqrt(tau_noise) * sigma_noise) / tau_noise
    eta = np.random.normal()
    dI_n2 = (- I_n2 + eta * np.sqrt(tau_noise) * sigma_noise) / tau_noise
    return np.array([ds1, ds2, dI_n1, dI_n2])

def run_single_sim1d(threshold, timeit = False):
    acc = 0
    rt = -1
    x0 = np.array([np.random.uniform()*0.08,
                   np.random.uniform()*0.08,
                   I_o + np.random.normal()*0.05,
                   I_o + np.random.normal()*0.05])

    if timeit: t0 = time.time()
    X = euler_fast(model, x0, xtime, threshold)
    if timeit: print(time.time() - t0)
    S_l, S_r , _, _ = X.T
    S_l = rescale_to_frequency(S_l)
    S_r = rescale_to_frequency(S_r)
    l_idcs = np.where(S_l > threshold)[0]
    r_idcs = np.where(S_r > threshold)[0]
    if len(l_idcs) > 0:
        acc = 1
        rt = xtime[l_idcs[0]]
    if rt == -1:
        rt  = np.nan
        warnings.warn("Not enough RT values (1d)")
    return acc, rt

def run_many_sim1d(Nrep, threshold):
    '''
    Run multiple repetitions of *run_single_sim1d* function
    and return average and std of results for ACCs and RTs.
    '''
    accvec = np.zeros((Nrep, 1))
    rtvec = np.zeros((Nrep, 1))
    for i in range(Nrep):
        acc_, rt_ = run_single_sim1d(threshold)
        accvec[i] = acc_
        rtvec[i] = rt_
    return np.mean(accvec), np.nanmean(rtvec), np.std(accvec), np.nanstd(rtvec)

def run_for_params(mu_ratio, i0_ratio, silent = True):
    '''
    Run four experimental conditions for mu_ratio and i0_ratio.
    '''
    global I_o, calculate_input_A, calculate_input_B, cA, cB

    mu_B = mu_o / (mu_ratio + 1)
    mu_A = mu_ratio * mu_B
    I_o_1, I_o_2 = I_o, I_o*i0_ratio

    if not silent: print('>> incon')
    I_o = I_o_1
    calculate_input_B = lambda x: calculate_input_B_incon(x, mu_B)
    calculate_input_A = lambda x: calculate_input_A_mu(x, mu_A)
    cA, cB = 15, 0
    if not silent: print('sim 1d')
    acc1d_i, rt1d_i = run_single_sim1d(threshold)
    if not silent: print('end 1d')
    I_o = I_o_2
    calculate_input_B = lambda x: calculate_input_B_incon(x, mu_B)
    calculate_input_A = lambda x: calculate_input_A_mu(x, mu_A)
    cA, cB = 20, 5
    if not silent: print('sim 2d')
    acc2d_i, rt2d_i = run_single_sim1d(threshold)
    if not silent: print('end 2d')

    if not silent: print('>> con')
    I_o = I_o_1
    calculate_input_B = lambda x: calculate_input_B_cong(x, mu_B)
    calculate_input_A = lambda x: calculate_input_A_mu(x, mu_A)
    cA, cB = 20, 0
    if not silent: print('sim 1d')
    acc1d_c, rt1d_c = run_single_sim1d(threshold)
    if not silent: print('end 1d')
    I_o = I_o_1
    calculate_input_B = lambda x: calculate_input_B_cong(x, mu_B)
    calculate_input_A = lambda x: calculate_input_A_mu(x, mu_A)
    cA, cB = 15, 5
    if not silent: print('sim 2d')
    acc2d_c, rt2d_c = run_single_sim1d(threshold)
    if not silent: print('end 2d')

    return acc1d_i, acc2d_i, acc1d_c, acc2d_c, rt1d_i, rt2d_i, rt1d_c, rt2d_c

def iter_over_params(mu_range, i0_range):
    '''
    Iterate over parameters mu_ratio from mu_range and i0_ratio from i0_range.
    '''
    Nsample = len(mu_range)
    muv, i0v = np.meshgrid(mu_range, i0_range)
    accs_i1, accs_i2 = np.zeros((Nsample, Nsample)), np.zeros((Nsample, Nsample))
    accs_c1, accs_c2 = np.zeros((Nsample, Nsample)), np.zeros((Nsample, Nsample))
    rts_i1, rts_i2 = np.zeros((Nsample, Nsample)), np.zeros((Nsample, Nsample))
    rts_c1, rts_c2 = np.zeros((Nsample, Nsample)), np.zeros((Nsample, Nsample))

    for i in range(Nsample):
        for j in range(Nsample):
            vals_ = run_for_params(muv[i, j], i0v[i, j])
            acc1d_i, acc2d_i, acc1d_c, acc2d_c, rt1d_i, rt2d_i, rt1d_c, rt2d_c = vals_
            accs_i1[i, j] = acc1d_i
            accs_i2[i, j] = acc2d_i
            accs_c1[i, j] = acc1d_c
            accs_c2[i, j] = acc2d_c
            rts_i1[i, j] = rt1d_i
            rts_i2[i, j] = rt2d_i
            rts_c1[i, j] = rt1d_c
            rts_c2[i, j] = rt2d_c
    return accs_i1, accs_i2, accs_c1, accs_c2, rts_i1, rts_i2, rts_c1, rts_c2

if __name__ == "__main__":
    if len(sys.argv) == 2:
        OUT_FOLDER = sys.argv[1]
    else:
        OUT_FOLDER = 'gridvals' # default output folder 

    Nsample = 100
    mu_range = np.logspace(-1, 1, Nsample)
    i0_range = np.linspace(0.98, 1.02, Nsample)

    accs_i1, accs_i2, accs_c1, accs_c2, rts_i1, rts_i2, rts_c1, rts_c2 = iter_over_params(mu_range, i0_range)
    
    f_out =  "{}_{}".format(str(round(time.time())), str(round(np.random.random()*100)))

    np.savez('{}/{}.npz'.format(OUT_FOLDER, f_out),
             accs_i1 = accs_i1, accs_i2=accs_i2, accs_c1=accs_c1,
             accs_c2 = accs_c2, rts_i1=rts_i1, rts_i2=rts_i2,
             rts_c1= rts_c1, rts_c2=rts_c2)
