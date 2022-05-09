from random import random
import numpy as np
from scipy.stats import bootstrap
import os
import random

seed = 300_000
rng = np.random.default_rng(seed)


class ScipyBootstrap:
    def __init__(self) -> None:
        self.mean = None

    def calculate_mean(self, sample, axis=0):
        self.mean = np.mean(sample, axis=axis)
        # print('self.mean:', self.mean)
        # print('len(mean):', len(self.mean))
        return self.mean

    def execute(self, sample, resample_size, method):
        sample = (sample,)  # samples must be in a sequence
        res = bootstrap(sample, self.calculate_mean, confidence_level=0.95, method=method, 
            random_state=rng, n_resamples=resample_size)
        # print('method:', method, ', mean:' , self.mean)
        if method == 'basic':
            return self.mean, res
        return np.mean(self.mean), res
        

def my_bootstrap(x, num_resamples, iteration):
    # confidence level: 0.95
    random.seed(seed)
    x = np.array(x)
    resample_means = []
    pctl_2_5 = []
    pctl_97_5 = []
    for i in range(iteration):
        y = random.choices(x.tolist(), k=num_resamples)
        resample_means.append(np.mean(y))
        pctl_2_5.append(np.percentile(y, 2.5))
        pctl_97_5.append(np.percentile(y, 97.5))
    return np.mean(resample_means), np.mean(pctl_2_5), np.mean(pctl_97_5)

def my_bootstrap2(x, num_resamples, iteration):
    # inspired by https://allendowney.github.io/ElementsOfDataScience/12_bootstrap.html
    # confidence level: 0.95
    random.seed(seed)
    x = np.array(x)
    resample_means = []
    for i in range(iteration):
        y = random.choices(x.tolist(), k=num_resamples)
        resample_means.append(np.mean(y))
    ci = np.percentile(resample_means, [2.5, 97.5])
    return np.mean(resample_means), ci

def my_mean(data, axis=0):
    mean = np.mean(data, axis=axis)
    return mean

def scipy_bootstrap(sample):
    resample_size = 10000
    m = None
    def inner_mean(data, axis=0):
        m = np.mean(data, axis=axis)
        return m
    res = bootstrap(sample, my_mean, confidence_level=0.95, method='percentile', 
            random_state=rng, n_resamples=resample_size)
    # ci = res.confidence_interval
    # lower_error = m - ci.low
    # upper_error = ci.high = m
    return m, res

