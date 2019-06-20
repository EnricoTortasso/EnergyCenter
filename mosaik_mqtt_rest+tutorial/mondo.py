# demo_1.py

import mosaik.util


# Sim config. and other parameters
SIM_CONFIG = {
    'ExSim': {

        'python': 'exSimulator:ExSim',
    },
    'ExampleCtrl': {

        'python': 'controller:Controller',
    },
    'Collector': {
        'cmd': 'python collector.py %(addr)s',
    },
}

mosaik_config = {
	'start_timeout': 600,  # seconds
	'stop_timeout': 10,  # seconds
}

END = 50 * 60  # 10 minutes

# Create World
world = mosaik.World(SIM_CONFIG)

# Start simulators
rest = {
    "address": "127.0.0.1:8000",
    "attrs": {
        "x": {
            "GET": "/x.txt",
            "timeout": "10"
        }
    }
}

mqtt = {
    "broker": "127.0.0.1",
    "attrs": {
        "x": {
            "topic": "test/sensor1/x",
            "timeout_reset": True
        }
    }
}

examplesim = world.start('ExSim', eid_prefix='Model_', mqtt=mqtt, rest=rest)
examplectrl = world.start('ExampleCtrl')
collector = world.start('Collector', step_size=60)



# Instantiate models
model = examplesim.ExModel()

agent = examplectrl.Agent()

monitor = collector.Monitor()

#odysseus = odysseusModel.Odysseus.create(1)
#ody = odysseus[0]


#world.connect(model, ody, 'P', 'Vm')



# Connect entities
#for model, agent in zip(models, agents):
world.connect(model, agent, 'x', async_requests=True)


world.connect(model, monitor,'x', async_requests=True)


# Run simulation
world.run(until=END, rt_factor=0.01)