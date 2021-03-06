import networkx as nx
import matplotlib.pyplot as plt
import csv
import pprint as pp
from math import log, e
import matplotlib as mpl 

# function to read from finalized_cewit_faculty.csv and make a dictionary from it.

def get_dep_fac_dict():
    with open('student_affiliates.csv') as f:
        csv_content = csv.DictReader(f)
        dep_fac_dict = {}
        names = []
        iu_dep_list = []
        for row in csv_content:
            fn = row['first_name'].strip().lower()
            ln = row['last_name'].strip().lower()
            dep_fac_dict.setdefault(row['School'].title(),[]).append((fn,ln))


    return dep_fac_dict

def get_gradien_color():
    with open('gradient_colors_students') as f:
        color_dict ={}
        colors = []
        for c in f.readlines():
            colors.append('#'+c.strip())
        colors.reverse()
        for i,j in [(7,0),(20,1),(47,2),(105,3),(115,4),(176,5),(274,6),(514,7)]:
            color_dict[i] = colors[j].strip()
    return color_dict, colors


dep_fac_dict = get_dep_fac_dict()
color_dict, C = get_gradien_color()

pp.pprint(color_dict)
print C



# pp.pprint(color_dict)

# because there are too many departments/nodes in the graph, so we only keep the top 25 departments


for d in dep_fac_dict.keys():
    if len(dep_fac_dict[d]) < 5:
        dep_fac_dict.pop(d)








G = nx.Graph()


edge_width_list = []
for d in dep_fac_dict.keys():
    # if len(dep_fac_dict[d]) <= 4:
    #     width = 4
    # else:
    #     width = len(dep_fac_dict[d])
    if len(dep_fac_dict[d]) < 10:
        width = len(dep_fac_dict[d]) * 6
    elif len(dep_fac_dict[d]) < 30:
        width = len(dep_fac_dict[d]) * 3
    elif len(dep_fac_dict[d]) < 50:
        width = len(dep_fac_dict[d]) * 2
    else:
       width = len(dep_fac_dict[d])
    edge_tuple = ('CEWIT', d)
    edge_width_list.append((edge_tuple,width))



for tuple, width in edge_width_list:
    G.add_edge(tuple[0], tuple[1], weight = width/5)   # the weight determines the width of links between departments and CEWIT






node_labels = {}
node_sizes = {}
node_colors = {}
scaler = 10
for d in dep_fac_dict.keys():
    node_labels[d] = d + '\n' + str(len(dep_fac_dict[d]))
    # node_sizes[d] = len(dep_fac_dict[d]) *100  # use log() to decrease the difference between huge node and small node
    if len(dep_fac_dict[d]) < 20:
        node_sizes[d] = len(dep_fac_dict[d]) *30 *scaler

    elif len(dep_fac_dict[d]) <= 50:
        node_sizes[d] = len(dep_fac_dict[d]) *10 *scaler
    elif len(dep_fac_dict[d]) < 280:
        node_sizes[d] = len(dep_fac_dict[d]) *5 *scaler
    else:
        node_sizes[d] = len(dep_fac_dict[d]) *3 *scaler
    # else:
    #     node_sizes[d] = (len(dep_fac_dict[d])-2) * scaler
    # node_colors[d] = '#E1D8B7'
    node_colors[d] = color_dict[len(dep_fac_dict[d])]

    # color_index.append(len(dep_fac_dict[d]))


node_labels['CEWIT'] = 'CEWIT'
node_sizes['CEWIT'] = 2500
node_colors['CEWIT'] = '#CD894E'


edges = G.edges()
weights = [G[u][v]['weight'] for u,v in edges]

plt.figure('Distribution of CEWIT student Members-no caption',figsize=(16,8)) 

cm = mpl.colors.ListedColormap(C)

pos = nx.spring_layout(G, k=.9, scale = 10)

nx.draw(G, pos, linewidths = 0.5,labels = node_labels, font_size = 14, edges = edges, width = 3, nodelist = node_sizes.keys(), node_size = node_sizes.values(), font_family = 'Century Gothic', node_color=node_colors.values(), edge_color='#9adcc6',with_labels=True)

sm = plt.cm.ScalarMappable(cmap=cm, norm=plt.normalize(vmin=7, vmax=514))
sm._A = []
plt.colorbar(sm, shrink = 0.7, pad = 0.15, orientation = 'vertical', anchor = (-2,0.5),fraction = 0.1)



plt.show() # display