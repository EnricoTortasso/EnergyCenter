package simulazione;

import java.util.Random;

class JModel {
    private float pace=1;
    private float[] queue = {0,0,0,0};
    private String verso ="ns";
    private String old_verso = "ew";

    public JModel() {
        this.pace=1 ;
    }

    public JModel(float initVal) {
        this.pace = initVal;
    }

    public String get_verso() {
        return this.verso;
    }
    
    public float[] get_queue() {
        return this.queue;
    }

    public void set_verso(String verso) {
        this.verso = verso;
    }
    
    public float get_pace() {
        return this.pace;
    }
    public void set_pace(int pace) {
        this.pace = pace;
    }

    public void step() {
        if (this.verso == "ns" ) {
            this.queue[0] -= this.pace;
            this.queue[1] -= this.pace;
        }
        else {
            this.queue[2] -= this.pace;
            this.queue[3] -= this.pace;
        }
        
        for (int i=0;i<4;i++)
            if  (this.queue[i] <0) 
                this.queue[i] = 0;
                
        for (int i =0; i<3;i++)
            this.queue[new Random().nextInt(4)] +=1;
            
            
        if (this.verso == this.old_verso )
            this.pace += 1;
        else 
            this.pace = 1;

        this.old_verso=this.verso;
    }
    
}