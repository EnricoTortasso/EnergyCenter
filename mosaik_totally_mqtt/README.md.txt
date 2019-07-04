# Mosaik MQTT 

Questa � una versione di mosaik che utilizza per lo scambio di messaggi con i simulatori solo il protocollo MQTT.

## Far funzionare lo scenario d'esempio

Prima di chiarire come funziona questa versione consiglio di provare a far funzionare l'esempio relativo.
Per prima cosa sostituire i file nella cartella "mosaik_changed_files" a quelli originali di mosaik.
A questo punto si pu� avviare il file "sensor.py" che in questo caso ha il solo scopo di avviare i 3 simulatori.
Infine avviare il file mondo.py per iniziare la simulazione.

Consiglio di osservare tramite un programma di sniffing lo scambio di dati, per comprendere appieno in che modo viene 
usato mqtt.

# Protocollo
## Init

Quando un simulatore viene avviato gli viene dato un indirizzo IP e una porta su cui ricevere i messaggi in arrivo. 
Poich� in questo momento della simulazione non possiede ancora un nome, che verr� fornito da Mosaik, il simulatore
si iscrive al topic <indirizzo_IP>:<PORT>. Su questo topic Mosaik mander� la richiesta di init, fornendo anche il nome
che identificher� univocamente il simulatore per la durata della simulazione. A questo punto il simulatore si iscrive 
al topic corrispondente al proprio nome, su quale ricever� tutte le istruzioni da parte di mosaik.

## Step

Step e get_data sono i due metodi pi� usati di mosaik, e il loro protocollo di scambio di messaggi con i simulatori � 
quasi identico. Vediamo in particolare il metodo step:

mosaik ->     "<Simulator_ID>/in/step"    "[<starting_step_time>, <inputs>]"
mosaik blocca il semaforo del simulatore corrente
mosaik aspetta il semaforo
...
simulator riceve il messaggio
	...
simulator esegue step()
	...
simulator ->  "<Simulator_ID>/out/step"   "<next_time>"
...
mosaik riceve il messaggio
	...
l'handler dei messaggi sblocca il semaforo del simulatore corrente
	...
mosaik riprende l'esecuzione


� da notare nel file controller.py come vengono gestiti i loop in questa nuova versione di mosaik. Nella versione originale
si effettua una chiamata asincrona che va a modificare gli input per il prossimo step del simulatore voluto attraverso il
metodo set_data. In questa versione, poch� � stata alterata leggermente la struttura di mosaik, non � pi� possibile fare cos�.
Al posto di invocare un metodo di mosaik ci limitiamo a inviare un messaggio tramite MQTT
	
	self.client.publish("/".join(model_eid.split(".")) +"/" + agent_eid +"/verso",verso)

dove model_eid � il nome univoco dell'entit�, agent_eid � il nome dell'agente che sta effettuando il set_data e "/verso" indica 
che vogliamo modificare il valore della variabile verso.


## Fake Proxy

Per rendere possibile lo scambio di dati attraverso MQTT ho definito una nuova classe fake_proxy in simmanager.py, il cui unico 
scopo � quello di far finta di essere un proxy di Mosaik, mentre in realt� comunica con MQTT.