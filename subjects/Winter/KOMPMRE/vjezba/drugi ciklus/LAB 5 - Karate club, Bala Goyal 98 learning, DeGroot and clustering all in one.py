#!/usr/bin/env python
# coding: utf-8

# # LAB 5 - Karate club, Bala Goyal 98 learning, DeGroot and clustering all in one

# In[1]:


import networkx as nx
import random
import numpy as np

random.seed(123)

p_val = 0.55

### Bala Goyal 98 LEARNIING - repeated action, observe one another
#----------------------------------------------------------------------


# In[2]:


# Create an empty graph
G = nx.Graph()

# Add 20 nodes to the graph
for i in range(1, 21):
    G.add_node(i)

# Add random edges to the graph
for i in range(1, 21):
    for j in range(i+1, 21):
        if random.random() < 0.5:
            G.add_edge(i, j)
            
import matplotlib.pyplot as plt
nx.draw(G, with_labels = True)
plt.show()


# In[3]:


# Add random state "A" or "B" to each node
for node in G.nodes():
    if random.random() < 0.5:
        G.nodes[node]["state"] = "A"
        G.nodes[node]["value"] = 1
    else:
        G.nodes[node]["state"] = "B"
        G.nodes[node]["value"] = 2 if random.random() < p_val else 0


# In[4]:


#printing the node state and value
for node in G.nodes():
    print(f'{node},{G.nodes[node]["state"]},{G.nodes[node]["value"]}')


# In[5]:


# Create a dictionary to map each state to a color
state_colors = {"A": "blue", "B": "red"}

# Draw the graph, coloring each node by its state
pos = nx.spring_layout(G)
nx.draw(G, pos, node_color=[state_colors[G.nodes[node]["state"]] for node in G.nodes()], with_labels = True)
plt.show()


# In[6]:


# Create a dictionary to map each value to a color
value_colors = {1: "blue", 2: "green",0:"red"}

# Draw the graph, coloring each node by its value
pos = nx.spring_layout(G)
nx.draw(G, pos, node_color=[value_colors[G.nodes[node]["value"]] for node in G.nodes()], with_labels = True)
plt.show()


# In[7]:


#20 iterations for loop
for i in range(20):
    new_states = {}
    new_values = {}
    for node in G.nodes():
        # calculate average value of state A
        A_neighbors = [G.nodes[neighbor]["value"] for neighbor in G.neighbors(node) if G.nodes[neighbor]["state"] == "A"]
        if len(A_neighbors) == 0:
            A_average = 0
        else:
            A_average = sum(A_neighbors) / len(A_neighbors)

        # calculate average value of state B
        B_neighbors = [G.nodes[neighbor]["value"] for neighbor in G.neighbors(node) if G.nodes[neighbor]["state"] == "B"]
        if len(B_neighbors) == 0:
            B_average = 0
        else:
            B_average = sum(B_neighbors) / len(B_neighbors)

        # change state of node to the one of higher average value
        if A_average > B_average:
            new_states[node] = "A"
            new_values[node] = 1
        elif B_average > A_average:
            new_states[node] = "B"
            new_values[node] = 2 if random.random() < p_val else 0
    for node in new_states:
        G.nodes[node]["state"] = new_states[node]
        G.nodes[node]["value"] = new_values[node]


# In[8]:


#printing the node state and value
for node in G.nodes():
    print(f'{node},{G.nodes[node]["state"]},{G.nodes[node]["value"]}')
#-------------------------------------------------------- 


# In[9]:


# Create a dictionary to map each state to a color
state_colors = {"A": "blue", "B": "red"}

# Draw the graph, coloring each node by its state
pos = nx.spring_layout(G)
nx.draw(G, pos, node_color=[state_colors[G.nodes[node]["state"]] for node in G.nodes()], with_labels = True)
plt.show()


# In[10]:


# Create a dictionary to map each value to a color
value_colors = {1: "blue", 2: "green",0:"red"}

# Draw the graph, coloring each node by its value
pos = nx.spring_layout(G)
nx.draw(G, pos, node_color=[value_colors[G.nodes[node]["value"]] for node in G.nodes()], with_labels = True)
plt.show()


# In[11]:


