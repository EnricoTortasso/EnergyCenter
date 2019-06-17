Esempio di base in Python, a cui però il simulatore principale è stato sostituito da uno in Java.

La difficoltà maggiore è quella di riuscire a far comunicare i due linguaggi 
(Java è più complesso da questo punto di vista, visto che ci vogliono dei cast espliciti per 
indicare il tipo di dato, cosa che in Python non serve). 
Per rendere più facile la comunicazione consiglio di scambiare solo dati numerici o stringhe 
(io in questi esempi ho scambiato un vettore, ma potevo bennissimo trattare i dati come 4 singoli 
numeri). Questo rende molto più facile gestire i dati una volta che questi arrivano in java, mentre 
dal lato python direi che non ci sono problemi. 

In realtà il problema principale è che java è un linguaggio fortemente tipizzato, mentre spesso 
i dizionari che python usa per mandare i dati attraverso mosaik hanno al loro interno tipi di dato 
diversi tra loro, che java ha difficoltà a riconoscere, da cui l'uso estensivo dei cast espliciti.

La simulazione è basata sull'esempio di base per la distribuzione su più macchine, perciò ne eredita
già la predisposizione alla distribuzione.

é anche presente un cattura di pacchetti effettuatta tramite wireshark:
Si nota che tutte le chiamate init, create, step, get_data e stop vengono usate e funzionano
correttamente.