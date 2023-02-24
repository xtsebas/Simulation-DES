import random
import simpy

def MemoryUse(env, name, time, RAM, CPU):
    print("")


env = simpy.Environment()
RAM = simpy.Container(env, init=0, capacity=100)
CPU= simpy.Resource(env, capacity=1)
random.seed(10)

for i in range(25):
    env.process(MemoryUse(env, "Process %s"%i, random.randint(1,10),RAM, CPU))
env.run(until=100)
