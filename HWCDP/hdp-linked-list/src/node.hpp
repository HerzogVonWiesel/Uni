#pragma once

/**
 * This is the basic structure that holds values in your linked list. For this task, it is enough to support only
 * integer keys and values. In a more realistic setup, this would be templated to allow custom types.
 *
 * DO NOT CHANGE THIS FILE!
 */
struct Node {
  int key;
  int value;
  Node* next_node = nullptr;

  Node() {};
  Node(int k, int v) : key(k), value(v) {};
};

