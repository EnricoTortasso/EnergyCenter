# Tutorial: collegare simulatori java e matlab a servizi mqtt e http


Prendiamo il simulatore in java che abbiamo usato in precedenza. Vogliamo che ogni 5 secondi richieda
un dato tramite il servizio rest. 
Finora solo i simulatori in python sono in grado di usare i servizi **mqtt** e **rest**, quindi 
dovremo usarne uno che faccia da intermediario.

Creiamo quindi un simulatore fittizio, il cui unico scopo sia quello di ricevere i messaggi e mandarli
a chi di dovere.

## Buffer

import mosaik_api

META = {
    'models': {
        'Buffer': {
            'public': True,
            'params': [],
            'attrs': []						#per ora non mettiamo alcun attributo, in questo modo creiamo un buffer riutilizzabile e adattabile
        },
    },
}


class Buffer(mosaik_api.Simulator):
    def __init__(self):
        super().__init__(META)
        self.eid = "Buffer"
								#notare: init_plus()
    def init_plus(self, sid, extra_attrs=None):			#extra_attrs è un array di stringhe contenente i nomi degli attributi che gestirà il buffer

        for i in extra_attrs:
            META["models"]["Buffer"]["attrs"].append(i)		#per ogni attributo lo aggiungiamo al meta
            setattr(self, i, None)				#e creiamo un attributo con lo stesso nome
        return self.meta

    def create(self, num, model):

        return [{'eid': self.eid, 'type': model}]		#è un unico modello, la create è fittizia perchè tanto un buffer può esser usato da tutti i simulatori

    def step_plus(self, time, inputs):				#notare: step_plus()
        dic = dict(self.rest_commands)				#copio il dizionario dei comandi in arrivo
        for attr, val in dic.items():
            setattr(self, attr, val)				#scrivo come valore degli attributi le stringhe ricevute tramite rest
            del self.rest_commands[attr]			#cancello gli ultimi messaggi ricevuti

        return time + 60  # Step size is 1 minute

        def get_data(self, outputs):
        data = {}
        for eid, attrs in outputs.items():
            data[eid] = {}
            for attr in attrs:
                if attr not in self.meta['models']['Buffer']['attrs']:
                    raise ValueError('Unknown output attribute: %s' % attr)

                # Get model.val or model.delta:
                data[eid][attr] = getattr(self, attr)				#quando qualcuno gli chiede un dato gli dà la stringa ricevuta

        for eid, attrs in outputs.items():
            for attr in attrs:
                setattr(self, attr, None)					#poi la rende nulla finchè non ne riceverà un'altra

        return data


def main():
    return mosaik_api.start_simulation(ExampleSim())


if __name__ == '__main__':
    main()


Questo simulatore Buffer non fa altro che fare da tramite tra il simulatore scritto in java e il "sensore" a cui dovrebbe richiedere i dati.
é stato scritto nel modo più generale possibile e dovrebbe andare bene per gestire (**con un unico simulatore**) tutte le necessità di tutti gli
altri simulatori non implementati in python.
Come input in questo esempio ho scelto l'attributo **pace**, che il simulatore vorrebbe conoscere ogni 5 secondi.
Come fatto per un simulatore capace di usare http/rest per inizializzarlo dobbiamo passargli come argomento una libreria di configurazione:


rest = {
    "address": "127.0.0.1:8000",		#questo è il server http a cui connettersi, in questo caso un server sulla stessa macchina
    "attrs": {					#questo è il dizionario che contiene le informazioni relative ad ogni attributo
        "pace": {				#ogni attributo indica:
            "GET": "/x.txt",			#	l'url a cui richiedere il dato,
            "timeout": "5"			#	il tempo tra una richiesta e l'altra
        }
    }
}


quindi il main di mosaik diventerà:

## World

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
buffer = world.start("Buffer",extra_attrs=["pace"], rest=rest)		#qui è dove passiamo rest e il vettore contenente i nomi degli attributi

# Instantiate models
model = examplesim.JModel()
agent = examplectrl.Agent.create(1)
monitor = collector.Monitor()
buffer = buffer.Buffer()

# Connect entities
world.connect(model, agent[0], ('queue', 'q_in'), async_requests=True)
world.connect(buffer, model, "pace")						#colleghiamo il buffer a tutti i simulatori che non possono usare http/rest
world.connect(model, monitor, 'queue', "pace", 'verso', async_requests=True)

