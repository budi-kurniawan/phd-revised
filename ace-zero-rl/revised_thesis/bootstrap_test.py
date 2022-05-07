from random import random
import numpy as np
from scipy.stats import norm
from scipy.stats import bootstrap
import os
import random

def my_bootstrap(x, num_resamples, iteration, seed = 300000):
    # confidence level: 0.95
    random.seed(seed)
    x = np.array(x)
    resample_mean = []
    pctl_2_5 = []
    pctl_97_5 = []
    for i in range(iteration):
        y = random.choices(x.tolist(), k=num_resamples)
        resample_mean.append(np.mean(y))
        pctl_2_5.append(np.percentile(y, 2.5))
        pctl_97_5.append(np.percentile(y, 97.5))
    return np.mean(resample_mean), np.mean(pctl_2_5), np.mean(pctl_97_5)


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

    print(f'sample mean={np.mean(sample):.4f}')
    print("My bootstrap\n===========================")
    for resample_size in iterations:
        mean, ci_low, ci_high = my_bootstrap(sample, num_resamples, resample_size)
        print(f'Resample size={resample_size:n}, mean={mean:.4f}')
        print(f'ConfidenceInterval(low={ci_low:.4f}, high={ci_high:.4f})\n')


    print("\n\n\nScipy bootstrap with np.mean\n=====================")
    rng = np.random.default_rng()
    sample = (sample,)  # samples must be in a sequence
    for resample_size in iterations:
        print(f'Resample size={resample_size:n}')
        res = bootstrap(sample, np.mean, confidence_level=0.95, method='basic', random_state=rng, n_resamples=resample_size)
        ci = res.confidence_interval
        print(f'ConfidenceInterval(low={ci.low:.4f}, high={ci.high:.4f})\n')


    print("\n\n\nScipy bootstrap with np.std\n=====================")
    for resample_size in iterations:
        print(f'Resample size={resample_size:n}')
        res = bootstrap(sample, np.std, confidence_level=0.95, method='basic', random_state=rng, n_resamples=resample_size)
        ci = res.confidence_interval
        print(f'ConfidenceInterval(low={ci.low:.4f}, high={ci.high:.4f})\n')

    """ Result:
    sample mean=0.2966
    My bootstrap
    ===========================
    Resample size=100, mean=0.2994
    ConfidenceInterval(low=0.2332, high=0.3637)

    Resample size=1000, mean=0.2985
    ConfidenceInterval(low=0.2288, high=0.3671)

    Resample size=10000, mean=0.2970
    ConfidenceInterval(low=0.2262, high=0.3677)




    Scipy bootstrap with np.mean
    =====================
    Resample size=100
    ConfidenceInterval(low=0.2580, high=0.3402)

    Resample size=1000
    ConfidenceInterval(low=0.2543, high=0.3356)

    Resample size=10000
    ConfidenceInterval(low=0.2548, high=0.3366)




    Scipy bootstrap with np.std
    =====================
    Resample size=100
    ConfidenceInterval(low=0.0510, high=0.0946)

    Resample size=1000
    ConfidenceInterval(low=0.0476, high=0.0927)

    Resample size=10000
    ConfidenceInterval(low=0.0488, high=0.0937)
    """