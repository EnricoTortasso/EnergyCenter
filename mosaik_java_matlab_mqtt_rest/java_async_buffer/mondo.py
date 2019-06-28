# demo_1.py
import mosaik

import mosaik.util
import itertools

# Sim config. and other parameters
SIM_CONFIG = {
    'ExampleSim1': {
        'connect': '127.0.0.1:9999',
    },
    'ExampleSim2': {
        'connect': '127.0.0.1:9998',
    },
    'ExampleCtrl': {
        'python': 'controller:Controller',
    },
    'Collector': {
        'python': 'collector:Collector',
    },
    'Buffer': {
        'python': 'buffer_sim:Buffer',
    }
}
END = 20 * 60  # 10 minutes

# Create World
world = mosaik.World(SIM_CONFIG)

rest = {
    "address": "127.0.0.1:8000",		# questo è il server http a cui connettersi, in questo caso un server sulla stessa macchina
    "attrs": {					        # questo è il dizionario che contiene le informazioni relative ad ogni attributo
        "pace1": {					    # ogni attributo indica:
            "GET": "/x.txt",			# l'url a cui richiedere il dato,
            "timeout": "4"			    # il tempo tra una richiesta e l'altra
        },
        "pace2": {
            "GET": "/y.txt",
            "timeout": "7"
        }
    }
}

# Start simulators
examplesim1 = world.start('ExampleSim1', eid_prefix='Model_')
examplesim2 = world.start('ExampleSim2', eid_prefix='Model_')
examplectrl = world.start('ExampleCtrl')
collector = world.start('Collector', step_size=60)
buffer = world.start("Buffer", extra_attrs=["pace1", "pace2"], rest=rest)


# Instantiate models
model1 = examplesim1.JModel.create(2)
model2 = examplesim2.JModel.create(2)
agent = examplectrl.Agent.create(2)
monitor = collector.Monitor()
buffer = buffer.Buffer()


# Connect entities
world.connect(buffer, model1[0], ("pace1", "pace"))
world.connect(buffer, model1[1], ("pace1", "pace"))
world.connect(buffer, model2[0], ("pace2", "pace"))
world.connect(buffer, model2[1], ("pace2", "pace"))
mosaik.util.connect_many_to_one(world, model1, agent[0], ('queue', 'q_in'), async_requests=True)
mosaik.util.connect_many_to_one(world, model2, agent[1], ('queue', 'q_in'), async_requests=True)
mosaik.util.connect_many_to_one(world, list(itertools.chain.from_iterable([model1, model2])), monitor, 'queue', "pace", 'verso', async_requests=True)

# Run simulation
world.run(until=END, rt_factor=0.025)

