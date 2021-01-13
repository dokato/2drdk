import os
import numpy as np 
import matplotlib.pyplot as plt 

# parameters of sampled space
Nsample = 100
mu_range = np.logspace(-1, 1, Nsample)
i0_range = np.linspace(0.98, 1.02, Nsample)

# loading the saved data
path_to_grid_values = 'gridvalsf/'

def average_std_grid(grid):
    """
    Computes average and STD from gridvalues.
    INPUT:
      grid (numpy.array)
        array of size (repetitions, N samples, N samples)
    OUTPUT:
      two arrays with average and STD among repetitions.
    """
    return np.nanmean(grid, axis=0), np.nanstd(grid, axis=0)

def load_grid_values(path = path_to_grid_values):
    '''
    Load data from path. It expects that folder contains only npz files
    with the following fields: accs_i1, accs_i2, accs_c1, accs_c2,
    rts_i1, rts_i2, rts_c1, rts_c2.
    INPUT:
      path (str)
        path to folder with npz files
    OUTPUT:
      eight matrices with data for ACCs and RTs.
    '''
    accs_i1_vec = []
    accs_i2_vec = []
    accs_c1_vec = []
    accs_c2_vec = []
    rts_i1_vec = []
    rts_i2_vec = []
    rts_c1_vec = []
    rts_c2_vec = []
    for p in os.listdir(path):
        m = np.load(os.path.join(path, p))
        accs_i1_vec += [m['accs_i1']]
        accs_i2_vec += [m['accs_i2']]
        accs_c1_vec += [m['accs_c1']]
        accs_c2_vec += [m['accs_c2']]
        rts_i1_vec += [m['rts_i1']]
        rts_i2_vec += [m['rts_i2']]
        rts_c1_vec += [m['rts_c1']]
        rts_c2_vec += [m['rts_c2']]
    accs_i1_vec = np.array(accs_i1_vec)
    accs_i2_vec = np.array(accs_i2_vec)
    accs_c1_vec = np.array(accs_c1_vec)
    accs_c2_vec = np.array(accs_c2_vec)
    rts_i1_vec = np.array(rts_i1_vec)
    rts_i2_vec = np.array(rts_i2_vec)
    rts_c1_vec = np.array(rts_c1_vec)
    rts_c2_vec = np.array(rts_c2_vec)
    return accs_i1_vec, accs_i2_vec, accs_c1_vec, accs_c2_vec,\
            rts_i1_vec, rts_i2_vec, rts_c1_vec, rts_c2_vec,

def load_and_avg_grid(path = path_to_grid_values):
    '''
    Loads data from path and compute average over repetitions.
    It expects that folder contains only npz files
    with the following fields: accs_i1, accs_i2, accs_c1, accs_c2,
    rts_i1, rts_i2, rts_c1, rts_c2.
    INPUT:
      path (str)
        path to folder with npz files
    OUTPUT:
      two tuples each consisting of 8 matrices
       - first with matrices with averaged data for ACCs and RTs
       - second for STD.
       In order of experimental conditions: ACC i1, i2, c1, c2,
       RT i1, i2, c1, c2
    '''
    vals = load_grid_values(path)
    avg_vals = []
    std_vals = []
    for v in vals:
        a_, s_ = average_std_grid(v)
        avg_vals.append(a_)
        std_vals.append(s_)
    return avg_vals, std_vals

avgs, stds = load_and_avg_grid()

grid_acc_i1, grid_acc_i2 = avgs[0], avgs[1]
grid_acc_c1, grid_acc_c2 = avgs[2], avgs[3]

grid_rt_i1, grid_rt_i2 = avgs[4], avgs[5]
grid_rt_c1, grid_rt_c2 = avgs[6], avgs[7]

std_acc_i1, std_acc_i2 = stds[0], stds[1]
std_acc_c1, std_acc_c2 = stds[2], stds[3]

std_rt_i1, std_rt_i2 = stds[4], stds[5]
std_rt_c1, std_rt_c2 = stds[6], stds[7]

del avgs, stds

plot_grids = False
if plot_grids == True:
    plt.subplot(221)
    plt.imshow(grid_acc_c1, interpolation='none', aspect='equal')
    plt.colorbar()
    plt.title('C1')
    plt.subplot(222)
    plt.imshow(grid_acc_c2, interpolation='none', aspect='equal')
    plt.colorbar()
    plt.title('C2')
    plt.subplot(223)
    plt.imshow(grid_acc_i1, interpolation='none', aspect='equal')
    plt.colorbar()
    plt.title('I1')
    plt.subplot(224)
    plt.imshow(grid_acc_i2, interpolation='none', aspect='equal')
    plt.colorbar()
    plt.title('I2')
    plt.suptitle('ACC')
    plt.figure()
    plt.subplot(221)
    plt.imshow(grid_rt_c1, interpolation='none', aspect='equal')
    plt.colorbar()
    plt.title('C1')
    plt.subplot(222)
    plt.imshow(grid_rt_c2, interpolation='none', aspect='equal')
    plt.colorbar()
    plt.title('C2')
    plt.subplot(223)
    plt.imshow(grid_rt_i1, interpolation='none', aspect='equal')
    plt.colorbar()
    plt.title('I1')
    plt.subplot(224)
    plt.imshow(grid_rt_i2, interpolation='none', aspect='equal')
    plt.colorbar()
    plt.title('I2')
    plt.suptitle('RT')
    plt.show()

# Standard deviations difference between 0

