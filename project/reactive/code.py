class ReactiveAgent:
    def __init__(self, tools):
        self.tools = tools
        
    def process_request(self,vehicle_id,request_type):
        
        if request_type == "vehicle_history":
            return self.tools.searchVehicle(vehicle_id)
        
        elif request_type == "vehicle_company":
            return self.tools.getCarState(vehicle_id)
        
        elif request_type == "common_problems":
            return self.tools.getCarHistory(vehicle_id)
        
        elif request_type == "solution":
            return self.tools.getCarHistory(vehicle_id)
        
        else:
            return "Invalid request type. Please specify a valid request."