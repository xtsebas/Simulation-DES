import random
import simpy
import statistics


def MemoryUse(env, name, time, RAM, ramQty, number_Instructions, velocity):
    global totalTime, total

    # Prints the quantity needed for the process
    yield env.timeout(time)
    print("The %s needs %d quantity of RAM" % (name, ramQty))
    total = env.now

    # Obtain the actual ram space
    yield RAM.get(ramQty)
    print("The %s can use the: %d of RAM needed." % (name, ramQty))

    neeededInstructions = 0

    # Still uses a complete clock cycle to run all the instructions of the process even if they are less than the
    # stablished number of instructions
    while neeededInstructions < number_Instructions:
        with CPU.request() as cpuRequest:
            yield cpuRequest

            # Calculates the number of instructions the CPU will do per clock cycle for the process
            if (number_Instructions - neeededInstructions) >= velocity:
                new_velocity = velocity

            else:
                new_velocity = (number_Instructions - neeededInstructions)

            print("The %s will do %d instructions in the CPU." % (name, new_velocity))
            yield env.timeout(new_velocity / velocity)

            neeededInstructions += new_velocity
            print("The %s has completed %d of %f instructions" % (name, neeededInstructions, number_Instructions))

        waiting_or_ready = random.randint(1, 2)

        #Pending to code the waiting list with a new CPU


env = simpy.Environment()
RAM = simpy.Container(env, init=100, capacity=100)
CPU = simpy.Resource(env, capacity=1)
Wait = simpy.Resource(env, capacity=1)
random.seed(10)

totalTime = 0
elapsed_times = []

for i in range(25):
    ramQty = random.randint(1, 10)
    number_Instructions = random.randint(1, 10)
    env.process(MemoryUse(env, "Process %s" % i , random.expovariate(1.0 / 5.0), RAM, ramQty, number_Instructions, 3))

env.run()
standard_deviation = statistics.stdev(elapsed_times)

print("The average time of the processes is: ", totalTime / 25.0)
print("The standard deviation of the processes is: ", standard_deviation)
