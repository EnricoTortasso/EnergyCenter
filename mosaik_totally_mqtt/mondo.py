# demo_1.py
import mosaik

import mosaik.util


# Sim config. and other parameters
SIM_CONFIG = {
    'ExampleSim': {
        'connect': '127.0.0.1:6666'
        #'python': 'simulator_mosaik:ExampleSim',
    },
    'ExampleCtrl': {

        'connect': '127.0.0.1:6667',
        #'python': 'controller:Controller',
    },
    'Collector': {
        'connect': '127.0.0.1:6668',
        #'python': 'collector:Collector',
    },
    #'Odysseus': {
     #   'connect': '127.0.0.1:5554',
    #}
}
END = 10 * 60  # 10 minutes

# Create World

world = mosaik.World(SIM_CONFIG)

# Start simulators
examplesim = world.start('ExampleSim', eid_prefix='Model_')
examplectrl = world.start('ExampleCtrl')
collector = world.start('Collector', step_size=60)
#odysseusModel = world.start('Odysseus', step_size=60*15)


# Instantiate models
model = examplesim.ExampleModel()


agent = examplectrl.Agent()

monitor = collector.Monitor()

#odysseus = odysseusModel.Odysseus.create(1)
#ody = odysseus[0]


#world.connect(model, ody, 'P', 'Vm')



# Connect entities
#for model, agent in zip(models, agents):
world.connect(model, agent, ("queue", "q_in"), async_requests=True)


world.connect(model, monitor, 'queue', 'pace', 'verso', async_requests=True)
#mosaik.util.connect_many_to_one(world,models,monitor,'queue', 'pace', 'verso')

# Run simulation
world.run(until=END, rt_factor=0.025)