
import carla 

from xml.dom.expatbuilder import parseString
from scenario_follow_vehicle import ScenarioFollowVehicle

class ScenarioBase:

    #Set Client
    client = carla.Client('localhost', 2000)
    client.set_timeout(2.0)
    world = client.get_world()
    ego_vehicle = None
    #Set the ego vehicle actor
    actor_list = world.get_actors()
    for actor in actor_list:
        try:
            if(actor.attributes['role_name'] == 'ego_vehicle'):
               ego_vehicle = actor
        except: 
            pass


    def __init__(self, scenario):

        if(scenario == "follow_vehicle"):
            self.follow_vehicle()

                
        


    def follow_vehicle(self):          
        scenario = ScenarioFollowVehicle(self.world, self.ego_vehicle)
        scenario.run()

        
        