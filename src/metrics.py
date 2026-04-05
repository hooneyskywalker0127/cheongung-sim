import pandas as pd

class Metrics:
    def __init__(self):
        self.intercept_success = {"BallisticMissile": 0, "CruiseMissile": 0, "Drone": 0}                                                                                                                                                                                         
        self.used_missile = 0
        self.intercept_fail = {"BallisticMissile": 0, "CruiseMissile": 0, "Drone": 0}
        self.number_hit = {"BallisticMissile": 0, "CruiseMissile": 0, "Drone": 0}
        self.battle_time = 0

    def record_success(self, threat_type):
        self.intercept_success[threat_type] += 1
        
    def record_used_missile(self,):
        self.used_missile += 1

    def record_fail(self,threat_type):
        self.intercept_fail[threat_type] += 1
        
    def record_hit(self, threat_type):
        self.number_hit[threat_type] += 1

    def record_battle_time(self, dt):
        self.battle_time +=dt
    
    def save_csv(self):
        df = pd.DataFrame({
    "threat_type" : ["BallisticMissile", "CruiseMissile","Drone" ],
    "success" : list(self.intercept_success.values()),
    "fail" : list(self.self.intercept_fail.values()),
    "number_hit" :list(self.number_hit.values()),
    "battle_time" : [self.battle_time]








})

