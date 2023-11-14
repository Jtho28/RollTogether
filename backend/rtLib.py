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

    uno_north = {'X': [96.01661, 96.01616],
                 'Y': [41.25780, 41.25763]}
    
    midtown = {'X': [95.96641, 95.95730],
               'Y': [41.26016, 41.25582]}

    eppley = {'X': [95.91622, 95.87575],
              'Y': [41.31906, 41.28308]}


    regions = {'uno_north': [(96.01661, 96.01616), (41.25780, 41.25763)],
               'midtown':   [(95.96641, 95.95730), (41.26016, 41.25582)],
               'eppley':    [(95.91622, 95.87575), (41.31906, 41.28308)],
               'aksarben':  [(96.02075, 96.00885), (41.24897, 41.23538)],
              }


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


            for region, boundaries in regions.items():
                latitude_range, longitude_range = boundaries
                # print(latitude_range)
                # print(longitude_range)
                if (latitude_range[1] <= sched_i.arrival_locX <= latitude_range[0]
                   and latitude_range[1] <= sched_j.arrival_locX <= latitude_range[0]
                   and longitude_range[1] <= sched_i.arrival_locY <= longitude_range[0]
                   and longitude_range[1] <= sched_j.arrival_locY <= longitude_range[0]
                   and dep_time_diff <= time_thresh
                   and arr_time_diff <= time_thresh):

                     print(f"Users {sched_i.rider_id} and {sched_j.rider_id} can ride together to {region}")
                     g.add_edge(str(sched_i), str(sched_j))

            # if (dep_distance <= dist_thresh 
            #     and arrival_distance <= dist_thresh
            #     and dep_time_diff <= time_thresh
            #     and arr_time_diff <= time_thresh):
            #     print(f"Users {sched_i.rider_id} and {sched_j.rider_id} can ride together")
            #     g.add_edge(str(sched_i), str(sched_j))


    print(g.nodes)
    print(g.edges)

    groups = nx.find_cliques(g)

    pos = []
    for clique in groups:
        if rider in clique:
            pos.append(clique)

    print(f"Group {pos}")
    return pos

