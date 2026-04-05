

class Metrics:
    def __init__(self):
        self.intercept_success = {"BallisticMissile": 0, "CruiseMissile": 0, "Drone": 0}                                                                                                                                                                                         
        self.used_missile = 0
        self.intercept_fail = {"BallisticMissile": 0, "CruiseMissile": 0, "Drone": 0}
        self.number_hit = {"BallisticMissile": 0, "CruiseMissile": 0, "Drone": 0}
        self.battle_time = 0