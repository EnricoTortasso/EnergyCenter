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
                ns = value[0]+value[1]
                ew = value[2]+value[3]
                if ns > ew:
                    verso = "ns"
                else:
                    verso = "ew"
                if agent_eid not in commands:
                    commands[agent_eid] = {}
                if model_eid not in commands[agent_eid]:
                    commands[agent_eid][model_eid] = {}
                commands[agent_eid][model_eid]['verso'] = verso
                #yield self.mosaik.set_data(commands)
                self.client.loop_start()
                self.client.publish("/".join(model_eid.split(".")) +"/" + agent_eid +"/verso",verso)
        # this works only for Python versions >=3.3.
        # For older versions use: raise StopIteration(time + 60)
        return time + 60


def main():
    return mosaik_api.start_simulation(Controller())


if __name__ == '__main__':
    main()