##### what is the issue - random network
G = nx.karate_club_graph()
random.seed(12345)

# Add random state "A" or "B" to each node
for node in G.nodes():
    if random.random() < 0.75:
        G.nodes[node]["state"] = "A"
        G.nodes[node]["value"] = 1
    else:
        G.nodes[node]["state"] = "B"
        G.nodes[node]["value"] = 2 if random.random() < p_val else 0
        


# In[12]:


import matplotlib.pyplot as plt
nx.draw(G, with_labels = True)
plt.show()


# In[13]:


# Create a dictionary to map each state to a color
state_colors = {"A": "blue", "B": "red"}

# Draw the graph, coloring each node by its state
pos = nx.spring_layout(G)
nx.draw(G, pos, node_color=[state_colors[G.nodes[node]["state"]] for node in G.nodes()], with_labels = True)
plt.show()


# In[14]:


# Create a dictionary to map each value to a color
value_colors = {1: "blue", 2: "green",0:"red"}

# Draw the graph, coloring each node by its value
nx.draw(G, pos, node_color=[value_colors[G.nodes[node]["value"]] for node in G.nodes()], with_labels = True)
plt.show()


# In[15]:


average_values = []


# In[16]:


new_states = {}
new_values = {}
for node in G.nodes():
    # calculate average value of state A
    A_neighbors = [G.nodes[neighbor]["value"] for neighbor in G.neighbors(node) if G.nodes[neighbor]["state"] == "A"]
    if len(A_neighbors) == 0:
        A_average = 0
    else:
        A_average = sum(A_neighbors) / len(A_neighbors)

    # calculate average value of state B
    B_neighbors = [G.nodes[neighbor]["value"] for neighbor in G.neighbors(node) if G.nodes[neighbor]["state"] == "B"]
    if len(B_neighbors) == 0:
        B_average = 0
    else:
        B_average = sum(B_neighbors) / len(B_neighbors)

    # change state of node to the one of higher average value
    if A_average > B_average:
        new_states[node] = "A"
        new_values[node] = 1
    elif B_average > A_average:
        new_states[node] = "B"
        new_values[node] = 2 if random.random() < 0.5 else 0
for node in new_states:
    G.nodes[node]["state"] = new_states[node]
    G.nodes[node]["value"] = new_values[node]
average_values.append(sum([G.nodes[node]["value"] for node in G.nodes()])/len(G.nodes()))
    
    # Create a dictionary to map each state to a color
state_colors = {"A": "blue", "B": "red"}

# Draw the graph, coloring each node by its state
nx.draw(G, pos, node_color=[state_colors[G.nodes[node]["state"]] for node in G.nodes()], with_labels = True)
plt.show()


# In[17]:


new_states = {}
new_values = {}
for node in G.nodes():
    # calculate average value of state A
    A_neighbors = [G.nodes[neighbor]["value"] for neighbor in G.neighbors(node) if G.nodes[neighbor]["state"] == "A"]
    if len(A_neighbors) == 0:
        A_average = 0
    else:
        A_average = sum(A_neighbors) / len(A_neighbors)

    # calculate average value of state B
    B_neighbors = [G.nodes[neighbor]["value"] for neighbor in G.neighbors(node) if G.nodes[neighbor]["state"] == "B"]
    if len(B_neighbors) == 0:
        B_average = 0
    else:
        B_average = sum(B_neighbors) / len(B_neighbors)

    # change state of node to the one of higher average value
    if A_average > B_average:
        new_states[node] = "A"
        new_values[node] = 1
    elif B_average > A_average:
        new_states[node] = "B"
        new_values[node] = 2 if random.random() < 0.5 else 0
for node in new_states:
    G.nodes[node]["state"] = new_states[node]
    G.nodes[node]["value"] = new_values[node]
average_values.append(sum([G.nodes[node]["value"] for node in G.nodes()])/len(G.nodes()))
    
    # Create a dictionary to map each state to a color
state_colors = {"A": "blue", "B": "red"}

# Draw the graph, coloring each node by its state
nx.draw(G, pos, node_color=[state_colors[G.nodes[node]["state"]] for node in G.nodes()], with_labels = True)
plt.show()


# In[18]:


