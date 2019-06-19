import mosaik_api

META = {
    'models': {
        'ExModel': {
            'public': True,
            'params': [],
            'attrs': ['x'],
        },
    },
}


class ExSim(mosaik_api.Simulator):
    def __init__(self):
        super().__init__(META)
        self.eid_prefix = "exModel"
        self.models = {}

    def init_plus(self, sid, eid_prefix=None):
        if eid_prefix is not None:
            self.eid_prefix = eid_prefix
        return self.meta

    def create(self, num, model):
        next_eid = len(self.models)
        entities = []

        for i in range(next_eid, next_eid + num):
            eid = '%s%d' % (self.eid_prefix, i)
            self.models[eid] = 0
            entities.append({'eid': eid, 'type': model})

        return entities

    def step_plus(self, time, inputs):

        for eid, attrs in inputs.items():
            for attr, values in attrs.items():
                if attr == "x":
                    for src, val in values.items():
                        self.models[eid] += val

        if hasattr(self, "rest_commands"):
            if self.rest_commands != {}:
                x = self.rest_commands.get("x", None)
                if x is not None:
                    eid, x = x.split(":")
                    self.models[eid] = int(x)
                    del self.rest_commands["x"]


        return time + 60

    def get_data(self, outputs):
        data = {}
        for eid, attrs in outputs.items():
            data[eid] = {}
            for attr in attrs:
                if attr not in self.meta['models']['ExModel']['attrs']:
                    raise ValueError('Unknown output attribute: %s' % attr)

                data[eid][attr] = self.models[eid]

        return data


def main():
    return mosaik_api.start_simulation(ExSim())


if __name__ == '__main__':
    main()

