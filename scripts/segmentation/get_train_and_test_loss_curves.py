import matplotlib.pyplot as plt
import numpy as np

# path_folder = '/Users/manu/boulot/unit_solutions/training/cellpose/v1/'
#
# loss_train = np.load(path_folder + 'losses_train.npy')
# loss_test = np.load(path_folder + 'losses_test.npy')
#
# fig, ax = plt.subplots(1,1)
# ax.plot(loss_train, label='train')
# ax.plot(loss_test, label='test')
# ax.legend()
# ax.set_xlabel('epochs')
# ax.set_ylabel('loss')
# ax.grid()
#
# fig.savefig(path_folder+'loss_curves_plot.png')

path_folders = [
    '/Users/manu/boulot/unit_solutions/training/cellpose/v1/round1/',
    '/Users/manu/boulot/unit_solutions/training/cellpose/v1/round2/',
    '/Users/manu/boulot/unit_solutions/training/cellpose/v1/round3/',
    '/Users/manu/boulot/unit_solutions/training/cellpose/v1/round4/',
    '/Users/manu/boulot/unit_solutions/training/cellpose/v1/round5/',
]

loss_train_list = []
loss_test_list = []
for path_folder in path_folders:
    loss_train = np.load(path_folder + 'losses_train.npy')
    loss_test = np.load(path_folder + 'losses_test.npy')

    loss_train_list += list(loss_train)
    loss_test_list += list(loss_test)


fig, ax = plt.subplots(1,1)
ax.plot(loss_train_list, label='train')
ax.plot(loss_test_list, label='test')
ax.legend()
ax.set_xlabel('epochs')
ax.set_ylabel('loss')
ax.grid()

fig.savefig(path_folder+'loss_curves_plot.png')