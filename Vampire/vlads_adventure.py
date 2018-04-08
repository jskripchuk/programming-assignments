#James Skripchuk
#CISC320

import os
import networkx as nx
import heap as atlas_heap

#OUTLINE OF THE ALGORITHM:
#1) Iterate through possible routes, and remove any impossible routes
#       Eg. Remove routes that depart before 18:00 or arrive after 06:00
#
#2) If node A has multiple routes to node B, choose the route that has the
#   earliest arrival time at B. (This is not necessarily the route
#   that has the shortest travel time).
#
#3) Now that we have a graph that is not a multigraph, we perform a modified
#   Dijsktras algorithm, who's update function aims to find paths that have
#   the earliest arrivial times at a destination.
#
#4) At the end of the Dijsktras, the amount of blood bags that Vlad needs is
#   rounded(time/24)-1. [The -1 is because we start our Dijsktras at 18:00,
#   which is after 12:00, so we assume Vlad already had lunch before he started
#   his trip]

#A route is valid for Vlad if it leaves after 1800 and arrives before 0600
def is_valid_route(departure_time,travel_time):
    arrival_time = departure_time+travel_time
    return departure_time >= 18 and arrival_time <= 30

#A special mod function that I use in order to signify numerically which arrival
#times are earlier, so thus 00:00 would map to 24 showing that it arrives later
#than 23:00
def special_mod(time):
    val = time%24
    if val<18:
        val+=24
    return val

#Checks to see if old has an earlier arrival time
def old_has_earlier_arrival(old_dept_time, old_travel_time, new_dept_time, new_travel_time):
    old_arrival_time = (old_dept_time+old_travel_time)
    new_arrival_time = (new_dept_time+new_travel_time)

    return old_arrival_time < new_arrival_time

#Total Worst Case Time: Somewhere along the lines of O(ElogV)
def modified_dijkstra(graph, source, destination):
    time = {}
    prev = {}

    #Vlad arrives at his first station at 6
    time[source] = 18

    min_heap = atlas_heap.Heap()

    for vertex in graph:
        if vertex != source:
            time[vertex] = float("inf")
            prev[vertex] = None
        #Worst Case: log(V)
        min_heap.insert(time[vertex],vertex)

    while not min_heap.empty():
        #Worst Case: log(V)
        u = min_heap.deleteMin()
        current_time = u[0]
        current_vertex = u[1]

        for neighbor in graph[current_vertex]:
            edge = graph[current_vertex][neighbor]
            departure_time = edge['departure_time']
            travel_time = edge['travel_time']
            #O(1) op due to custom hash table implementation
            neighbor_heap_node = min_heap.getByName(neighbor)

            arrival_time = special_mod(current_time)
            #calculating the value of the next node
            #We arrived after the possible departure time, so we have to wait the day
            if arrival_time > departure_time:
                #Do thing
                waiting_time = 24+departure_time-arrival_time
            else:
                #We've arrived before departure so we don't have to wait
                waiting_time = departure_time-arrival_time


            alt = waiting_time+travel_time+current_time
            if alt < time[neighbor]:
                time[neighbor] = alt
                neighbor_heap_node.data = alt
                prev[neighbor] = current_vertex
                #Worst Case: log(V)
                min_heap.decreaseKey(neighbor_heap_node)

    if destination not in time or time[destination] == float("inf"):
        return -1
    else:
        blood_bags = round(time[destination]/24)-1
        return blood_bags

def read_write(inpath, outpath):
    #Make sure we're in the correct working directory
    script_dir = os.path.dirname(__file__)
    read = open(os.path.join(script_dir,inpath))

    content = read.readlines()
    content = [x.strip("\n") for x in content]
    read.close()

    #TODO
    #Use a better structure for O(1) pop
    test_case_num = int(content.pop(0))

    result_string = ""

    #Run Tests
    for i in range(0, test_case_num):
        route_graph = nx.DiGraph()

        number_of_routes = int(content.pop(0))

        taken_routes = {}

        for j in range(0, number_of_routes):
            route = content.pop(0).split()
            departure_city = route[0]
            arrival_city = route[1]
            departure_time = int(route[2])
            travel_time = int(route[3])

            if is_valid_route(special_mod(departure_time),travel_time):
                if not route_graph.has_edge(departure_city,arrival_city):
                    route_graph.add_edge(departure_city,arrival_city, departure_time = special_mod(departure_time), travel_time = travel_time)
                else:
                    old_edge = route_graph[departure_city][arrival_city]
                    #If the new one arrives earlier
                    if not old_has_earlier_arrival(old_edge['departure_time'], old_edge['travel_time'], special_mod(departure_time),travel_time):
                        route_graph.add_edge(departure_city,arrival_city,departure_time = special_mod(departure_time), travel_time = travel_time)

        from_to = content.pop(0).split()

        result = modified_dijkstra(route_graph,from_to[0],from_to[1])
        result_string += "Test Case "+str(i)+".\n"

        if result == -1:
            result_string +="There is no route Vladimir can take.\n"
        else:
            result_string +="Vladimir needs "+str(result)+" litre(s) of blood.\n"

    write = open(os.path.join(script_dir,outpath), 'w')
    print(result_string)
    write.write(result_string)

    write.close()

read_write("sample_in.txt","output.txt")
