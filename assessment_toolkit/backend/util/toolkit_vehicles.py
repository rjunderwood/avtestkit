


#Return toolkit vehicles. 

class ToolkitVehicles: 

    blueprint_library = None 
    
    def __init__(self, blueprint_library): 
        
        self.blueprint_library = blueprint_library
    

    def create(self, type):
        if type == 'van':
            return self.van()
        elif type == 'sedan':
            return self.sedan()
        elif type == 'motorbike':
            return self.motorbike()
        elif type == 'small_car':
            return self.small_car()
        elif type == 'suv':
            return self.suv()
        else:
            #Returning a carla vehicle actor Id
            try:
                return self.blueprint_library.filter(type)[0]
            except:
                return self.sedan()

    def van(self):
        return self.blueprint_library.filter('vehicle.carlamotors.carlacola')[0]
    
    def sedan(self):
        return self.blueprint_library.filter('vehicle.tesla.model3')[0]
    
    def motorbike(self):
        return self.blueprint_library.filter('vehicle.kawasaki.ninja')[0]


    def small_car(self):
        return self.blueprint_library.filter('vehicle.mini.cooperst')[0]

    def suv(self):
        return self.blueprint_library.filter('vehicle.nissan.patrol')[0]

    