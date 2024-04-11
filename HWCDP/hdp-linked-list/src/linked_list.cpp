#include "linked_list.hpp"

/**
 * You need the implement the methods in this class according to the task description.
 */

OrderedLinkedList::OrderedLinkedList() {
    // head = new Node(-1,-1);
}

OrderedLinkedList::~OrderedLinkedList() {
    Node* current = head;
    while (current != nullptr) {
        Node* next = current->next_node;
        delete current;
        current = next;
    }
    head = nullptr;
}

void OrderedLinkedList::add(int key, int value) {
    if (head == nullptr) {
        head = new Node(key, value);
        return;
    }
    Node* current = head;
    Node* prev = nullptr;
    while (current != nullptr && current->key < key) {
        prev = current;
        current = current->next_node;
    }
    if (prev == nullptr) {
        head = new Node(key, value);
        head->next_node = current;
    } else {
        prev->next_node = new Node(key, value);
        prev->next_node->next_node = current;
    }

}

void OrderedLinkedList::remove(int key) {
    Node* current = head;
    Node* prev = nullptr;
    while (current != nullptr && current->key != key) {
        prev = current;
        current = current->next_node;
    }
    if (current == nullptr) {
        return;
    }
    if (prev == nullptr) {
        head = current->next_node;
    } else {
        prev->next_node = current->next_node;
    }
    delete current;
}

Node* OrderedLinkedList::find(int key) {
    Node* current = head;
    while (current != nullptr && current->key != key) {
        current = current->next_node;
    }
    return current;
 }
