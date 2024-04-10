# HDP - Concurrent Ordered Linked List

This is the starter task for our Hardware-Conscious Data Processing course.
It is meant for you to see if you are comfortable writing C++ at the level needed for the course.
The idea is to also think about concurrency and how to write efficient code, as this is the basis for the course.
If you are really struggling with this task, the course might not be for you at the moment.
We will aid with programming here and there, but we will not teach basic C++ concepts.
However, we will introduce some more advanced concepts where required as part of the course.

## Task

You should build a concurrent linked list that stores its entries in ascending order.
If you insert the records `2, 1, 4, 3`, you should store them as `1 --> 2 --> 3 --> 4`.
The interface is given in `linked_list.hpp` and you should implement the methods in `linked_list.cpp`.
You may add variables to the header file if you need them.
The `node.hpp` file contains the basic node structure that you will use to store the data. 
Do *not* modify this file.

## Setup

The project is a basic CMake project.
You can either include this in your IDE, e.g., CLion (is free for students) or VSCode (also free).
Or you can build it manually, if you write code in Vim.
But in that case you probably know how to build a project anyway.

```shell
mkdir build && cd build
cmake ..
make -j4
```

## Tests
For our tests, we use Google's test framework [googletest](https://github.com/google/googletest).
There are basic and advanced tests (similar to the structure in the course).
The basic tests (`basic.cpp`) will check for single-threaded correctness on small examples.
The advanced tests (`advanced.cpp`) run a larger test with multiple concurrent threads.
The executables are `./basic_test` and `./advanced_test`.
The basic tess should pass immediately, while the advanced test may run for a bit (anywhere between 5 and 30 seconds).

## Benchmarks
For our benchmarks, we use Google's [benchmark framework](https://github.com/google/benchmark).
This is the style of benchmarks we will be running throughout the course.
To run the benchmark, execute `./hdp_benchmark`.
This might run for a while (up to one or two minutes).
Feel free to play around with this if you like.
