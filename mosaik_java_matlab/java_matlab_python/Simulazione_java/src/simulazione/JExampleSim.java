package simulazione;


import java.util.HashMap;
import java.util.List;
import java.util.Map;

import org.json.simple.*;
import de.offis.mosaik.api.*;


public class JExampleSim extends Simulator {

    private int stepSize = 60;
    private int idCounter = 0;
    private final JSimulator simulator;
    private String eid_prefix = "JExampleModel_";
    private final Map<String, Integer> entities;

    // Alternatively, put all the JSON into a .json file and read meta data from there
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

    public JExampleSim() {
        super("JExampleSim");
        simulator = new JSimulator();
        entities = new HashMap<String, Integer>(); //Maps entity-ID to indices in JSimulator
    }

    @SuppressWarnings("unchecked")
    @Override
    public Map<String, Object> init(String sid, Map<String, Object> simParams) {
    	if (simParams.containsKey("eid_prefix")) {
    		this.eid_prefix = simParams.get("eid_prefix").toString();
    	}
        return JExampleSim.meta;
    }

    @SuppressWarnings("unchecked")
    @Override
    public List<Map<String, Object>> create(int num, String model, 
    		Map<String, Object> modelParams) {
        JSONArray entities = new JSONArray();
        for (int i = 0; i < num; i++) {
            String eid = this.eid_prefix + (this.idCounter + i);
            if (modelParams.containsKey("init_val")) {
                Number init_val = (Number) modelParams.get("init_val");
                this.simulator.add_model(init_val);
            }
            JSONObject entity = new JSONObject();
            entity.put("eid", eid);
            entity.put("type", model);
            entity.put("rel", new JSONArray());
            entities.add(entity);
            this.entities.put(eid, this.idCounter + i);
        }
        this.idCounter += num;
        return entities;
    }

    @SuppressWarnings("unchecked")
    @Override
    public long step(long time, Map<String, Object> inputs) {
    	
    	String verso;
    	//go through entities in inputs
        for (Map.Entry<String, Object> entity : inputs.entrySet()) {
            //get attrs from entity
            Map<String, Object> attrs = (Map<String, Object>) entity.getValue();
            //go through attrs of the entity
            for (Map.Entry<String, Object> attr : attrs.entrySet()) {
            	//check if there is a new delta
                String attrName = attr.getKey();
                if (attrName.equals("verso")) {
                    //sum up deltas from different sources
                    Object[] values = ((Map<String, Object>) attr.getValue()).values().toArray();
                    float ns = 0;
                    float ew =0 ;
                    for (int i = 0; i < values.length; i++) {
                    	String str =(String) values[i];
                    	if (str.compareTo("ns")==0)
                    		ns++;
                    	else
                    		ew++;
                    }
                    verso="ew";
                    if (ns>ew)
                        verso="ns";
                    //set verso
                    String eid = entity.getKey();
                    int idx = this.entities.get(eid);
                    this.simulator.set_verso(idx, verso);
                }
            }
        }
        //call step-method
        this.simulator.step();

        return time + this.stepSize;
    }

    @Override
    public Map<String, Object> getData(Map<String, List<String>> outputs) {
        Map<String, Object> data = new HashMap<String, Object>();
        //*outputs* lists the models and the output values that are requested
        //go through entities in outputs
        for (Map.Entry<String, List<String>> entity : outputs.entrySet()) {
            String eid = entity.getKey();
            List<String> attrs = entity.getValue();
            HashMap<String, Object> values = new HashMap<String, Object>();
            int idx = this.entities.get(eid);
            //go through attrs of the entity
            for (String attr : attrs) {
                if (attr.equals("queue")) {
                	float[] q=this.simulator.get_queue(idx);
                	String str = (int) q[0]+","+(int) q[1]+","+(int) q[2]+"," + (int)q[3];
                	values.put(attr, str);
                }
                else if (attr.equals("verso")) {
                	values.put(attr, this.simulator.get_verso(idx));
                }
            }
            data.put(eid, values);
        }
        return data;
    }

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
}//JExampleSim

