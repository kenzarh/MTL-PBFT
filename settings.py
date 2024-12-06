# File defining global variables common between the other files 

import math
import random
import PBFT

global requests_number
requests_number = 3

global n # number of nodes in the network
#n = random.randint(4,1000) # To revise: should adapt to the number of launched nodes in the run_PBFT function
n=20
#print("n=",n)

global number_of_validated_requests
number_of_validated_requests = 0 
  
global number_of_messages_sent_per_node
number_of_messages_sent_per_node = [0 for i in range (n)]

global number_of_faulty_messages_sent_per_node
number_of_faulty_messages_sent_per_node = [0 for i in range (n)]

global mean_delay_to_validate_accepted_block_per_node
mean_delay_to_validate_accepted_block_per_node = [1e9 for i in range (n)]

global number_of_validated_blocks_per_node
number_of_validated_blocks_per_node = [0 for i in range (n)]

global rate_of_validated_blocks_per_node
rate_of_validated_blocks_per_node = [0 for i in range (n)]

global number_of_unavailabilities_per_node
number_of_unavailabilities_per_node = [0 for i in range (n)]

global rapidity_label
rapidity_label=[]

global availability_label
availability_label=[]

global honesty_label
honesty_label=[]

global fault_label
fault_label=[]

global mean_messages_size 
mean_messages_size = [0 for i in range (n)] 

global node_is_primary # A list initialized to 0 and saying if a node was primary during the simulation or not: 0 if it was never primary, 1 if it was once, 2 if twice, etc.
node_is_primary = [0 for i in range (n)]  # Initialized in the beginning of the simulation and changed with new-views

global changed_primary # A list saying if a node was primary then was changed: 0 if it was never the case, 1 if once, etc.
changed_primary = [0 for i in range (n)]  # Updated when the new primary broadcasts a new-view message



global nodes_data_without_labels1



