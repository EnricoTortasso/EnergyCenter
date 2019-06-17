Esempio di base in Python, a cui per� il simulatore principale � stato sostituito da uno in Java.

La difficolt� maggiore � quella di riuscire a far comunicare i due linguaggi 
(Java � pi� complesso da questo punto di vista, visto che ci vogliono dei cast espliciti per 
indicare il tipo di dato, cosa che in Python non serve). 
Per rendere pi� facile la comunicazione consiglio di scambiare solo dati numerici o stringhe 
(io in questi esempi ho scambiato un vettore, ma potevo bennissimo trattare i dati come 4 singoli 
numeri). Questo rende molto pi� facile gestire i dati una volta che questi arrivano in java, mentre 
dal lato python direi che non ci sono problemi. 

In realt� il problema principale � che java � un linguaggio fortemente tipizzato, mentre spesso 
i dizionari che python usa per mandare i dati attraverso mosaik hanno al loro interno tipi di dato 
diversi tra loro, che java ha difficolt� a riconoscere, da cui l'uso estensivo dei cast espliciti.

La simulazione � basata sull'esempio di base per la distribuzione su pi� macchine, perci� ne eredita
gi� la predisposizione alla distribuzione.

� anche presente un cattura di pacchetti effettuatta tramite wireshark:
Si nota che tutte le chiamate init, create, step, get_data e stop vengono usate e funzionano
correttamente.