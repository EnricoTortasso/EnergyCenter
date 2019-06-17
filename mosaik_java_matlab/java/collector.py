# collector.py
import collections
import pprint
import matplotlib.pyplot as plt
import mosaik_api


META = {
    'models': {
        'Monitor': {
            'public': True,
            'any_inputs': True,
            'params': [],
            'attrs': [],
        },
    },
}


class Collector(mosaik_api.Simulator):
    def __init__(self):
        super().__init__(META)
        self.eid = None
        self.data = collections.defaultdict(lambda:
                                            collections.defaultdict(list))
        self.step_size = None

    def init(self, sid, step_size):
        self.step_size = step_size
        return self.meta

    def create(self, num, model):
        if num > 1 or self.eid is not None:
            raise RuntimeError('Can only create one instance of Monitor.')

        self.eid = 'Monitor'
        return [{'eid': self.eid, 'type': model}]

    def step(self, time, inputs):
        data = inputs[self.eid]
        for attr, values in data.items():
            for src, value in values.items():
                self.data[src][attr].append(value)

        return time + self.step_size

    def finalize(self):
        print('Collected data:')
        for sim, sim_data in sorted(self.data.items()):
            print('- %s:' % sim)
            for attr, values in sorted(sim_data.items()):
                '''# x axis values
                x = range(0,1000)
                # corresponding y axis values
                y = values

                # plotting the points
                plt.plot(x, y)

                # naming the x axis
                plt.xlabel('x - axis')
                # naming the y axis
                plt.ylabel('y - axis')

                # giving a title to my graph
                plt.title('My first graph!')

                # function to show the plot
                plt.show()'''

                print('  - %s: %s' % (attr, values))



if __name__ == '__main__':
    mosaik_api.start_simulation(Collector())