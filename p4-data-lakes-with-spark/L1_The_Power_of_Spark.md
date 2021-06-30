# The Power of Spark

Spark is currently one of the most popular tools for big data analytics. Hadoop is a slightly older technology although still in use by some companies. Spark is generally faster than Hadoop, which is why Spark has become more popular over the last few years.

- [x] What is big data?
- [x] Hardware behind big data
- [ ] Introduction to distributed systems
- [ ] Brief history of Spark and big data
- [ ] Common Spark use cases
- [ ] Other technologies in the big data ecosystem

## What is Big Data?

- CPU: **Fastest**. *The "brain" of the computer*. Every process on your computer is eventually handled by your CPU. This includes calculations and also instructions for the other components of the compute.
- Memory (RAM): **2nd Fastest**. *Short-term, quick data storage*. When your program runs, data gets temporarily stored in memory before getting sent to the CPU. Memory is _ephemeral_ storage - when your computer shuts down, the data in the memory is lost.
- Solid State Drive (SSD): **3rd Fastest**. *Long-term, safe data storage*. Storage is used for keeping data over long periods of time. When a program runs, the CPU will direct the memory to temporarily load data from long-term storage.
- Network: **Slowest**. *Connection between computers*. Network is the gateway for anything that you need that isn't stored on your computer. The network could connect to other computers in the same room (a Local Area Network) or to a computer on the other side of the world, connected over the internet.

## Hardware

### CPU

The CPU is the brains of a computer. The CPU has a few different functions including directing other components of a computer as well as running mathematical calculations. The CPU can also store small amounts of data inside itself in what are called  **registers**. These registers hold data that the CPU is working with at the moment.

For example, say you write a program that reads in a 40 MB data file and then analyzes the file. When you execute the code, the instructions are loaded into the CPU. The CPU then instructs the computer to take the 40 MB from disk and store the data in memory (RAM). If you want to sum a column of data, then the CPU will essentially take two numbers at a time and sum them together. The accumulation of the sum needs to be stored somewhere while the CPU grabs the next number.

This cumulative sum will be stored in a register. The registers make computations more efficient: the registers avoid having to send data unnecessarily back and forth between memory (RAM) and the CPU.

**A 2.5 Gigahertz CPU means** that the CPU processes 2.5 billion operations per second. Let's say that for each operation, the CPU processes 8 bytes of data. How many bytes could this CPU process per second?
2.5e9 (opers/sec) * 8 (bytes/oper) = 20e9 (bytes/sec)

### Memory

It seems like the right combination of CPU and memory can help you quickly load and process data. We could build a single computer with lots of CPUs and a ton of memory. The computer would be incredibly fast.

What are the potential trade offs of creating one computer with a lots of CPUs and memory?

It's true that you could build a computer with a ton of CPU and memory, which is effectively a supercomputer. However, this approach has its downsides.

Beyond the fact that memory is expensive and ephemeral, we'll learn that for most use cases in the industry, memory and CPU aren't the bottleneck. Instead the storage and network slow down many tasks you'll work on in the industry.

### Storage

While long-term storage is cheap and durable, it's much slower than memory. Loading data from SSD can be about 15 times slower.

### Network

The biggest bottleneck when working with big data is transferring data across a network.

For example, the same hour of tweets that would take half a second to process from storage, would take 30 seconds to download from the Twitter API on a typical network.

Network speeds depend on a lot of factors, but it usually takes at least 20 times longer to process data, when you have to download it from another machine first.

For this reason, distributed systems try to minimize shuffling data back and forth across different computers. Minimizing network input and output is crucial to mastering Spark programming.

### Key Ratios

- CPU: 200x faster than memory
- Memory: 15x faster than SSD
- SSD: 20x faster than network.