# Run simulation
world.run(until=END,rt_factor=0.01)


Modifichiamo anche il simulatore in java per fargli gestire i nuovi dati di input. 
Oltre ad aggiungere vari metodi per settare e leggere **pace** dobbiamo modificare il metodo di gestione degli input.
I dati in arrivo dal buffer sono equivalenti a quelli in arrivo da ogni altro simulatore, il che semplifica la gestione dei dati.

## Step

public long step(long time, Map<String, Object> inputs) {
    	
    	String verso;
    	//go through entities in inputs
        for (Map.Entry<String, Object> entity : inputs.entrySet()) {
            //get attrs from entity
            Map<String, Object> attrs = (Map<String, Object>) entity.getValue();
            //go through attrs of the entity
            for (Map.Entry<String, Object> attr : attrs.entrySet()) {

                String attrName = attr.getKey();
                if (attrName.equals("verso")) {
                	...
			fa le stesse cose di prima
			...
                }
                if (attrName.equals("pace")) {										//sappiamo che il dato in input avrà questo nome (glielo abbiamo detto noi nella connect)
                    if (((Map<String, Object>)attr.getValue()).values().toArray()[0] == null);				//controlliamo che sia arrivato effettivamente un nuovo dato 
                    else {
                    	String val = (String) ((Map<String, Object>)attr.getValue()).values().toArray()[0];		//da qui è gestione del dato che è lasciata al programmatore; in questo istante val contiene la stringa ottenuta con la GET http (in questo caso Model_0:15)
                    	String eid = entity.getKey();
                    	if (val.split(":")[0].equals(eid)) {								//dato che stiamo ciclando sui vari modelli, con questo if controlliamo che il dato sia effettivamente per quel preciso modello (questa è UNA implementazione possibile, un dato potrebbe servire a tutti i modelli)
                    		int idx = this.entities.get(eid);
                    		this.simulator.set_pace(idx, Integer.parseInt(val.split(":")[1]));			//settiamo il valore di **pace** al valore arrivato in input 
                    	}
                    	
                    }
                }
            }
        }
        //call step-method
        this.simulator.step();

        return time + this.stepSize;
    }

A questo punto facciamo partire la simulazione:
Per prima cosa avviamo il server http, poi il simulatore (ho dimenticato di farlo notare ma il simulatore java è in **remoto**, 
quindi ovviamente questa versione di mosaik supporta la distribuzione), e infine il main di mosaik.

- pace: [1.0, 2.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, **16.0**, 1.0, 2.0, 1.0, 1.0, 2.0, 1.0, 2.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 2.0, 1.0, 1.0, **16.0**, 1.0, 1.0, 2.0, 1.0, 1.0, 2.0, 1.0, 1.0, **16.0**, 1.0, 1.0, 1.0, 1.0, 2.0, 1.0, 1.0, 2.0, 1.0, 1.0, 2.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, **16.0**, 1.0, 2.0, 3.0, 4.0, 1.0, 2.0, 3.0, 1.0, 1.0, 1.0, 1.0, 1.0, 2.0, 3.0, 1.0, 1.0, 2.0, 1.0, 1.0, 2.0, 3.0, 1.0, 1.0, 2.0, 1.0, 1.0, **16.0**, 1.0, 1.0, 2.0, 3.0, 4.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 2.0, 1.0, 1.0, 1.0, 2.0, 3.0, 1.0]
 
Ora a parte il fatto che i valori di **pace** sono rappresentati in float (perchè in java ho voluto considerarli tali), 
notiamo che ogni 5 secondi il valore subisce un incremento che non rispetta l'andamento abituale.
Questo significa che i messaggi tramite **http/rest** vengono ricevuti dal buffer e inoltrati correttamente al simulatore java
(il messaggio diceva "Model_0:15", in base all'attributo **verso** il 15 verrà o incrementato a 16 o riportato a 1, da qui il 
motivo per cui sembrano esserci dei "buchi" tra i vari 16)

## Buffer multi-uso

