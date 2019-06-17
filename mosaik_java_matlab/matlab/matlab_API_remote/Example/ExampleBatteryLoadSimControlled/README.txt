Purtroppo per come è fatto socket in matlab non è possibile avviare due istanze dello stesso simulatore, perchè il socket non risponde
a più di un SYN, quindi permette una singola connessione. Si può però avviare più volte lo stesso simulatore e da mosaik creare un'istanza
per simulatore.