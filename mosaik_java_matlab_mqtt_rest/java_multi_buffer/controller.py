# controller.py
"""
A simple demo controller.

"""
import mosaik_api
from typing import Any

META = {
    'models': {
        'Agent': {
            'public': True,
            'params': [],
            'attrs': ['q_in'],
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
            values = attrs.get('q_in', {})
            for model_eid, value in values.items():
                q=value.split(",")  # type: list
                ns = int(q[0])+ int(q[1])
                ew = int(q[2]) + int(q[3])
                if ns>ew:
                    verso = "ns"
                else:
                    verso = "ew"


                if ns>=10 and ew > 10 :
                    if ew > 2*ns :
                        verso = "ew"
                    else :
                        verso = "ns"

                if agent_eid not in commands:
                    commands[agent_eid] = {}
                if model_eid not in commands[agent_eid]:
                    commands[agent_eid][model_eid] = {}
                commands[agent_eid][model_eid]['verso'] = verso

        yield self.mosaik.set_data(commands)

        # this works only for Python versions >=3.3.
        # For older versions use: raise StopIteration(time + 60)
        return time + 60


def main():
    return mosaik_api.start_simulation(Controller())


if __name__ == '__main__':
    main()