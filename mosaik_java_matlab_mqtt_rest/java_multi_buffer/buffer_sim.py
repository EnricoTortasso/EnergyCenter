import mosaik_api

META = {
    'models': {
        'Buffer': {
            'public': True,
            'params': [],
            'attrs': []
        },
    },
}


class Buffer(mosaik_api.Simulator):
    def __init__(self):
        super().__init__(META)
        self.eid = "Buffer"

    def init_plus(self, sid, extra_attrs=None):

        for i in extra_attrs:
            META["models"]["Buffer"]["attrs"].append(i)
            setattr(self, i, None)
        return self.meta

    def create(self, num, model):

        return [{'eid': self.eid, 'type': model}]

    def step_plus(self, time, inputs):
        dic = dict(self.rest_commands)
        for attr, val in dic.items():
            setattr(self, attr, val)
            del self.rest_commands[attr]

        return time + 60  # Step size is 1 minute

    def get_data(self, outputs):
        data = {}
        for eid, attrs in outputs.items():
            data[eid] = {}
            for attr in attrs:
                if attr not in self.meta['models']['Buffer']['attrs']:
                    raise ValueError('Unknown output attribute: %s' % attr)

                # Get model.val or model.delta:
                data[eid][attr] = getattr(self, attr)

        for eid, attrs in outputs.items():
            for attr in attrs:
                setattr(self, attr, None)

        return data


def main():
    return mosaik_api.start_simulation(ExampleSim())


if __name__ == '__main__':
    main()

