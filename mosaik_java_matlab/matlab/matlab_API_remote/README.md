Per prima cosa consiglio di guardare il README della versione precedente che spiega molto bene il funzionamento dell'API

API aggiornata, ora permetta la distribuzione su più macchine.
Il procedimento per la distribuzione consiste nell'avviare il simulatore matlab dando come argomento indirizzo ip e porta su cui 
ascoltare, avviare mosaik dopo aver inserito nel sim_config il metodo connect e l'indirizzo a cui collegarsi.

	'connect': '127.0.0.1:9999'

WARNING per come è implementato il server della libreria standard di matlab, questo può gestire una sola connessione alla volta.
Per questo motivo se si vogliono 2 istanze dello stesso simulatore con questa configuazione bisogna avviare due processi distinti.
