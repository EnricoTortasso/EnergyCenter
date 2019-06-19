Tutorial: come costruire un simulatore che comunichi con mqtt e/o http(rest)
per prima cosa creiamo un simulatore classico che funziona con mosaik.



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

    def init(self, sid, eid_prefix=None):
        if eid_prefix is not None:
            self.eid_prefix = eid_prefix
        return self.meta

    def create(self, num, model):
        next_eid = len(self.entities)
        entities = []

        for i in range(next_eid, next_eid + num):
            eid = '%s%d' % (self.eid_prefix, i)
            self.models[eid] = 0
            entities.append({'eid': eid, 'type': model})

        return entities

    def step(self, time, inputs):

        for eid, attrs in inputs.items():
            for attr, values in attrs.items():
                for src, val in values.items():
                    self.models[eid] += val

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






Questo è un simulatore banale i cui modelli possiedono un solo attributo x. Si nota che sono presenti i metodi init, create, step e 
get_data. 
aggiungiamo un controllore banale che incrementa x di 1 se x è minore di 6, altrimenti lo decrementa di 2.





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





e infine aggiungiamo un collettore che prenda i dati che vogliamo salvare (in questo caso x).





import collections
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
                print('  - %s: %s' % (attr, values))


if __name__ == '__main__':
    mosaik_api.start_simulation(Collector())





A questo punto aggiungiamo il main di mosaik per far partire la simulazione




import mosaik.util


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

END = 10 * 600  # 10 minutes

world = mosaik.World(SIM_CONFIG)

examplesim = world.start('ExSim', eid_prefix='Model_')
examplectrl = world.start('ExampleCtrl')
collector = world.start('Collector', step_size=60)

model = examplesim.ExModel()
agent = examplectrl.Agent()
monitor = collector.Monitor()

world.connect(model, agent, 'x', async_requests=True)
world.connect(model, monitor,'x', async_requests=True)

world.run(until=END)




Così come è adesso funziona come una normale simulazione standard di mosaik. Per aggiungere le modalità di comunicazione in 
mqtt e in http dobbiamo sostituire le funzioni init() con init_plus() e step() con step_plus() (basta cambiare il nome).
Facendo questo lasciamo a mosaik il controllo sulla init() e sulla step() "standard", facendogli creare i client mqtt e/o http 
nella init() e gestendoli nella step().
Ora bisogna dire quale servizio vogliamo utilizzare e altre varie informazioni utili alla connessione. Per farlo dobbiamo 
passare un dizionario contenente tutti i dati necessari durante la init().

Ipotizziamo che il nostro simulatore voglia chiedere ogni 10 secondi il valore di x a un sensore che comunica tramite http/rest.
Il dizionario che dovremo passare durante la create sarà:

rest = {
    "address": "127.0.0.1:8000",		#questo è il server http a cui connettersi, in questo caso un server sulla stessa macchina
    "attrs": {					#questo è il dizionario che contiene le informazioni relative ad ogni attributo
        "x": {					#ogni attributo indica: 
            "GET": "/x.txt",			#	l'url a cui richiedere il dato,
            "timeout": "10"			#	il tempo tra una richiesta e l'altra
            }
        }
    }

perciò nel main di mosaik quando si chiama la init() del simulatore dovremo passare anche il dizionario rest come parametro:

examplesim = world.start('ExSim', eid_prefix='Model_', rest=rest)


Fatto ciò torniamo nel nostro simulatore. Infatti ora grazie a questi cambiamenti ogni 10 secondi il simulatore chiederà il dato al 
server indicato, salvando la risposta in un nuovo attributo di dipo dizionario : rest_commands. La struttura di questo dizionario è
molto semplice:

rest_commands = {
		attr1 : val1,
		attr2 : val2,
		...	... ,
		}

Possiamo quindi modificare il metodo step_plus() per poter usare i dati ottenuti dal sensore.
Bisogna tenere conto che a questo punto diventa compito del programmatore decidere come usare i dati. I vari val1, val2, ecc.. sono tutti
in formato stringa, quindi possono contenere moltissime informazioni.
Nel nostro caso il dato che abbiamo richiesto è un file che contiene la stringa "Model_0:15", quindi per usarlo dovremo interpretarne il 
significato e poi agire di conseguenza (in questo caso a Model_0 assegneremo un valore di x pari a 15).

Dobbiamo poi decidere una volta usato il dato se vogliamo salvarlo o ci basta averlo usato una volta. Nel nostro caso vogliamo che solo 
appena letto questo influisca sulla simulazione, mentre vogliamo che dopo questa prosegua regolarmente. Per questo motivo dopo l'uso 
eliminiamo la chiave x dal dizionario (quando arriverà un nuovo dato questa verrà aggiunta nuovamente) 



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



A questo punto per provare se la nostra simulazione funziona creiamo un server sulla nostra macchina in ascolto alla porta 8000:



import http.server
import socketserver

PORT = 8000

Handler = http.server.SimpleHTTPRequestHandler

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print("serving at port", PORT)
    httpd.serve_forever()



Nella stessa cartella mettiamo il file da cui riceveremo il dato richiesto e infine modifichiamo il main di mosaik per fare durare la
simulazione abbastanza da permettere che scadano i 10 secondi di timeout.


END = 10 * 600
world.run(until=END, rt_factor=0.01)


In questo modo la simulazione durerà un minuto.