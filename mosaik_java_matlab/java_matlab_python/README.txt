Questo � un esempio che collega un simulatore in java a un controllore in python e a un collettore in matlab.
Lo scopo � quello di dimostrare la funzionalit� e l'interoperabilit� della piattaforma mosaik.
Il simulatore e il controllore sono gli stess dell'esempio java, mentre il collettore deriva dall'esempio
matlab. � bastato cambiare nella sim_config di mosaik il metodo di collegamento al collettore per far funzionare
la simulazione.

SIM_CONFIG = {
    'ExampleSim': {
        'connect': '127.0.0.1:9999'    #java
    },
    'ExampleCtrl': {
        'python': 'controller:Controller'  #python
    },
    'Collector': {
        'connect': '127.0.0.1:9998'	#matlab
    }
}

Il fatto che sia stato cos� semplice � un ottimo segno, perch� significa che sono davvero riuscito ad aggiustare le varie
API in modo che tutto funzioni correttamente. Il vantaggio della piattaforma mosaik � che tutti i dati passano attraverso
il corpo principale della simulazione, che � scritto in python, quindi una volta realizzate delle API funzionanti non bisogna
pi� preocuparsi dell'interazione tra i vari linguaggi (es non c'� il problema di come far parlare matlab con java perch� i
loro dati passano attraverso python che sa come riceverli e come mandarli in formato adatto al linguaggio di destinazione).