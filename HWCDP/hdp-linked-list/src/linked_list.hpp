#pragma once

#include "node.hpp"

/** Concurrent Ordered Linked List
 *
 * Elements must be inserted in ascending order, i.e., 1, 2, 3, .., N
 * Assume unique keys, there will be no duplicates. You do not need to handle those.
 * To pass advanced tests, it must be concurrent.
 */
class OrderedLinkedList {
 private:
  Node* head = nullptr;
  /** You may add variables here, if needed. */


 public:
  /*********************************************
   *            TO BE IMPLEMENTED              *
   *********************************************/
  OrderedLinkedList();
  ~OrderedLinkedList();

  void add(int key, int value);

  void remove(int key);

  Node* find(int key);

  /*********************************************
   *             DO NOT CHANGE!                *
   *********************************************/
  Node* getHead() { return head; };
};
