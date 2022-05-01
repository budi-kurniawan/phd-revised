import os
import pickle
import matplotlib.pyplot as plt

# Plots the average of Q values in a test result folder
def draw_plots(path, folder_name, prefix):
    image_path = path + '/' + prefix + '-' + folder_name + '.png'
#     if os.path.exists(image_path):
#         print image_path + ' exists. Skipped'
#         return
    
    q_filenames = [f for f in os.listdir(path) if f.startswith('Q-')]
    q_tables = []
    for q_filename in q_filenames:
        q = pickle.load(open(os.path.join(path, q_filename)))
        q_tables.append(q['q'])

    q_avg = {}
    num_tables = len(q_tables)
    for zone in range(0, 131):
        for speed in range(0, 5):
            for action in range(0, 2):
                key = str(zone) + '-' + str(speed) + '-' + str(action)
                if key not in q_avg:
                    q_avg[key] = 0.0
                for q_table in q_tables:
                    value = q_table[key] if key in q_table else 0.0
                    q_avg[key] = q_avg[key] + value / num_tables   
    
    x = list(range(0, 131))

    # create a figure with 5 plots
    for speed in range(0, 5):
        plot_data0 = []
        plot_data1 = []
        for zone in range(0, 131):
            key = str(zone) + '-' + str(speed) + '-0'
            plot_data0.append(q_avg[key])
            key = str(zone) + '-' + str(speed) + '-1'
            plot_data1.append(q_avg[key])
        plt.subplot(511 + speed)
        plt.plot(x, plot_data0, 'r-', x, plot_data1, 'b-')
        plt.ylabel('Q (' + str(speed) + ')')
        plt.xlabel('Zone')
        if speed == 0:
            plt.title(path)
    plt.savefig(image_path)
    plt.gcf().clear()
    #plt.show()
    

if __name__ == '__main__':
    scenario = "eligibility_traces7"
    path = '../rl_results/' + scenario + '.json'
    folders = [f for f in os.listdir(path) if os.path.isdir(os.path.join(path, f))]
    for folder in folders:
        draw_plots(os.path.join(path, folder), folder, scenario)
