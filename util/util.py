import json
from pathlib import Path
from collections import OrderedDict
from itertools import repeat
import pandas as pd
import os
import numpy as np
from glob import glob
import math

def load_folds_data_shhs(np_data_path, n_folds):
    files = sorted(glob(os.path.join(np_data_path, "*.npz")))
    r_p_path = r"utils/r_permute_shhs.npy"
    r_permute = np.load(r_p_path)
    npzfiles = np.asarray(files , dtype='<U200')[r_permute]
    train_files = np.array_split(npzfiles, n_folds)
    folds_data = {}
    for fold_id in range(n_folds):
        subject_files = train_files[fold_id]
        training_files = list(set(npzfiles) - set(subject_files))
        folds_data[fold_id] = [training_files, subject_files]
    return folds_data

def load_folds_data(config,np_data_path, n_folds):
    '''
    将一个包含多个.npz文件的文件夹按照指定的折数（n_folds）分成多个 fold，每个 fold 包含一组训练文件和一组测试文件。
    :param np_data_path:   包含多个.npz文件的文件夹的路径
    :param n_folds:       指定的折数
    :return:     folds_data: 一个字典，其中键是 fold 的编号，值是一个包含两个列表的列表，第一个列表是训练文件，第二个列表是测试文件
    '''
    files = sorted(glob(os.path.join(np_data_path, "*.npz")))

    # npy文件能够保存NumPy数组的结构、数据类型以及数据内容
    if "78" in np_data_path:
        r_p_path = r"utils/r_permute_78.npy"
    #     如果配置文件name以learn开头则 只训练俩个被试者
    elif "Learn" in config["name"] :
        r_p_path = r"utils/r_learn_permute_20.npy"
    else:
        r_p_path = r"utils/r_permute_20.npy"

    if os.path.exists(r_p_path):
        # r_permute: 保存了文件顺序的数组:[14  5  4 17  8  7 19 12  0 15 16  9 11 10  3  1  6 18  2 13]
        r_permute = np.load(r_p_path)
    else:
        print ("============== ERROR =================")

    # 统计*npz文件信息
    # dict结构: {人员编号: [文件1,文件2]}
    files_dict = dict()
    for i in files:
        file_name = os.path.split(i)[-1] 
        # 截取受试人员编号 （例如：'01'）
        file_num = file_name[3:5]
        if file_num not in files_dict:
            files_dict[file_num] = [i]
        else:
            files_dict[file_num].append(i)
    files_pairs = []
    for key in files_dict:
        files_pairs.append(files_dict[key])
    #  缺失编号13的人员一条记录 导致报错 需要添加dtype=object
    files_pairs = np.array(files_pairs, dtype=object)
    # files_pairs = np.array(files_pairs)
    files_pairs = files_pairs[r_permute]

    train_files = np.array_split(files_pairs, n_folds)
    folds_data = {}
    for fold_id in range(n_folds):
        subject_files = train_files[fold_id]
        subject_files = [item for sublist in subject_files for item in sublist]
        files_pairs2 = [item for sublist in files_pairs for item in sublist]
        training_files = list(set(files_pairs2) - set(subject_files))
        folds_data[fold_id] = [training_files, subject_files]
    return folds_data


def calc_class_weight(labels_count):
    total = np.sum(labels_count)
    class_weight = dict()
    num_classes = len(labels_count)

    factor = 1 / num_classes
    mu = [factor * 1.5, factor * 2, factor * 1.5, factor, factor * 1.5] # THESE CONFIGS ARE FOR SLEEP-EDF-20 ONLY

    for key in range(num_classes):
        score = math.log(mu[key] * total / float(labels_count[key]))
        class_weight[key] = score if score > 1.0 else 1.0
        class_weight[key] = round(class_weight[key] * mu[key], 2)

    class_weight = [class_weight[i] for i in range(num_classes)]

    return class_weight


def ensure_dir(dirname):
    dirname = Path(dirname)
    if not dirname.is_dir():
        dirname.mkdir(parents=True, exist_ok=False)


def read_json(fname):
    fname = Path(fname)
    with fname.open('rt') as handle:
        return json.load(handle, object_hook=OrderedDict)


def write_json(content, fname):
    fname = Path(fname)
    with fname.open('wt') as handle:
        json.dump(content, handle, indent=4, sort_keys=False)


def inf_loop(data_loader):
    ''' wrapper function for endless data loader. '''
    for loader in repeat(data_loader):
        yield from loader


class MetricTracker:
    def __init__(self, *keys, writer=None):
        self.writer = writer
        self._data = pd.DataFrame(index=keys, columns=['total', 'counts', 'average'])
        self.reset()

    def reset(self):
        for col in self._data.columns:
            self._data[col].values[:] = 0

    def update(self, key, value, n=1):
        if self.writer is not None:
            self.writer.add_scalar(key, value)
        self._data.total[key] += value * n
        self._data.counts[key] += n
        self._data.average[key] = self._data.total[key] / self._data.counts[key]

    def avg(self, key):
        return self._data.average[key]

    def result(self):
        return dict(self._data.average)

#
if __name__ == '__main__':
    '''
        学习模式下数据集顺序:只选择前俩个数据集
    '''
    r_learn_permute_20 =[1,0]
    np.save(r"r_learn_permute_20",r_learn_permute_20)