new_states = {}
new_values = {}
for node in G.nodes():
    # calculate average value of state A
    A_neighbors = [G.nodes[neighbor]["value"] for neighbor in G.neighbors(node) if G.nodes[neighbor]["state"] == "A"]
    if len(A_neighbors) == 0:
        A_average = 0
    else:
        A_average = sum(A_neighbors) / len(A_neighbors)

    # calculate average value of state B
    B_neighbors = [G.nodes[neighbor]["value"] for neighbor in G.neighbors(node) if G.nodes[neighbor]["state"] == "B"]
    if len(B_neighbors) == 0:
        B_average = 0
    else:
        B_average = sum(B_neighbors) / len(B_neighbors)

    # change state of node to the one of higher average value
    if A_average > B_average:
        new_states[node] = "A"
        new_values[node] = 1
    elif B_average > A_average:
        new_states[node] = "B"
        new_values[node] = 2 if random.random() < 0.5 else 0
for node in new_states:
    G.nodes[node]["state"] = new_states[node]
    G.nodes[node]["value"] = new_values[node]
average_values.append(sum([G.nodes[node]["value"] for node in G.nodes()])/len(G.nodes()))

# Create a dictionary to map each state to a color
state_colors = {"A": "blue", "B": "red"}

# Draw the graph, coloring each node by its state
nx.draw(G, pos, node_color=[state_colors[G.nodes[node]["state"]] for node in G.nodes()], with_labels = True)
plt.show()


# In[19]:


new_states = {}
new_values = {}
for node in G.nodes():
    # calculate average value of state A
    A_neighbors = [G.nodes[neighbor]["value"] for neighbor in G.neighbors(node) if G.nodes[neighbor]["state"] == "A"]
    if len(A_neighbors) == 0:
        A_average = 0
    else:
        A_average = sum(A_neighbors) / len(A_neighbors)

    # calculate average value of state B
    B_neighbors = [G.nodes[neighbor]["value"] for neighbor in G.neighbors(node) if G.nodes[neighbor]["state"] == "B"]
    if len(B_neighbors) == 0:
        B_average = 0
    else:
        B_average = sum(B_neighbors) / len(B_neighbors)

    # change state of node to the one of higher average value
    if A_average > B_average:
        new_states[node] = "A"
        new_values[node] = 1
    elif B_average > A_average:
        new_states[node] = "B"
        new_values[node] = 2 if random.random() < 0.5 else 0
for node in new_states:
    G.nodes[node]["state"] = new_states[node]
    G.nodes[node]["value"] = new_values[node]
average_values.append(sum([G.nodes[node]["value"] for node in G.nodes()])/len(G.nodes()))
    
    # Create a dictionary to map each state to a color
state_colors = {"A": "blue", "B": "red"}

# Draw the graph, coloring each node by its state
nx.draw(G, pos, node_color=[state_colors[G.nodes[node]["state"]] for node in G.nodes()], with_labels = True)
plt.show()


# In[20]:


new_states = {}
new_values = {}
for node in G.nodes():
    # calculate average value of state A
    A_neighbors = [G.nodes[neighbor]["value"] for neighbor in G.neighbors(node) if G.nodes[neighbor]["state"] == "A"]
    if len(A_neighbors) == 0:
        A_average = 0
    else:
        A_average = sum(A_neighbors) / len(A_neighbors)

    # calculate average value of state B
    B_neighbors = [G.nodes[neighbor]["value"] for neighbor in G.neighbors(node) if G.nodes[neighbor]["state"] == "B"]
    if len(B_neighbors) == 0:
        B_average = 0
    else:
        B_average = sum(B_neighbors) / len(B_neighbors)

    # change state of node to the one of higher average value
    if A_average > B_average:
        new_states[node] = "A"
        new_values[node] = 1
    elif B_average > A_average:
        new_states[node] = "B"
        new_values[node] = 2 if random.random() < 0.5 else 0
for node in new_states:
    G.nodes[node]["state"] = new_states[node]
    G.nodes[node]["value"] = new_values[node]
average_values.append(sum([G.nodes[node]["value"] for node in G.nodes()])/len(G.nodes()))
    
    # Create a dictionary to map each state to a color
