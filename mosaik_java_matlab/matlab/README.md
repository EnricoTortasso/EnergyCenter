I take no credit for this work: I downloaded it from https://github.com/hesstobi/matlab-mosaik-toolbox.
I updated it to make it work with recent versions of mosaik and matlab.

Unfortunately this build is today (june 2019) 3 years old. Matlab and Mosaik have changed a lot in this period so i was expecting some 
problems.
This build relies on a (community-made i think) library called JSONlab, which can transform data in JSON and vice versa. This library was 
causing some problems in the code, so i switched to recently introduced matlab built-in functions jsonencode and jsondecode.

First of all a big WARNING (now resolved, look for matlab_API_remote) about using matlab with this configuration: as for now it only works 
if launched by python (same machine), but I think it shouldn't be a problem to make it work in remote control. 

Also for how matlab works and this API was implemented the SIM_ID of a simulator in python will be something like sim-0.model_0, 
while in matlab it will be something like sim_0_model_0 (there are some problems with "." in names in matlab and the functions that 
manage JSON). 
I already made the communication more stable by assuring that even if they call their simulators in different ways, mosaik and matlab 
still know who they are talking about.

How to build a mosaik compatible simulator in matlab:
  
  In first place our simulator must be a subclass ( i don't know if matlab call that in this way) of the ModelSimulator class.
  
    classdef ExampleSim < MosaikAPI.ModelSimulator
    
  
  Our simulator must have in its properties the name of its own models:
    
    properties
      providedModels = {'ExModel'}	
    end
	  

  The constructor method should be like this:
  
    function this = ExampleSim(varargin)
      this = this@MosaikAPI.ModelSimulator(varargin{:});
    end
    
  
  Ok the core body of our simulator is complete. You can add as many other functions as you want.
  
Our simulator now needs the model that we put in its properties.
This is how a model in matlab should be built to be used:
  It must me a subclass of the Model class:
  
    classdef ExModel < MosaikAPI.Model
    
    
  It must contain its public data in its properties:
  
    properties
      delta = 1	
      val			
    end
    
    
  Its constructor should call its parent's:
  
    function this = ExampleSim(varargin)
	this = this@MosaikAPI.ModelSimulator(varargin{:});
    end
    
    
  And it must implement at least a step():
  
    function step(this,~,varargin)
      this.val = this.val + this.delta; 
    end
  
  And a meta():
    
    function value = meta()
      value.public = true;
      value.attrs = {'delta', 'val'};
      value.params = {'init_value'};
      value.any_inputs = false;
    end
    
  
You can find more detailed info on the original page of the API implementation. Even if i had to change something to make it work, the 
main concepts and classes didn't change, as their properties.
