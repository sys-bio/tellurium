class Simulator:
    def __init__(self):
        self.computed_vales = {}

    def pre_simulation(self,model_roadrunner):
        model_roadrunner.simulate(0,1000,5000)

    def simulate_sensitivity(self, model_roadrunner):
        self.push("r1b_k2",model_roadrunner.getCC('PP_K', 'r1b_k2'))
        self.push("r8_a8",model_roadrunner.getCC('PP_K', 'r8a_a8'))
        self.push("r10a_a10",model_roadrunner.getCC('PP_K', 'r10a_a10'))

    def push(self, key, value):
        self.computed_vales[key] = value

    def get_computed_values(self):
        return(self.computed_vales)

