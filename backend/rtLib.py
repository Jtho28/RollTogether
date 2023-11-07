import networkx as nx
from datetime import datetime, timedelta
from flask_sqlalchemy import SQLAlchemy
from rtArch import CommuteSchedule

def rt_pool(sched_list: [CommuteSchedule], rider_id: int):
    """
    Function that will recommend groups of people
    to ride together.
    """

    dist_thresh = 0.009
    time_thresh = timedelta(minutes=7)
    rider = f"Rider: {rider_id}"

    g = nx.Graph()

    for i, sched_i in enumerate(sched_list):
        g.add_node(str(sched_i))

        for j in range(i):
            sched_j = sched_list[j]

            # print(sched_i)
            # print(sched_j)

            dep_distance = ((sched_i.departure_locX - sched_j.departure_locX) ** 2) + ((sched_i.departure_locY - sched_j.departure_locY) ** 2) ** 0.5
            # print(dep_distance)

            arrival_distance = ((sched_i.arrival_locX - sched_j.arrival_locX) ** 2) + ((sched_i.arrival_locY - sched_j.arrival_locY) ** 2) ** 0.5
            # print(arrival_distance)

            dep_time_diff = (sched_i.departure_time - sched_j.departure_time)
            # print(dep_time_diff)

            arr_time_diff = (sched_i.arrival_time - sched_j.arrival_time)
            # print(arr_time_diff)

            if (dep_distance <= dist_thresh 
                and arrival_distance <= dist_thresh
                and dep_time_diff <= time_thresh
                and arr_time_diff <= time_thresh):
                print(f"Users {sched_i.rider_id} and {sched_j.rider_id} can ride together")
                g.add_edge(str(sched_i), str(sched_j))


    print(g.nodes)
    print(g.edges)

    groups = nx.find_cliques(g)

    pos = []
    for clique in groups:
        if rider in clique:
            pos.append(clique)

    print(pos)
    return pos

