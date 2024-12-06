import threading
import time
import settings
import random

# Parameters to be defined by the user
waiting_time_before_resending_request = 10000  # Time the client will wait before resending the request. This time, it broadcasts the request to all nodes
timer_limit_before_view_change = 50000 # There is no value proposed in the paper so let's fix it to 200s
checkpoint_frequency = 100 # 100 is the proposed value in the original article

n = settings.n
f = (n-1)//3
h = n - f 

nfp = random.randint(0,0) # nfp: number of faulty primaries
nsn = random.randint(0,h) # nsn: number of slow nodes
nnrn = random.randint(0,(f-nfp)//2) # nnrn: number of non responding nodes
nfn = random.randint(0,(f-nfp-nnrn)//2) # nfn: number of faulty nodes
nfrn = random.randint(0,(f-nfp-nnrn-nfn)//2) # nfrn: number of faulty replies nodes
nda = random.randint(0,(f-nfp-nnrn-nfn-nfrn)//2) # nda: number of dos attackers
nbn = random.randint(0,f-nfp-nnrn-nfn-nfrn-nda) # nbn: number of byzantine nodes
nhn = n-(nfp+nsn+nnrn+nfn+nfrn+nda+nbn) # nhn: number of honest nodes (All the rest nodes are honest nodes)

#nfp = 0 # nfp: number of faulty primaries
#nsn = 68 # nsn: number of slow nodes
#nnrn = 16 # nnrn: number of non responding nodes
#nfn = 11 # nfn: number of faulty nodes
#nfrn = 11 # nfrn: number of faulty replies nodes
#nda = 16 # nda: number of dos attackers
#nbn = 11 # nbn: number of byzantine nodes
#nhn = 67 # nhn: number of honest nodes


# Define the nodes we want in our network + their starting time + their type
nodes={} # This is a dictionary of nodes we want in our network. Keys are the nodes types, and values are a list of tuples of starting time and number of nodes 
#nodes[starting time] = [(type of nodes , number of nodes)]
#nodes[0]=[("faulty_primary",nfp),("honest_node",nhn),("slow_nodes",nsn),("non_responding_node",nnrn),("faulty_node",nfn),("faulty_replies_node",nfrn),("dos_attacker",nda),("byzantine_node",nbn)] # Nodes starting from the beginning
nodes[0]=[("faulty_primary",nfp),("honest_node",nhn),("slow_nodes",nsn),("non_responding_node",nnrn),("faulty_node",nfn),("faulty_replies_node",nfrn),("dos_attacker",nda),("byzantine_node",nbn)] # Nodes starting from the beginning
#nodes[0]=[("faulty_primary",0),("honest_node",7),("slow_nodes",9),("non_responding_node",1),("faulty_node",1),("faulty_replies_node",1),("dos_attacker",1),("byzantine_node",0)] # Nodes starting from the beginning
#nodes[2]=[("faulty_primary",0),("slow_nodes",0),("honest_node",3),("non_responding_node",0),("faulty_node",0),("faulty_replies_node",0),("message_size_change_node",0),("dos_attacker",0),("byzantine_node",1)] # Nodes starting from the beginning

############## CAUTION: number of nodes have to be filled in settings.py ##############""

#print("f=",f)
#print("h=",h)
#print("number of faulty primaries:",nfp)
#print("number of slow nodes:",nsn)
#print("number of honest nodes:",nhn)
#print("number of non responding nodes:",nnrn)
#print("number of faulty nodes:",nfn)
#print("number of faulty replies nodes:",nfrn)
#print("number of dos attackers:",nda)
#print("number of byzantine nodes:",nbn)

from client import *
from PBFT import *

# Running PBFT protocol
run_PBFT(nodes=nodes,proportion=1,checkpoint_frequency0=checkpoint_frequency,clients_ports0=clients_ports,timer_limit_before_view_change0=timer_limit_before_view_change)

time.sleep(1) # Waiting for the network to start...

primary_id = get_primary_id()

settings.node_is_primary[primary_id] += 1

# Run clients:
#settings.requests_number = 1 # The user chooses the number of requests he wants to execute simultaneously (They are all sent to the PBFT network at the same time) - Here each request will be sent by a different client
clients_list = []

for i in range (settings.requests_number):
    globals()["C%s" % str(i)]=Client(i,waiting_time_before_resending_request)
    clients_list.append(globals()["C%s" % str(i)])
for i in range (settings.requests_number):
    threading.Thread(target=clients_list[i].send_to_primary,args=("I am the client "+str(i),get_primary_id(),get_nodes_ids_list(),get_f())).start()
    # Classifier les noeuds, choisir les plus performants...
    time.sleep(50)
    settings.add_data_to_csv()
    time.sleep(5)


    #settings.add_data_to_csv()
    #time.sleep(30) #Exécution plus rapide lorsqu'on attend un moment avant de lancer la requête suivante

#time.sleep(10)
# Afficher à la fin de la simulation: lorsque toutes les transactions ont été validées (if actual transaction == number of transactions)
#if (settings.number_of_validated_requests == settings.requests_number):
        