def add_data_to_csv():

        global nodes_data_without_labels
        nodes_data_without_labels=[]

        data = [] # This list stores tha data we will append to the csv file

        data.append(number_of_messages_sent_per_node)
        #print("number_of_messages_sent_per_node: ",number_of_messages_sent_per_node)

        #data.append(settings.number_of_faulty_messages_sent_per_node)

        rate_of_faulty_messages_per_node=[(number_of_faulty_messages_sent_per_node[i]/number_of_messages_sent_per_node[i] if number_of_messages_sent_per_node[i]!=0 else 0) for i in range (n)]
        data.append(rate_of_faulty_messages_per_node)
        #print("rate_of_faulty_messages_per_node: ",rate_of_faulty_messages_per_node)

        data.append(mean_delay_to_validate_accepted_block_per_node)
        #print("mean_delay_to_validate_accepted_block_per_node: ",mean_delay_to_validate_accepted_block_per_node)

        #data.append(settings.number_of_validated_blocks_per_node)

        rate_of_validated_blocks_per_node = [(number_of_validated_blocks_per_node[i]/requests_number) for i in range (n)]
        #data.append(rate_of_validated_blocks_per_node)
        #print("rate_of_validated_blocks_per_node: ",rate_of_validated_blocks_per_node)

        data.append(number_of_unavailabilities_per_node)
        #print("number_of_unavailabilities_per_node: ",number_of_unavailabilities_per_node)

        data.append(mean_messages_size)
        #print("mean_messages_size: ",mean_messages_size)

        import statistics as s
        themean = s.mean(mean_messages_size)
        abs_mean_messages_size = [abs(x-themean) for x in mean_messages_size]
        data.append(abs_mean_messages_size)
        #print("deviation_mean_messages_size: ",mean_messages_size)

        data.append(changed_primary)
        #print("changed_primary: ",changed_primary)

        data.append(node_is_primary)
        #print("node_is_primary: ",node_is_primary)

        data.append([n for i in range (n)])

        #data.append([requests_number for i in range (n)])

        data.append(rapidity_label)
        #print("rapidity_label: ",rapidity_label)

        data.append(availability_label)
        #print("availability_label: ",availability_label)

        data.append(honesty_label)
        #print("honesty_label: ",honesty_label)

        data.append(fault_label)
        #print("fault_label: ",fault_label)

        global node_data1
        node_data1 = []

        labels = []

        #print("data: ",data)
        # Writing features and labels in csv file (one line per node):
        from csv import writer  
        with open('nodes_data.csv', 'a',newline='') as f_object:
            for i in range(n):
                node_data = []
                node_data_without_labels = []
                for j in range (len(data)):
                    node_data.append(data[j][i])
                #print(node_data[-4:])
                labels.append(node_data[-4:])
                node_data1.append(node_data)
                writer_object = writer(f_object)
                writer_object.writerow(node_data)   
            f_object.close()


        #print(node_data1)

        #print(labels)
     
        with open('nodes_data_without_labels.csv', 'a',newline='') as f_object:
            #nodes_data_without_labels = []
            for i in range(n):
                node_data_without_labels1 = []
                for j in range (len(data)-4):
                    node_data_without_labels1.append(data[j][i])
               
                nodes_data_without_labels.append(node_data_without_labels1)
                writer_object = writer(f_object)
                writer_object.writerow(node_data_without_labels1)   
            f_object.close()

        # Use trained model to predict nodes labels
        import pickle
        loaded_model = pickle.load(open('mtl-models/multioutputclassifier_classifierchain_extratrees.sav', 'rb'))
        import numpy
        from sklearn.preprocessing import StandardScaler
        sc = StandardScaler()
        nodes_data_without_labels = sc.fit_transform(nodes_data_without_labels)
        import time
        prediction_starting_time = time.time() 
        predictions = loaded_model.predict(nodes_data_without_labels)
        prediction_end_time = time.time() 

        print("The delay for prediction is:" , (prediction_end_time-prediction_starting_time))

        predicted_labels=[]
        for node in predictions:
            node_predicted_label=[]
            if node[0]==0:
                node_predicted_label.append("slow")
            if node[0]==1:
                node_predicted_label.append("rapid")
            if node[0]==2:
                node_predicted_label.append("byzantine")

            if node[1]==0:
                node_predicted_label.append("unavailable")
            if node[1]==1:
                node_predicted_label.append("available")
            if node[1]==2:
                node_predicted_label.append("byzantine")


            if node[2]==0:
                node_predicted_label.append("faulty")
            if node[2]==1:
                node_predicted_label.append("honest")
            if node[2]==2:
                node_predicted_label.append("byzantine")


            if node[3]==0:
                node_predicted_label.append("faulty-primary")
            if node[3]==1:
                node_predicted_label.append("honest")
            if node[3]==2:
                node_predicted_label.append("crash-fault")
            if node[3]==3:
                node_predicted_label.append("faulty-replies")
            if node[3]==4:
                node_predicted_label.append("byzantine")
            if node[3]==5:
                node_predicted_label.append("digest-change")
            if node[3]==6:
                node_predicted_label.append("dos-attacker")

            predicted_labels.append(node_predicted_label)

        PBFT.update_consensus_nodes(predicted_labels)
        classification_end_time = time.time() 
        print("The delay for updating consensus nodes is:" , (classification_end_time-prediction_starting_time))

        #for i in range (n):
            #print("features:",nodes_data_without_labels[i],"predicted labels:",predictions[i],"true labels:",node_data1[i][-4:])
        #print(predictions)

        # Calculating accuracy:
        a=0
        for i in range (len(predictions)):
            for j in range (len(predictions[0])):
                #print("pred.:",predicted_labels[i][j],"real:",labels[i][j])
                if (predicted_labels[i][j]==labels[i][j]):
                    a = a + 1
        accuracy = a/(n*4)
        print(accuracy)
        #print(predicted_labels)

        