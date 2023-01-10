
from .graph_label import GraphLabel


# function to draw positions
def plot_box_combined(values,graphlabel=GraphLabel(),filesave=None,selected=False,violations=False):
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches
    plt.figure(figsize=(5,6))
    values2 = []
    for ds in values:
        ds2 = []
        for d in ds:
            if d<10:
                ds2.append(d)
        values2.append(ds2)
    if selected:
        bplot = plt.boxplot(values2,patch_artist=True)
        if len(graphlabel.xlabels)>0:
            plt.xticks([i+1 for i in range(len(values2))], graphlabel.xlabels)
    else:
        bplot = plt.boxplot(values,patch_artist=True)
        if len(graphlabel.xlabels)>0:
            plt.xticks([i+1 for i in range(len(values))], graphlabel.xlabels,rotation=90)
    for c,patch in enumerate(bplot['boxes']):
        if c==0:
            patch.set_facecolor((0,0,0,1))
        else:
            try:
                if(violations[c-1]):
                    patch.set_facecolor((1,0,0,1))
                else:
                    patch.set_facecolor((0,1,0,1))
            except:
                patch.set_facecolor((0,1,0,1))
        #r,g,b = colors[scenarios[c]]
        #patch.set_facecolor((r,g,b,1))
    plt.grid(axis='both',linestyle='--')
    if selected:
        plt.ylim([0,5])
    plt.xlabel(graphlabel.xlabel)
    plt.ylabel(graphlabel.ylabel)
    # red_patch = mpatches.Patch(color='#ff0000', label='MR violation')
    # plt.legend(handles=[red_patch],bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.0)
    plt.tight_layout();
    if filesave==None:
        plt.show()
    else:
        plt.savefig(filesave,dpi=400)
    
    plt.close()

SET = '6'


def create_box_plot(data, save_path, graphlabel=GraphLabel(), violations=False):
    plot_box_combined(data,graphlabel,filesave=save_path, violations=violations)


