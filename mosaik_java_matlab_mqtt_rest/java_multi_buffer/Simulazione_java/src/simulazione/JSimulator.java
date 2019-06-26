package simulazione;

import java.util.ArrayList;

class JSimulator {
    private final ArrayList<JModel> models;

    public JSimulator() {
    	this.models = new ArrayList<JModel>();
    	this.models.add(new JModel());
    }
    
    public void add_model(Number init_val) {
        JModel model;
        if (init_val == null) {
        	model = new JModel();
        } else {
        	model = new JModel(init_val.floatValue());
        }
        this.models.add(model);
    }
    
    public void step() {
    	for (int i = 0; i < this.models.size(); i++) {
    		JModel model = this.models.get(i);
    		model.step();
    	}	    		
    }
    
    public float[] get_queue(int idx) {
    	JModel model = this.models.get(idx);
    	return model.get_queue();
    }
    
    public String get_verso(int idx) {
    	JModel model = this.models.get(idx);
    	return model.get_verso();
    }
    
    public void set_verso(int idx, String verso) {
    	JModel model = this.models.get(idx);
    	model.set_verso(verso);
    }
    
    public void set_pace(int idx, int n) {
    	JModel model = this.models.get(idx);
    	model.set_pace(n);
    }
    
    public float get_pace(int idx) {
    	JModel model = this.models.get(idx);
    	return model.get_pace();
    }
    
}