std_acc_i = np.sqrt((std_acc_i1**2 + std_acc_i2**2) / 2)
std_acc_c = np.sqrt((std_acc_c1**2 + std_acc_c2**2) / 2)
std_rt_i = np.sqrt((std_rt_i1**2 + std_rt_i2**2) / 2)
std_rt_c = np.sqrt((std_rt_c1**2 + std_rt_c2**2) / 2)

# Behavioural condtions
cond_i_acc = np.where(grid_acc_i1 > grid_acc_i2)
cond_i_acc = [(x,y) for x, y in zip(cond_i_acc[0], cond_i_acc[1])]
cond_c_acc = np.where(grid_acc_c1 > grid_acc_c2)
cond_c_acc = [(x,y) for x, y in zip(cond_c_acc[0], cond_c_acc[1])]

cond_i_rt = np.where(grid_rt_i1 > grid_rt_i2)
cond_i_rt = [(x,y) for x, y in zip(cond_i_rt[0], cond_i_rt[1])]
cond_c_rt = np.where(grid_rt_c2 > grid_rt_c1)
cond_c_rt = [(x,y) for x, y in zip(cond_c_rt[0], cond_c_rt[1])]

all_cond_ids = set(cond_i_acc) & set(cond_c_acc) & set(cond_i_rt) & set(cond_c_rt)

print(all_cond_ids)

cond_mask = np.zeros((Nsample, Nsample))

for p in all_cond_ids:
    cond_mask[p[0], p[1]] = 1

alpha_level = 0.4
colmap = 'seismic'

fig, axes = plt.subplots(2, 2)
#im = axes[0, 0].imshow(100*(grid_acc_c1 - grid_acc_c2), interpolation='none', aspect='equal')
im = axes[0, 0].imshow(100*(grid_acc_c1 - grid_acc_c2), vmin = -20, vmax = 20, cmap = colmap, interpolation='none', aspect='equal')
axes[0, 0].imshow(cond_mask, cmap = 'Greys',  interpolation = 'nearest', alpha = alpha_level)
axes[0, 0].set_title('Congruent')
#cbar = plt.colorbar(im, ax = axes[0, 0])
#cbar.ax.set_ylabel('ACC(1ax) - ACC(2ax) [%]', verticalalignment='baseline', rotation=270)
axes[1, 0].set_ylabel(r'$I_0$ ratio')

#im = axes[0, 1].imshow(100*(grid_acc_i1 - grid_acc_i2), interpolation='none', aspect='equal')
im = axes[0, 1].imshow(100*(grid_acc_i1 - grid_acc_i2), vmin = -20, vmax = 20, cmap = colmap, interpolation='none', aspect='equal')
axes[0, 1].imshow(cond_mask, cmap = 'Greys',  interpolation = 'nearest', alpha = alpha_level)
axes[0, 1].set_title('Incongruent')
cbar = plt.colorbar(im, ax = axes[0, 1])
cbar.ax.set_ylabel('ACC(single) - ACC(double) [%]', verticalalignment='baseline', rotation=270)

#im = axes[1, 0].imshow(grid_rt_c1 - grid_rt_c2, interpolation='none', aspect='equal')
im = axes[1, 0].imshow(grid_rt_c1 - grid_rt_c2, vmin = -200, vmax = 200, cmap = colmap, interpolation='none', aspect='equal')
axes[1, 0].imshow(cond_mask, cmap = 'Greys',  interpolation = 'nearest', alpha = alpha_level)
#cbar = plt.colorbar(im, ax = axes[1, 0])
#cbar.ax.set_ylabel('RT(1ax) - RT(2ax) [ms]', verticalalignment='baseline', rotation=270)
axes[1, 0].set_xlabel(r'$\mu$ ratio')
axes[1, 0].set_ylabel(r'$I_0$ ratio')

#im = axes[1, 1].imshow(grid_rt_i1 - grid_rt_i2, interpolation='none', aspect='equal')
im = axes[1, 1].imshow(grid_rt_i1 - grid_rt_i2, vmin = -200, vmax = 200, cmap = colmap, interpolation='none', aspect='equal')
axes[1, 1].imshow(cond_mask, cmap = 'Greys',  interpolation = 'nearest', alpha = alpha_level)
cbar = plt.colorbar(im, ax = axes[1, 1])
cbar.ax.set_ylabel('RT(single) - RT(double) [ms]', verticalalignment='baseline', rotation=270)

everyNth = 20
mu_line =  np.argmin(np.abs(mu_range - 1))
i0_line =  np.argmin(np.abs(i0_range - 1))
for er, r in enumerate(axes):
    for ec, ax in enumerate(r):
        if er > 0:
          #ticks_pos = range(0, len(mu_range), everyNth)
          ticks_pos = [0, mu_line, len(mu_range)-1]
          ticks_lab = ['{:.1f}'.format(mu_range[i]) for i in ticks_pos]
          ticks_lab[1] = '1.0'
          ax.set_xticks(ticks_pos)
          ax.set_xticklabels(ticks_lab)
        else:
          ax.set_xticks([])
        if ec == 0:
          #ticks_pos = range(0, len(i0_range), everyNth)
          ticks_pos = [0, i0_line, len(i0_range)-1]
          ticks_lab = ['{:.2f}'.format(i0_range[i]) for i in ticks_pos]
          ax.set_yticks(ticks_pos)
          ax.set_yticklabels(ticks_lab)
        else:
          ax.set_yticks([])
        ax.axvline(x = mu_line, linewidth=1, color='k', alpha = 0.5)
        ax.axhline(y = i0_line, linewidth=1, color='k', alpha = 0.5)

plt.tight_layout()
#plt.show()
plt.savefig('grid_f.svg')
#plt.close()

