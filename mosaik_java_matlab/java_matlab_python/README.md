Questo è un esempio che collega un simulatore in java a un controllore in python e a un collettore in matlab.
Lo scopo è quello di dimostrare la funzionalità e l'interoperabilità della piattaforma mosaik.
Il simulatore e il controllore sono gli stessi dell'esempio java, mentre il collettore deriva dall'esempio
matlab. è bastato cambiare nella sim_config di mosaik il metodo di collegamento al collettore per far funzionare
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

Il fatto che sia stato così semplice è un ottimo segno, perchè significa che le varie API comunicano correttamente e non vengono ostacolate dalla differenza di linguaggio. Il vantaggio della piattaforma mosaik è che tutti i dati passano attraverso
il corpo principale della simulazione, che è scritto in python, quindi una volta realizzate delle API funzionanti non bisogna
più preocuparsi dell'interazione tra i vari linguaggi (es non c'è il problema di come far parlare matlab con java perchè i
loro dati passano attraverso python che sa come riceverli e come mandarli in formato adatto al linguaggio di destinazione).