if __name__ == '__main__':
    os.system('cls' if os.name == 'nt' else 'clear')
    sample_ac_001_200K_defensive = [0.33485841006239003, 0.21226203699857799, 0.3248557954618527, 0.2659631076330068, 0.42039470604574736, 0.28715685650746015, 0.19695643705457427, 0.33538180288874714, 0.23743488056530565, 0.35075769712147]
    sample_ac_001_200K_neutral = [0.18532895566884122, 0.2604845866164399, 0.19353037608236096, 0.16365756861449576, 0.27915018593650864, 0.16810275835243826, 0.1968941667203078, 0.20947801140981598, 0.22344925888354694, 0.18704771587187413]
    sample_ac_001_200K_offensive = [0.459400557809027, 0.4592314383266912, 0.43629164412004007, 0.405906185668918, 0.43426501928792755, 0.3746436206719713, 0.4435103599790182, 0.4433257775740126, 0.440837983937531, 0.4093241812212999]
    sample_ac_001_200K_head_on = [0.026668727450197882, 0.03958254683019785, 0.04478790330012139, 0.01837042822244922, 0.04144759479905363, 0.027994892669779115, 0.02641771824487965, 0.02725429584117567, 0.11945002525094278, 0.1073073386597293]
    # choose one sample
    sample = sample_ac_001_200K_defensive

    num_resamples = 5
    iterations = [100, 1000, 10000]

    print(f'original sample mean={np.mean(sample):.4f}')
    print("My bootstrap\n===========================")
    for resample_size in iterations:
        mean, ci_low, ci_high = my_bootstrap(sample, num_resamples, resample_size)
        print(f'Resample size={resample_size:n}, mean={mean:.4f}')
        print(f'ConfidenceInterval(low={ci_low:.4f}, high={ci_high:.4f})\n')

    print("My bootstrap2 (num_resamples:5)\n===========================")
    for resample_size in iterations:
        mean, ci = my_bootstrap2(sample, num_resamples, resample_size)
        print(f'Resample size={resample_size:n}, mean={mean:.4f}')
        print(f'ConfidenceInterval(low={ci[0]:.4f}, high={ci[1]:.4f})\n')
        print('ci:', ci)

    print("\n\nMy bootstrap2 (num_resamples:10)\n===========================")
    num_resamples = len(sample)
    print('num_resamples:', num_resamples)
    for resample_size in iterations:
        mean, ci = my_bootstrap2(sample, num_resamples, resample_size)
        print(f'Resample size={resample_size:n}, mean={mean:.4f}')
        print(f'ConfidenceInterval(low={ci[0]:.4f}, high={ci[1]:.4f})\n')

    print("\n\n\nScipy bootstrap (bca)\n=====================")
    rng = np.random.default_rng(seed)
    for resample_size in iterations:
        b = ScipyBootstrap()
        mean, res = b.execute(sample, resample_size, 'bca')
        ci = res.confidence_interval
        print(f'Resample size={resample_size:n}, mean={mean:.4f}')
        print(f'ConfidenceInterval(low={ci.low:.4f}, high={ci.high:.4f})\n')

    print("\n\n\nScipy bootstrap (basic)\n=====================")
    rng = np.random.default_rng(seed)
    for resample_size in iterations:
        b = ScipyBootstrap()
        mean, res = b.execute(sample, resample_size, 'basic')
        ci = res.confidence_interval
        print(f'Resample size={resample_size:n}, mean={mean:.4f}')
        print(f'ConfidenceInterval(low={ci.low:.4f}, high={ci.high:.4f})\n')

    print("\n\n\nScipy bootstrap (percentile)\n=====================")
    rng = np.random.default_rng(seed)
    for resample_size in iterations:
        b = ScipyBootstrap()
        mean, res = b.execute(sample, resample_size, 'percentile')
        ci = res.confidence_interval
        print(f'Resample size={resample_size:n}, mean={mean:.4f}')
        print(f'ConfidenceInterval(low={ci.low:.4f}, high={ci.high:.4f})\n')

"""
original sample mean=0.2966
My bootstrap
===========================
Resample size=100, mean=0.2994
ConfidenceInterval(low=0.2332, high=0.3637)

Resample size=1000, mean=0.2985
ConfidenceInterval(low=0.2288, high=0.3671)

Resample size=10000, mean=0.2970
ConfidenceInterval(low=0.2262, high=0.3677)

My bootstrap2 (num_resamples:5)
===========================
Resample size=100, mean=0.2994
ConfidenceInterval(low=0.2369, high=0.3481)

ci: [0.23689445 0.34805381]
Resample size=1000, mean=0.2985
ConfidenceInterval(low=0.2415, high=0.3575)

ci: [0.24148513 0.35753209]
Resample size=10000, mean=0.2970
ConfidenceInterval(low=0.2411, high=0.3565)

ci: [0.24112481 0.3564732 ]


My bootstrap2 (num_resamples:10)
===========================
num_resamples: 10
Resample size=100, mean=0.3016
ConfidenceInterval(low=0.2528, high=0.3391)

Resample size=1000, mean=0.2967
ConfidenceInterval(low=0.2580, high=0.3382)

Resample size=10000, mean=0.2969
ConfidenceInterval(low=0.2570, high=0.3378)




Scipy bootstrap (bca)
=====================
Resample size=100, mean=0.2966
ConfidenceInterval(low=0.2625, high=0.3375)

Resample size=1000, mean=0.2966
ConfidenceInterval(low=0.2554, high=0.3363)

Resample size=10000, mean=0.2966
ConfidenceInterval(low=0.2564, high=0.3388)




Scipy bootstrap (basic)
=====================
Resample size=100, mean=0.2966
ConfidenceInterval(low=0.2593, high=0.3330)

Resample size=1000, mean=0.2966
ConfidenceInterval(low=0.2570, high=0.3384)

Resample size=10000, mean=0.2966
ConfidenceInterval(low=0.2550, high=0.3376)




Scipy bootstrap (percentile)
=====================
Resample size=100, mean=0.2955
ConfidenceInterval(low=0.2602, high=0.3339)

Resample size=1000, mean=0.2966
ConfidenceInterval(low=0.2548, high=0.3362)

Resample size=10000, mean=0.2965
ConfidenceInterval(low=0.2556, high=0.3382)
"""