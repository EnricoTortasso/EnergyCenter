# demo_1.py
import mosaik

import mosaik.util


# Sim config. and other parameters
SIM_CONFIG = {
    'ExampleSim': {
        'connect': '127.0.0.1:9999',
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
END = 10 * 600  # 10 minutes

# Create World
world = mosaik.World(SIM_CONFIG)

rest = {
    "address": "127.0.0.1:8000",		#questo è il server http a cui connettersi, in questo caso un server sulla stessa 								macchina
    "attrs": {					        #questo è il dizionario che contiene le informazioni relative ad ogni attributo
        "pace": {					        #ogni attributo indica:
            "GET": "/x.txt",			#	l'url a cui richiedere il dato,
            "timeout": "5"			    #	il tempo tra una richiesta e l'altra
        }
    }
}

# Start simulators
examplesim = world.start('ExampleSim', eid_prefix='Model_')
examplectrl = world.start('ExampleCtrl')
collector = world.start('Collector', step_size=60)
buffer = world.start("Buffer",extra_attrs=["pace"], rest=rest)


# Instantiate models
model = examplesim.JModel()

agent = examplectrl.Agent.create(1)

monitor = collector.Monitor()

buffer = buffer.Buffer()


# Connect entities
world.connect(model, agent[0], ('queue', 'q_in'), async_requests=True)
world.connect(buffer, model, "pace")

world.connect(model, monitor, 'queue', "pace", 'verso', async_requests=True)


# Run simulation
world.run(until=END,rt_factor=0.005)