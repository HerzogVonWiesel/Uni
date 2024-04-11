# CMake generated Testfile for 
# Source directory: /mnt/c/Uni_Master/HWCDP/hdp-linked-list
# Build directory: /mnt/c/Uni_Master/HWCDP/hdp-linked-list
# 
# This file includes the relevant testing commands required for 
# testing this directory and lists subdirectories to be tested as well.
add_test(basic_test "basic_test")
set_tests_properties(basic_test PROPERTIES  _BACKTRACE_TRIPLES "/mnt/c/Uni_Master/HWCDP/hdp-linked-list/CMakeLists.txt;49;add_test;/mnt/c/Uni_Master/HWCDP/hdp-linked-list/CMakeLists.txt;0;")
add_test(advanced_test "advanced_test")
set_tests_properties(advanced_test PROPERTIES  _BACKTRACE_TRIPLES "/mnt/c/Uni_Master/HWCDP/hdp-linked-list/CMakeLists.txt;56;add_test;/mnt/c/Uni_Master/HWCDP/hdp-linked-list/CMakeLists.txt;0;")
subdirs("_deps/googletest-build")
subdirs("_deps/google_benchmark-build")
