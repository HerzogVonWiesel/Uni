#include "gtest/gtest.h"

#include "linked_list.hpp"
#include "node.hpp"

TEST(OrderedLinkedListTests, AddOrdered) {
  OrderedLinkedList linkedList;
  linkedList.add(1, 1);
  linkedList.add(2, 2);
  linkedList.add(3, 3);
  linkedList.add(4, 4);

  Node* head = linkedList.getHead();

  ASSERT_NE(head, nullptr);
  EXPECT_EQ(head->key, 1);
  head = head->next_node;
  ASSERT_NE(head, nullptr);
  EXPECT_EQ(head->key, 2);
  head = head->next_node;
  ASSERT_NE(head, nullptr);
  EXPECT_EQ(head->key, 3);
  head = head->next_node;
  ASSERT_NE(head, nullptr);
  EXPECT_EQ(head->key, 4);
}

TEST(OrderedLinkedListTests, AddUnordered) {
  OrderedLinkedList linkedList;
  linkedList.add(4, 4);
  linkedList.add(2, 2);
  linkedList.add(1, 1);
  linkedList.add(3, 3);

  Node* head = linkedList.getHead();

  ASSERT_NE(head, nullptr);
  EXPECT_EQ(head->key, 1);
  head = head->next_node;
  ASSERT_NE(head, nullptr);
  EXPECT_EQ(head->key, 2);
  head = head->next_node;
  ASSERT_NE(head, nullptr);
  EXPECT_EQ(head->key, 3);
  head = head->next_node;
  ASSERT_NE(head, nullptr);
  EXPECT_EQ(head->key, 4);
}

TEST(OrderedLinkedListTests, FindSuccessfull) {
  OrderedLinkedList linkedList;
  linkedList.add(1, 1);
  linkedList.add(2, 2);
  linkedList.add(4, 4);
  linkedList.add(3, 3);

  auto foundMid = linkedList.find(3);
  ASSERT_NE(foundMid, nullptr);
  EXPECT_EQ(foundMid->key, 3);

  auto foundFront = linkedList.find(1);
  EXPECT_EQ(foundFront->key, 1);

  auto foundLast = linkedList.find(4);
  EXPECT_EQ(foundLast->key, 4);
}

TEST(OrderedLinkedListTests, FindUnuccessfull) {
  OrderedLinkedList linkedList;
  linkedList.add(1, 1);
  linkedList.add(2, 2);
  linkedList.add(4, 4);
  linkedList.add(3, 3);

  auto found = linkedList.find(4);
  ASSERT_NE(found, nullptr);

  auto notfound = linkedList.find(10);
  ASSERT_EQ(notfound, nullptr);
}

TEST(OrderedLinkedListTests, Delete) {
  OrderedLinkedList linkedList;
  linkedList.add(1, 1);
  linkedList.add(2, 2);
  linkedList.add(4, 4);
  linkedList.add(3, 3);

  linkedList.remove(3);

  Node* head = (linkedList.getHead());
  ASSERT_NE(head, nullptr);
  EXPECT_EQ(head->key, 1);
  head = head->next_node;
  EXPECT_EQ(head->key, 2);
  head = head->next_node;
  EXPECT_EQ(head->key, 4);
}

int main(int argc, char** argv) {
  ::testing::InitGoogleTest(&argc, argv);
  return RUN_ALL_TESTS();
}