state_colors = {"A": "blue", "B": "red"}

# Draw the graph, coloring each node by its state
nx.draw(G, pos, node_color=[state_colors[G.nodes[node]["state"]] for node in G.nodes()], with_labels = True)
plt.show()


# In[21]:


new_states = {}
new_values = {}
for node in G.nodes():
    # calculate average value of state A
    A_neighbors = [G.nodes[neighbor]["value"] for neighbor in G.neighbors(node) if G.nodes[neighbor]["state"] == "A"]
    if len(A_neighbors) == 0:
        A_average = 0
    else:
        A_average = sum(A_neighbors) / len(A_neighbors)

    # calculate average value of state B
    B_neighbors = [G.nodes[neighbor]["value"] for neighbor in G.neighbors(node) if G.nodes[neighbor]["state"] == "B"]
    if len(B_neighbors) == 0:
        B_average = 0
    else:
        B_average = sum(B_neighbors) / len(B_neighbors)

    # change state of node to the one of higher average value
    if A_average > B_average:
        new_states[node] = "A"
        new_values[node] = 1
    elif B_average > A_average:
        new_states[node] = "B"
        new_values[node] = 2 if random.random() < 0.5 else 0
for node in new_states:
    G.nodes[node]["state"] = new_states[node]
    G.nodes[node]["value"] = new_values[node]
average_values.append(sum([G.nodes[node]["value"] for node in G.nodes()])/len(G.nodes()))
    
    # Create a dictionary to map each state to a color
state_colors = {"A": "blue", "B": "red"}

# Draw the graph, coloring each node by its state
nx.draw(G, pos, node_color=[state_colors[G.nodes[node]["state"]] for node in G.nodes()], with_labels = True)
plt.show()


# In[22]:


from sklearn.cluster import AgglomerativeClustering


# In[ ]:


A = nx.floyd_warshall_numpy(G) # distance mx - istance[i, j] is the distance along a shortest path from i to j


# In[ ]:


A


# In[ ]:


# Create an AgglomerativeClustering object
agg_clustering = AgglomerativeClustering(n_clusters=2, affinity = "precomputed",  linkage = 'complete')

# Fit the model to the data
agg_clustering.fit(A)

# Retrieve the labels for each node
cluster_labels = agg_clustering.labels_


# In[ ]:


# Define colors for the nodes
colors = ["gray" if cluster_labels[i] == 0 else "red" for i in range(len(cluster_labels))]

# Plot the graph with the colors
nx.draw(G, pos, node_color=colors, with_labels=True)
plt.show()


# In[ ]:


# Retrieve the labels for each node
# Get the original community labels
original_labels = nx.get_node_attributes(G,'club')

# Plot the graph with the colors
nx.draw(G, pos, node_color=colors, with_labels=False)

# Add the original labels to the graph
nx.draw_networkx_labels(G, pos, original_labels)
plt.show()


# In[ ]:


propagating_state = nx.get_node_attributes(G,'state')
nx.draw(G, pos, node_color=colors, with_labels=False)
nx.draw_networkx_labels(G, pos, propagating_state)
plt.show()


# In[ ]:


#### DeGroot learning

import networkx as nx
import numpy as np

# Import the Karate Club graph
G = nx.karate_club_graph()

np.random.seed(123)
# Initialize the opinion vector with random values - probability of event X occuring
# Get the club labels of each node
club_labels = nx.get_node_attributes(G, "club")


# In[ ]:


club_labels


# In[ ]:


# Create a dictionary to map each node to its club label
node_club = {}
for node, label in club_labels.items():
    node_club[node] = label


# In[ ]:


# Initialize the opinion vector with random values
opinions = np.random.rand(G.number_of_nodes())

# Make the opinions 50% less for one group
for i in range(G.number_of_nodes()):
    if node_club[i] == 'Officer':
        opinions[i] = opinions[i]*0.5


# In[ ]:


opinions


# In[ ]:


# Draw the graph
pos = nx.spring_layout(G)
# Plot the graph with the colors
nx.draw(G, pos, node_color=colors, with_labels=False)
# Add the opinions to each node
for i in range(G.number_of_nodes()):
    plt.annotate(round(opinions[i], 2), xy=pos[i], fontsize=8)

