This is a collection of different variations of the Mosaik core build, along with examples to understand their possibilities and limits

All this material is just a personal modification of Mosaik. The original version can be found at https://mosaik.readthedocs.io/en/latest/

In the following examples we will mostly use the same 3 simulators: a traffic light simulator, a controller and a collector of data.

The traffic light simulator: this simulator can create many models of traffic lights, each with their own attributes. The attributes for each 
model are a "queue" for each direction (N, S, E, W) merged into an array, a "verso" that shows which queues are allowed to move in the 
crossroad  and a "pace" that is the number of cars that can exit their queue during a step.

during a step a random number of cars arrives in each queue and "pace" cars exit their queues according to "verso" value. if the "verso" value
remain constant in 2 successive steps the value of "pace" is increased by 1, else it is set to 1.

The controller: this simulator can create models of Agents, each capable of coontrolling one or more traffic lights. An Agent receive the queue
of the traffic light(s) he is controlling, check which direction contains the highest number of cars and send a command to the simulator 
setting the "verso" value for the next step.

The controller: this simulator just receive all data from the traffic lights simulator and store them in cronological order until the end of the
simulation, when he will print them.

