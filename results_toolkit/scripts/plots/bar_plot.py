from .graph_label import GraphLabel

def plot_stacked_bar(values,graphlabel=GraphLabel(),legend=None,filesave=None,selected=False):

    import matplotlib.pyplot as plt
    import numpy as np
    #plt.figure(figsize=(3,4))
    pass_test = values['passes']
    crash_test = values['collisions']

    
 
    width = 0.3 
    ind = np.arange(len(pass_test))
    fig = plt.subplots(figsize=(5,6))
    p1 = plt.bar(ind, pass_test, width, color = '#00ff00', edgecolor='black')
    p2 = plt.bar(ind, crash_test, width,
                bottom = pass_test,  color = '#ff0000', edgecolor='black')
    # plt.subplots_adjust(left=1, right=1.1, top=1.1, bottom=1)

    plt.ylabel(graphlabel.ylabel)
    plt.xlabel(graphlabel.xlabel) 
    plt.title(graphlabel.title)
    plt.xticks(ind, (graphlabel.xlabels),rotation=90)
    plt.yticks(np.arange(0, values['upper_limit']+1, 1))
    plt.legend((p1[0], p2[0]), legend,bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.0)
    plt.tight_layout();
    if filesave==None:
        plt.show()
    else:
        plt.savefig(filesave,dpi=400)

    plt.close()

# if __name__ == "__main__":
#     # create_box_plot(data, save_path, graphlabel=GraphLabel())
    
#     values = {'passes': [1, 2, 3, 4, 5,6], 'collisions': [1, 2, 3, 4, 5,6], 'upper_limit':11}
#     graphlabel = GraphLabel(title='title',xlabel='xlabel',ylabel='ylabel',legend='legend',xlabels=['S','F1','F2','F3','F4'])
#     plot_stacked_bar(values,graphlabel=graphlabel,legend=('pass', 'pass_test'))



def plot_bar(values,graphlabel=GraphLabel(),legend=None,filesave=None,selected=False):

    import matplotlib.pyplot as plt
    import numpy as np
    fig, ax = plt.subplots(figsize=(5,4))
    width = 0.3 
    ax.bar(graphlabel.xlabels, values["values"], color = '#006400', width=width, edgecolor='black')
    for i, v in enumerate(values["values"]):
        ax.text(i, v + 0.2, str(v), ha='center')
    plt.title(graphlabel.title)
    plt.xlabel(graphlabel.xlabel)
    plt.ylabel(graphlabel.ylabel)
    plt.yticks(np.arange(0, values["upper_limit"], 5))
    plt.tight_layout();
    if filesave==None:
        plt.show()
    else:
        plt.savefig(filesave,dpi=400)

# if __name__ == "__main__":
#     values = {"values":[12.4, 13.5, 14.6, 15.7, 16.8], "upper_limit":40}
#     graphlabel = GraphLabel(title='title',xlabel='xlabel',ylabel='ylabel',legend='legend',xlabels=['S','F1','F2','F3','F4'])
#     plot_bar(values,graphlabel=graphlabel,legend=('pass', 'pass_test'))