Ora immaginiamo di avere 2 simulatori in java e che ognuno dei due voglia leggere un dato rispettivamente ogni x e y secondi. 
Non c'è bisogno di creare due simulatori Buffer distinti, dato che uno solo può gestire molteplici richieste (**tutti i simulatori 
però devono avere lo stesso step size**, vedremo dopo il perchè).
Per facilità prendiamo lo stesso simulatore e creiamone 2 istanze, da ognuno dei quali creiamo 2 modelli distinti, per un totale di 4 modelli.
Supponiamo di voler che il primo chieda un dato ogni 4 secondi mentre il secondo ogni 7

Nell'init dovremo passare al Buffer:

 
rest = {
    "address": "127.0.0.1:8000",		
    "attrs": {					
        "pace1": {				
            "GET": "/x.txt",			
            "timeout": "4"			
        },
	"pace2": {				
            "GET": "/y.txt",			
            "timeout": "7"			
        }
    }
}

i contenuti dei file sono:

## x.txt

	Model_0:15


## y.txt

	Model_1:99

modifichiamo anche il main di mosaik

## World

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
END = 10 * 60  # 10 minutes

# Create World
world = mosaik.World(SIM_CONFIG)

rest = {
    "address": "127.0.0.1:8000",		#questo è il server http a cui connettersi, in questo caso un server sulla stessa 								macchina
    "attrs": {					        #questo è il dizionario che contiene le informazioni relative ad ogni attributo
        "pace1": {					        #ogni attributo indica:
            "GET": "/x.txt",			#	l'url a cui richiedere il dato,
            "timeout": "4"			    #	il tempo tra una richiesta e l'altra
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
world.run(until=END,rt_factor=0.025)


Ci siamo collegati a due simulatori, da ognuno dei quali abbiamo creato 2 modelli. Abbiamo poi creato due controllori, ognuno che si 
occupa di una coppia di modelli. Infine abbiamo connesso i vari modelli tra loro.
Facciamo partire i due simulatori e il main di mosaik.

- ExampleSim1-0.Model_0:
  - pace: [1.0, 2.0, 3.0, 1.0, 1.0, 2.0, 1.0, 1.0, 1.0, 1.0, 1.0, 2.0, **16.0**, 1.0, 1.0, 1.0, 1.0, 2.0, **16.0**, 1.0]

- ExampleSim1-0.Model_1:
  - pace: [1.0, 1.0, 2.0, 3.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 2.0, 1.0, 2.0, 1.0, 2.0, 1.0, 1.0, 1.0, 2.0, 3.0]

- ExampleSim2-0.Model_0:
  - pace: [1.0, 1.0, 2.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 2.0, 1.0, 2.0, 1.0, 1.0, 1.0]

- ExampleSim2-0.Model_1:
  - pace: [1.0, 1.0, 2.0, 1.0, 1.0, **100.0**, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 2.0, 1.0, 1.0, 1.0, 1.0, 2.0, 3.0, 1.0]
  
Dato il contenuto dei due file ci aspettavamo che solo il primo e l'ultimo modello subissero modifiche, e infatti è così.
Ora vediamo perchè per funzionare i simulatori e il buffer devono avere lo stesso step:

Immaginiamo che il buffer abbia uno step di 1 unità, mentre il simulatore di 2. Mosaik dopo ogni step chiede al buffer i dati da 
mandare al simulatore nello step corrente. Ricordiamo che per come abbiamo implemementato il buffer questo elimina i messaggi una 
volta inoltrati a mosaik. Ecco cosa potrebbe succedere:

Time 0  1  2  3  4  5  6  7  8  9  10
Buf  n  15 n  n  15 n  n  15 n  n  15  -> Mosaik

Questo è il comportamento che vogliamo dal buffer, ma cosa arriva effettivamente al simulatore?
Il simulatore chiederà il dato solo ogni 2 unità di tempo, quindi

Time 0  1  2  3  4  5  6  7  8  9  10
Buf  n  15 n  n  15 n  n  15 n  n  15
Sim  n     n     15    n     n     15

Perciò notiamo che perdiamo 2 dei 4 dati che invece avremmo voluto.
Il problema opposto si presenta invece se il simulatore ha uno step inferiore rispetto al buffer:

Time 0  1  2  3  4  5  6  7  8  9  10
Buf  n     15    n     15    n     15  -> Mosaik
Sim  n  n  15 15 n  n  15 15 n  n  15

Qui invece anzichè ricevere 3 volte il dato il simulatore lo riceve 5 volte, ed è impossibile stabilire quali siano quelli
autentici.
