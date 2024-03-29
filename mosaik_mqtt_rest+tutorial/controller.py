# controller.py
"""
A simple demo controller.

"""
import mosaik_api


META = {
    'models': {
        'Agent': {
            'public': True,
            'params': [],
            'attrs': ['x'],
        },
    },
}


class Controller(mosaik_api.Simulator):
    def __init__(self):
        super().__init__(META)
        self.agents = []

    def create(self, num, model):
        n_agents = len(self.agents)
        entities = []
        for i in range(n_agents, n_agents + num):
            eid = 'Agent_%d' % i
            self.agents.append(eid)
            entities.append({'eid': eid, 'type': model})

        return entities

    def step(self, time, inputs):
        commands = {}
        for agent_eid, attrs in inputs.items():
            values = attrs.get('x', {})
            for model_eid, value in values.items():
                if value > 5:
                    data = -2
                else:
                    data = 1

                if agent_eid not in commands:
                    commands[agent_eid] = {}
                if model_eid not in commands[agent_eid]:
                    commands[agent_eid][model_eid] = {}
                commands[agent_eid][model_eid]['x'] = data

        yield self.mosaik.set_data(commands)

        return time + 60


def main():
    return mosaik_api.start_simulation(Controller())


if __name__ == '__main__':
    main()