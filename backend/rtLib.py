import networkx as nx
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from rtArch import CommuteSchedule

def rt_pool(sched_list: [CommuteSchedule]):
    """
    Function that will reccommend groups of people
    to ride together.
    """

    g = nx.Graph()

    for i, sched_i in enumerate(sched_list):
        g.add_node(i)

        for j in range(i):
            sched_j = sched_list[j]

            print(sched_i)
            print(sched_j)

            dep_distance = ((sched_i.departure_locX - sched_j.departure_locX) ** 2) + ((sched_i.departure_locY - sched_j.departure_locY) ** 2) ** 0.5
            print(dep_distance)

            arrival_distance = ((sched_i.arrival_locX - sched_j.arrival_locX) ** 2) + ((sched_i.arrival_locY - sched_j.arrival_locY) ** 2) ** 0.5
            print(arrival_distance)

            dep_time_diff = (sched_i.departure_time - sched_j.departure_time).total_seconds()
            print(dep_time_diff)

            arr_time_diff = (sched_i.arrival_time - sched_j.arrival_time).total_seconds()
            print(arr_time_diff)


    return 0

