#include <thread>
#include <numeric>
#include <random>

#include "gtest/gtest.h"
#include "linked_list.hpp"

void worker(OrderedLinkedList* ll, std::vector<int>& numbers, size_t start, size_t end, size_t num_numbers) {
  std::random_device dev;
  std::mt19937 rng(dev());
  std::uniform_int_distribution<std::mt19937::result_type> rand_delete_pos(0, num_numbers);
  std::bernoulli_distribution rand_should_delete(0.2);

  for (size_t pos = start; pos < end; ++pos) {
    int key = numbers[pos];
    int value = key;
    ll->add(key, value);

    // Delete previously inserted key
    if (pos > start && rand_should_delete(rng)) {
      size_t delete_pos = start + (rand_delete_pos(rng) % (pos - start));
      int delete_key = numbers[delete_pos];
      if (delete_key != 0) {
        ll->remove(delete_key);
        numbers[delete_pos] = 0;
      }
    }
  }
}

TEST(ConcurrentOrderedLinkedListTests, WorkCorrectly) {
  const size_t THREADS = 8;
  const size_t NUM_ENTRIES = 50000;
  std::vector<int> numbers(NUM_ENTRIES);

  std::iota(numbers.begin(), numbers.end(), 1);
  std::shuffle(numbers.begin(), numbers.end(), std::random_device());

  OrderedLinkedList ll;
  std::vector<std::thread> threads;

  size_t numbers_per_thread = NUM_ENTRIES / THREADS;
  for (size_t i = 0; i < THREADS; i++) {
    size_t thread_start = i * numbers_per_thread;
    size_t thread_end = thread_start + numbers_per_thread;
    threads.emplace_back(worker, &ll, std::ref(numbers), thread_start, thread_end, NUM_ENTRIES);
  }

  for (auto& t : threads) { t.join(); }

  Node* curr_node = ll.getHead();

  // Sort again to check the results
  std::sort(numbers.begin(), numbers.end());

  for (int key : numbers) {
    // Key was deleted
    if (key == 0) { continue; }

    auto node = ll.find(key);
    EXPECT_EQ(node, curr_node);
    ASSERT_NE(node, nullptr);
    EXPECT_EQ(node->key, key);
    curr_node = curr_node->next_node;
  }
}

int main(int argc, char** argv) {
  ::testing::InitGoogleTest(&argc, argv);
  return RUN_ALL_TESTS();
}
