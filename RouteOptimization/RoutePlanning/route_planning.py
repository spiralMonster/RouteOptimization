from datetime import datetime
import time
from future.backports.datetime import timedelta
from langchain_google_genai import ChatGoogleGenerativeAI
from .BestPossibleRoutes.get_best_possible_routes import GetBestPossibleRoute
from .RoadwayRouteOptimization.get_info_roadway_route import GetInfoRoadRoute
from .RailwayRouteOptimization.get_info_rail_routes import GetInfoRailRoutes
from .AirwayRouteOptimization.get_airway_routes import GetInfoAirwayRoute
from .SeawayRouteOptimization.get_info_seaway_route import GetInfoSeaRoute


def PerformRoutePlanning(model,source,destination):
    routes = GetBestPossibleRoute(model, source,destination)
    ind = 1
    final_result = {}
    for route in routes:
        results = {}
        current = datetime.now()
        for key, value in route.items():
            if key == 'roadways':
                roadway_route = []
                for src_dest in value:
                    src_dest = src_dest.split("-")
                    src = src_dest[0]
                    dest = src_dest[1]
                    route_info = GetInfoRoadRoute(model, src, dest)
                    time_to_add = timedelta(hours=1, minutes=0)
                    current = current + time_to_add
                    route_info['Departure Date'] = current.date().strftime("%d-%m-%Y")
                    route_info['Departure Time'] = current.time().strftime("%H:%M")
                    journey_time = route_info['time_required']
                    route_info['time_required'] = str(route_info['time_required']) + " (in hours)"
                    route_info['expected_cost'] = str(route_info['expected_cost']) + " (in INR)"
                    route_info['carbon_emission'] = str(route_info['carbon_emission']) + " (in kgs)"
                    time_to_add = timedelta(hours=journey_time, minutes=0)
                    current = current + time_to_add
                    route_info['Arrival Date'] = current.date().strftime("%d-%m-%Y")
                    route_info['Arrival Time'] = current.time().strftime("%H:%M")
                    roadway_route.append(route_info)
                results['Roadway routes'] = roadway_route

            elif key == 'railways':
                railway_route = []
                for src_dest in value:
                    src_dest = src_dest.split("-")
                    src = src_dest[0]
                    dest = src_dest[1]
                    route_info = GetInfoRailRoutes(model, src, dest, current)

                    dep = route_info['Departure Date'] + ' ' + route_info['Departure Time']
                    dep = datetime.strptime(dep, "%d %b %H:%M").replace(year=2024)
                    route_info['Departure Date'] = dep.date().strftime("%d-%m-%Y")
                    route_info['Departure Time'] = dep.time().strftime("%H:%M")

                    arr = route_info['Arrival Date'] + ' ' + route_info['Arrival Time']
                    arr = datetime.strptime(arr, "%d %b %H:%M").replace(year=2024)
                    route_info['Arrival Date'] = arr.date().strftime("%d-%m-%Y")
                    route_info['Arrival Time'] = arr.time().strftime("%H:%M")

                    route_info['Total Expenditure'] = str(route_info['Total Expenditure']) + " (in INR)"
                    route_info['Carbon Emission'] = str(route_info['Carbon Emission']) + ' (in kgs)'

                    current = arr
                    railway_route.append(route_info)
                results['Railway routes'] = railway_route

            elif key == 'airways':
                airway_route = []
                for src_dest in value:
                    time_to_add = timedelta(hours=24, minutes=0)
                    current = current + time_to_add
                    src_dest = src_dest.split("-")
                    src = src_dest[0]
                    dest = src_dest[1]
                    route_info = GetInfoAirwayRoute(model, src, dest, current.date())

                    dep = route_info['Departure Time']
                    dep = datetime.strptime(dep, "%d %b %H:%M")
                    route_info['Departure Date'] = dep.date().strftime("%d-%m-%Y")
                    route_info['Departure Time'] = dep.time().strftime("%H:%M")

                    arr = route_info['Arrival Time']
                    arr = datetime.strptime(arr, "%d %b %H:%M")
                    route_info['Arrival Date'] = arr.date().strftime("%d-%m-%Y")
                    route_info['Arrival Time'] = arr.time().strftime("%H:%M")

                    current = arr

                    airway_route.append(route_info)
                results['Airway routes'] = airway_route

            else:
                seaway_route = []
                for src_dest in value:
                    src_dest = src_dest.split("-")
                    src = src_dest[0]
                    dest = src_dest[1]
                    route_info = GetInfoSeaRoute(model, src, dest)
                    time_to_add = timedelta(hours=1, minutes=0)
                    current = current + time_to_add
                    route_info['Departure Date'] = current.date().strftime("%d-%m-%Y")
                    route_info['Departure Time'] = current.time().strftime("%H:%M")
                    journey_time = route_info['time_required']
                    route_info['time_required'] = str(route_info['time_required']) + " (in hours)"
                    route_info['expected_cost'] = str(route_info['expected_cost']) + " (in INR)"
                    route_info['carbon_emission'] = str(route_info['carbon_emission']) + " (in kgs)"
                    time_to_add = timedelta(hours=journey_time, minutes=0)
                    current = current + time_to_add
                    route_info['Arrival Date'] = current.date().strftime("%d-%m-%Y")
                    route_info['Arrival Time'] = current.time().strftime("%H:%M")
                    seaway_route.append(route_info)

                results['Seaway routes'] = seaway_route

        final_result[f'Route {ind}'] = results
        ind += 1
        time.sleep(5)

    return final_result


if __name__=='__main__':
    model = ChatGoogleGenerativeAI(
        model="gemini-1.5-pro",
        api_key='AIzaSyCve8Wj4fQj52DNw9qvjzcOesPfko4D084'
    )
    source=input('Enter source city: ')
    destination=input('Enter destination city: ')
    results=RoutePlanning(model,source,destination)
    print(results)