plt.show()


# In[ ]:


# Initialize the dictionary to store the average opinion for each group
avg_opinions = {'Mr. Hi': 0, 'Officer': 0}
count = {'Mr. Hi': 0, 'Officer': 0}

# Calculate the average opinion for each group
for i in range(G.number_of_nodes()):
    group = node_club[i]
    avg_opinions[group] += opinions[i]
    count[group] +=1


# In[ ]:


# Divide the total opinion by the number of nodes in each group
for group in avg_opinions.keys():
    avg_opinions[group] = avg_opinions[group]/count[group]

# Print the average opinion for each group
print(avg_opinions)


# In[ ]:


# Set the number of iterations
num_iters = 20

# Set the constant alpha also known as Tii - how much we are stubborn (confirmed by experiments)
alpha = 0.7

# Simulate the DeGroot model - talking to neigbours gettinng average of their opinion 
# and then update my belif in the event X
# note the unweighted graph vs full weights as in example - so this is different
for i in range(num_iters):
    new_opinions = np.zeros(G.number_of_nodes())
    for j in range(G.number_of_nodes()):
        neighbors = list(G.neighbors(j))
        neighbors_opinions = opinions[neighbors]
        new_opinions[j] = alpha * opinions[j] + (1 - alpha) * np.mean(neighbors_opinions)
    opinions = new_opinions

# Print the final opinions
print(opinions)
###----------------------


# In[ ]:


# Get the club labels of each node
club_labels = nx.get_node_attributes(G, "club")

# Create a list of colors for each club label
colors = ["gray" if club_labels[i] == 'Officer' else "red" for i in range(len(club_labels))]

# Draw the graph
pos = nx.spring_layout(G)
# Plot the graph with the colors
nx.draw(G, pos, node_color=colors, with_labels=False)
# Add the opinions to each node
for i in range(G.number_of_nodes()):
    plt.annotate(round(opinions[i], 2), xy=pos[i], fontsize=8)

plt.show()


# In[ ]:


# Initialize the dictionary to store the average opinion for each group
avg_opinions = {'Mr. Hi': 0, 'Officer': 0}
count = {'Mr. Hi': 0, 'Officer': 0}


# In[ ]:


# Calculate the average opinion for each group
for i in range(G.number_of_nodes()):
    group = node_club[i]
    avg_opinions[group] += opinions[i]
    count[group] +=1

# Divide the total opinion by the number of nodes in each group
for group in avg_opinions.keys():
    avg_opinions[group] = avg_opinions[group]/count[group]

# Print the average opinion for each group
print(avg_opinions)


# In[ ]:


# Set the number of iterations
num_iters = 100

# Set the constant alpha also known as Tii - how much we are stubborn (confirmed by experiments)
alpha = 0.7

# Simulate the DeGroot model - talking to neigbours gettinng average of their opinion 
# and then update my belif in the event X
# note the unweighted graph vs full weights as in example - so this is different
for i in range(num_iters):
    new_opinions = np.zeros(G.number_of_nodes())
    for j in range(G.number_of_nodes()):
        neighbors = list(G.neighbors(j))
        neighbors_opinions = opinions[neighbors]
        new_opinions[j] = alpha * opinions[j] + (1 - alpha) * np.mean(neighbors_opinions)
    opinions = new_opinions

# Print the final opinions
print(opinions)
###----------------------


# In[ ]:


# Initialize the dictionary to store the average opinion for each group
avg_opinions = {'Mr. Hi': 0, 'Officer': 0}
count = {'Mr. Hi': 0, 'Officer': 0}


# In[ ]:


# Calculate the average opinion for each group
for i in range(G.number_of_nodes()):
    group = node_club[i]
    avg_opinions[group] += opinions[i]
    count[group] +=1

# Divide the total opinion by the number of nodes in each group
for group in avg_opinions.keys():
    avg_opinions[group] = avg_opinions[group]/count[group]

# Print the average opinion for each group
print(avg_opinions)


# In[ ]:


# the society is wise precisely when even the most influential individual's influence vanishes in the large society limit
# if the society grows without bound, over time they will have a common and accurate belief on the uncertain subject

# 


# 
