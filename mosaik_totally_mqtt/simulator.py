# simulator.py
"""
This module contains a simple example simulator.

"""
from random import randint


class Model:
    """
    simulatore di un semaforo

    """
    def __init__(self):
        self.queue = [0, 0, 0, 0]
        self.pace = 1 
        self.verso = "ns"
        self.old_verso= "ew"

    def step(self):
        """Perform a simulation step """
        if self.verso == self.old_verso:
            self.pace += 1
        else:
            self.pace = 1

        for i in range(3):
            self.queue[randint(0, 3)] += 1

        if self.verso == "ns":
            self.queue[0] -= self.pace
            self.queue[1] -= self.pace
        else :
            self.queue[2] -= self.pace
            self.queue[3] -= self.pace
        
        for i in range(4):
            if self.queue[i] < 0:
                self.queue[i] = 0

        self.old_verso = self.verso


class Simulator(object):
    """Simulates a number of ``Model`` models and collects some data."""
    def __init__(self):
        self.models = []
        self.data = []

    def add_model(self):
        """Create an instances of ``Model`` with *init_val*."""
        model = Model()
        self.models.append(model)
        self.data.append([])  # Add list for simulation data

    def step(self, dirs=None):
        """Set new model inputs from *deltas* to the models and perform a
        simulatino step.

        *deltas* is a dictionary that maps model indices to new delta values
        for the model.

        """
        if dirs:
            # Set new deltas to model instances
            for idx, verso in dirs.items():
                self.models[idx].verso = verso

        # Step models and collect data
        for i, model in enumerate(self.models):
            model.step()
            state = [list(model.queue), model.verso]
            self.data[i].append(state)


if __name__ == '__main__':
    # This is how the simulator could be used:
    
    sim=Simulator()
    sim.add_model()
    sim.step()
    sim.step()
    sim.step()
    sim.step()
    sim.step()
    sim.step()
    sim.step({0: "ew", })
    sim.step()
    sim.step()
    sim.step({0: "ns", })
    
    print("%s" % sim.data)
