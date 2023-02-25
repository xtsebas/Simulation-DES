import random
import simpy
import statistics

def MemoryUse(env, name, time, RAM, CPU):
    global totalTime, total

    yield env.timeout(time)
    timeProcess = env.now

    timeNeeded = random.randint(1,10)
    ramNeeded = random.randint(1,10)

    print("The %s starts at %f and needs %d quantity of RAM" % (name, timeNeeded, ramNeeded))

    with CPU.request() as CPU_, RAM.put(ramNeeded) as RAM_:
        yield RAM_
        yield CPU_
        yield env.timeout(timeNeeded)
        print("The %s ended at %f" % (name, env.now))

    total = env.now - timeProcess
    print("The %s lasted %f units of time" % (name, total))
    totalTime += total
    Elapsed_times.append(total)




env = simpy.Environment()
RAM = simpy.Container(env, init=0, capacity=100)
CPU= simpy.Resource(env, capacity=1)
random.seed(10)

totalTime = 0
total=0
Elapsed_times=[]

for i in range(200):
    env.process(MemoryUse(env, "Process %s"%i, random.expovariate(1.0/5.0),RAM, CPU))

env.run(100)

standard_deviation = statistics.stdev(Elapsed_times)

print("The average time of the processes is: ", totalTime/25.0)
print("The standard deviation of the processes is: ", standard_deviation)

