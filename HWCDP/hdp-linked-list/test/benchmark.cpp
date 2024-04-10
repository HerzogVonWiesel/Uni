#include <numeric>
#include <random>
#include <vector>
#include <memory>
#include <chrono>
#include <iostream>

#include "benchmark/benchmark.h"
#include "linked_list.hpp"

constexpr size_t THREADS = 8;
constexpr size_t NUM_ENTRIES = 100000;
constexpr size_t SEED = 1337;
constexpr auto COUNTER_NAME = "duration_ms";

class LinkedListFixture : public benchmark::Fixture {
 public:
  void init() {
    numbers.resize(NUM_ENTRIES);
    std::iota(numbers.begin(), numbers.end(), 1);
    std::random_device dev;
    std::seed_seq seed{SEED};
    std::mt19937 rng(seed);
    std::shuffle(numbers.begin(), numbers.end(), rng);
    ll = std::make_unique<OrderedLinkedList>();
  }

  std::vector<int> numbers;
  std::unique_ptr<OrderedLinkedList> ll;
};

BENCHMARK_DEFINE_F(LinkedListFixture, LinkedListBenchmark)(benchmark::State& state) {
  std::random_device dev;
  std::seed_seq seed{SEED};
  std::mt19937 rng(seed);
  std::uniform_int_distribution<std::mt19937::result_type> rand_op_pos(0, NUM_ENTRIES);
  std::bernoulli_distribution rand_should_find(0.4);
  std::bernoulli_distribution rand_should_delete(0.2);

  const size_t numbers_per_thread = NUM_ENTRIES / THREADS;
  const size_t thread_start = state.thread_index() * numbers_per_thread;
  const size_t thread_end = thread_start + numbers_per_thread;

  if (state.thread_index() == 1) {
    init();
  }

  for (auto _: state) {
    const auto start_time = std::chrono::steady_clock::now();
    for (size_t pos = thread_start; pos < thread_end; ++pos) {
      int key = numbers[pos];
      int value = key;
      ll->add(key, value);

// Find previously inserted key
      if (pos > thread_start && rand_should_find(rng)) {
        size_t find_pos = thread_start + (rand_op_pos(rng) % (pos - thread_start));
        int find_key = numbers[find_pos];
        if (find_key != 0) {
          Node* node = ll->find(find_key);
          const bool valid = node != nullptr;
          if (!valid) {
            throw std::runtime_error("Did not find valid key!");
          }
        }
      }

// Delete previously inserted key
      if (pos > thread_start && rand_should_delete(rng)) {
        size_t delete_pos = thread_start + (rand_op_pos(rng) % (pos - thread_start));
        int delete_key = numbers[delete_pos];
        if (delete_key != 0) {
          ll->remove(delete_key);
          numbers[delete_pos] = 0;
        }
      }
    }
    const auto end_time = std::chrono::steady_clock::now();
    const auto duration = std::chrono::duration_cast<std::chrono::milliseconds>(end_time - start_time);
    state.counters[COUNTER_NAME] =
        benchmark::Counter(static_cast<double>(duration.count()), benchmark::Counter::kAvgThreads);
  }
}

BENCHMARK_REGISTER_F(LinkedListFixture, LinkedListBenchmark)
    ->Threads(THREADS)
    ->Iterations(1)  // We want only one iteration per run ...
    ->Repetitions(3) // ... but multiple runs.
    ->Unit(benchmark::kMillisecond)
    ->UseRealTime();


int main(int argc, char** argv) {
  benchmark::Initialize(&argc, argv);
  if (benchmark::ReportUnrecognizedArguments(argc, argv)) return 1;
  benchmark::RunSpecifiedBenchmarks();

  benchmark::Shutdown();
  return 0;
}
