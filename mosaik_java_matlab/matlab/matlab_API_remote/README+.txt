API aggiornata, ora permetta la distribuzione su pi� macchine.
Il procedimento per la distribuzione consiste nell'avviare il simulatore matlab dando come argomento indirizzo ip e porta su cui 
ascoltare, avviare mosaik dopo aver inserito nel sim_config il metodo connect e l'indirizzo a cui collegarsi.

	'connect': '127.0.0.1:9999'

WARNING per come � implementato il server della libreria standard di matlab, questo pu� gestire una sola connessione alla volta.
Per questo motivo se si vogliono 2 istanze dello stesso simulatore con questa configuazione bisogna avviare due processi distinti.
