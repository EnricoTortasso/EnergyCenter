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
nella init() e gestendoli nella step(). Questa modifica va fatta SOLO nei simulatori a cui vogliamo aggiungere queste funzionalità,
tutti gli altri possono rimanere nella forma normale. Inoltre se nella step() è presente una set_data(),

es. il controllore

step()

	...
	yield self.mosaik.set_data(commands)
        return time + 60

la step_plus() dovrà essere:

step_plus()

	...
        return time + 60, commands

quindi i comandi che andrebbero nella yield vengono ritornati normalmente, si occuperà poi mosaik di gestirli.

  
Ora bisogna dire quale servizio vogliamo utilizzare e altre varie informazioni utili alla connessione. Per farlo dobbiamo 
passare un dizionario contenente tutti i dati necessari durante la init().

Ipotizziamo che il nostro simulatore voglia chiedere ogni 10 secondi il valore di x a un sensore che comunica tramite http/rest.
Il dizionario che dovremo passare durante la init() sarà:

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


In questo modo la simulazione durerà un minuto. Verifichiamo l'andamento di x:

[0, 1, 2, 3, 4, 5, 6, 4, 5, 6, 4, 5, 6, 4, 5, 6, 4, 15, 13, 11, 9, 7, 5, 6, 4, 5, 6, 4, 5, 6, 4, 5, 6, 4, 15, 13, 11, ...

Si nota chiaramente che dopo un certo intervallo il valore di x viene impostato a 15 proprio come volevamo, e ogni volta che scade il 
timeout il processo si ripete.


Vediamo ora come inserire anche la comunicazione tramite mqtt.

Il procedimento è analogo al caso precedente: creiamo i simulatori standard, poi per quelli a cui vogliamo aggiungere il servizio 
sostituiamo i metodi init() e step(). Per comunicare che vogliamo usare mqtt creiamo un dizionario che passeremo all'init().


mqtt = {
	"broker" : "127.0.0.1",
	"x" : {					#nome dell'attributo
		"topic" : "test/sensor1/x",	#topic a cui iscriversi
		"timeout_reset" : True		#indica se quando riceve un aggiornamento su un attributo deve azzerare il timer http/rest
	}
}


ora lo passiamo all'init()


examplesim = world.start('ExSim', eid_prefix='Model_', rest=rest, mqtt=mqtt)


A questo punto creiamo un sensore che mandi dei messaggi sul topic indicato:


import paho.mqtt.client as mqtt #import the client1
import time

broker_address = "127.0.0.1"
client = mqtt.Client("Sensor") #create new instance
client.connect(broker_address) #connect to broker
client.loop_start() #start the loop


client.publish("test/sensor1/x", "Model_0:20")
time.sleep(5)
client.publish("test/sensor1/x", "Model_0:0")
time.sleep(5)
client.publish("test/sensor1/x", "Model_0:20")
time.sleep(15)
client.publish("test/sensor1/x", "Model_0:100")



i messaggi sono in formato uguale a quelli ricevuti tramite http (anche qui è compito del programmatore sapere come interpretarli e 
usarli). Notiamo che i primi messaggi vengono inviati con un intervallo di 5 secondi l'uno dall'altro. In questo modo, poichè avevamo
dato a mqtt il comando di azzerare i timeout, http non viene usato per richiedere il dato. Tra il terzo e il quarto messaggio c'è però
un intervallo di 15 secondi, abbastanza da far scadere il timeout e far partire una richiesta http.
Come prima otteniamo un novo attributo nel nostro simulatore: mqtt_commands (la cui struttura è uguale a quella di rest_commands)
Andiamo quindi nel metodo step_plus() per decidere come usare i nuovi dati a disposizione. Come prima vogliamo utilizzarli solo appena
arrivati e poi eliminarli, quindi step_plus() sarà:


    def step_plus(self, time, inputs):

        for eid, attrs in inputs.items():
            for attr, values in attrs.items():
                if attr == "x":
                    for src, val in values.items():
                        self.models[eid] += val

        if hasattr(self, "rest_commands"):			# in teoria questo potrebbe non esserci dato che avendo programmato noi il simulatore sappiamo se comunica con http o no
            if self.rest_commands != {}:
                x = self.rest_commands.get("x", None)
                if x is not None:
                    eid, x = x.split(":")
                    self.models[eid] = int(x)
                    del self.rest_commands["x"]
        if hasattr(self, "mqtt_commands"):			# in teoria questo potrebbe non esserci dato che avendo programmato noi il simulatore sappiamo se comunica con mqtt o no
            if self.mqtt_commands != {}:
                x = self.mqtt_commands.get("x", None)
                if x is not None:
                    eid, x = x.split(":")
                    self.models[eid] = int(x)
                    del self.mqtt_commands["x"]

        return time + 60




Come prima avviamo il server http, il main di mosaik e il sensore e osserviamo l'output della simulazione.

[0, 1, 2, 3, 4, 20, 18, 16, 14, 12, 10, 8, 6, 0, 1, 2, 3, 4, 5, 6, 4, 5, 20, 18, 16, 14, 12, 10, 8, 6, 4, 5, 6, 4, 5, 6, 4, 5, 15, 13, 11, 9, 7, 5, 6, 4, 5, 100, 98, 96]

il primo messaggio è ricevuto tramite mqtt e imposta il valore di x a 20. Dopo 5 secondi arriva un'altro messaggio che lo imposta a 0 e 
dopo altri 5 nuovamente a 20. Ora per 15 secondi mqtt non manderà più messaggi, facendo scadere il timeout e forzando il simulatore a 
effettuare una richiesta tramite http. Il messaggio di risposta riporta il valore di x a 15, mentre dopo circa 5 secondi mqtt porta il 
valore a 100


Ora vediamo l'ultimo caso in cui vogliamo usare solo mqtt:

Per dire a mosaik che il simulatore useà solo mqtt basta non passargli alcun attributo rest.

[0, 1, 2, 3, 20, 18, 16, 14, 12, 10, 8, 6, 0, 1, 2, 3, 4, 5, 6, 4, 20, 18, 16, 14, 12, 10, 8, 6, 4, 5, 6, 4, 5, 6, 4, 5, 6, 4, 5, 6, 4, 5, 6, 4, 5, 100, 98, 96, 94, 92]

questo è il risultato di una run con gli stessi parametri di quella precedente, ma senza aver passato il parametro rest.
Osserviamo che adesso c'è un buco di 15 secondi in cui il sensore mqtt non manda messaggi e nient'altro modifica l'andamento del valore
di x.


Quindi adesso sappiamo costruire dei simulatori che possono comunicare con l'esterno tramite mqtt, http/rest o una combinazione dei due.
Ovviamente questi simulatori supportano la simulazione distribuita, come i simulatori standard di mosaik.


