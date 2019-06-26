# Esempio di comunicazione Java-Python

## Considerazioni
La difficoltà maggiore è quella di riuscire a far comunicare i due linguaggi 
(Java è più complesso da questo punto di vista, visto che ci vogliono dei cast espliciti per 
indicare il tipo di dato, cosa che in Python non serve). 
Per rendere più facile la comunicazione consiglio di scambiare solo dati numerici o stringhe 
(io in questi esempi ho scambiato un vettore, ma potevo benissimo trattare i dati come 4 singoli 
numeri). Questo rende molto più facile gestire i dati una volta che questi arrivano in java, mentre 
dal lato python direi che non ci sono problemi. 

In realtà il problema principale è che java è un linguaggio fortemente tipizzato, mentre spesso 
i dizionari che python usa per mandare i dati attraverso mosaik hanno al loro interno tipi di dato 
diversi tra loro, che java ha difficoltà a riconoscere, da cui l'uso estensivo dei cast espliciti.

é anche presente un cattura di pacchetti effettuatta tramite wireshark:
Si nota che tutte le chiamate init, create, step, get_data e stop vengono usate e funzionano
correttamente.

I due file .jar all'interno di Simulazione_java sono quelli che contengono tutte le funzioni e le utilities 
dell'API per java, quindi vanno inserite nei progetti dei simulatori che si vogliono collegare a mosaik.
Possono anche essere trovati qui https://bitbucket.org/mosaik/mosaik-api-java/src/master/


Per eseguire la simulazione avviare il simulatore java dando come parametri "127.0.0.1:9999 server" e 
il collettore in python con parametri "127.0.0.1:9998 -r". I dati raccolti verranno stampati dal 
collettore al termine della simulazione

# Creazione di un simulatore in java

il simulatore deve estendere la classe **Simulator** fornita da Mosaik,

  public class JExampleSim extends Simulator {
  ...

deve possedere un proprio **dizionario di configurazione**,

  private static final JSONObject meta = (JSONObject) JSONValue.parse(("{"
              + "    'api_version': " + Simulator.API_VERSION + ","
              + "    'models': {"
              + "        'JModel': {" 
              + "            'public': true,"
              + "            'params': ['init_val'],"
              + "            'attrs': ['queue', 'pace', 'verso']" 
              + "        }"
              + "    }" 
              + "}").replace("'", "\""));
              
 il suo **costruttore** deve richiamare quello del genitore,
 
  public JExampleSim() {
        super("JExampleSim");
        ...
    }
              
deve possedere un metodo **init**,

 public Map<String, Object> init(String sid, Map<String, Object> simParams) {
    	...                                                                          //simParams associa a una stringa un oggetto di qualunque tipo (intero, stringa, vettore, dizionario), sono i \*\*kwargs di python
    }
    
un metodo **create**,

  public List<Map<String, Object>> create(int num, String model, Map<String, Object> modelParams) {
        JSONArray entities = new JSONArray();
        ...
        for (int i = 0; i < num; i++) {
            ...
            }
            JSONObject entity = new JSONObject();
            entity.put("eid", eid);
            entity.put("type", model);
            entity.put("rel", new JSONArray());
            entities.add(entity);
            ...
        }
        ...
        return entities;
    }
              
un metodo **step**,

  public long step(long time, Map<String, Object> inputs) {
    	//go through entities in inputs
        for (Map.Entry<String, Object> entity : inputs.entrySet()) {
            //get attrs from entity
            Map<String, Object> attrs = (Map<String, Object>) entity.getValue();
            //go through attrs of the entity
            for (Map.Entry<String, Object> attr : attrs.entrySet()) 
                String attrName = attr.getKey();
                if (attrName.equals("<attributo>")) {
                    ...                                                            //qui attr.values() è una collezione di coppie (agente:valore), usarle di conseguenza
                    }
                    ...
                }
            }
        }
        ...
    return time + this.stepSize;
  }
  
e un metodo **get_data**.
  
public Map<String, Object> getData(Map<String, List<String>> outputs) {
        Map<String, Object> data = new HashMap<String, Object>();
        //*outputs* lists the models and the output values that are requested
        //go through entities in outputs
        for (Map.Entry<String, List<String>> entity : outputs.entrySet()) {
            String eid = entity.getKey();
            List<String> attrs = entity.getValue();
            HashMap<String, Object> values = new HashMap<String, Object>();
            ...
            //go through attrs of the entity
            for (String attr : attrs) {
                if (attr.equals("<attributo>")) {
                	values.put(attr, <qualunque dato in qualunque formato>);
                }
                else if (attr.equals("<un altro attributo>")) {
                	values.put(attr, <qualunque dato in qualunque formato>);
                }
            }
            data.put(eid, values);
        }
        return data;
  }
  
Infine aggiungiamo un **main**:

  public static void main(String[] args) throws Throwable {
          Simulator sim = new JExampleSim();
          //TODO: Implement command line arguments parser (http://commons.apache.org/proper/commons-cli/)
          if (args.length < 1) {
            String ipaddr[] = {"127.0.0.1:5678"};
            SimProcess.startSimulation(ipaddr, sim);
          }
          else {
            SimProcess.startSimulation(args, sim);
          }     
      }//main
