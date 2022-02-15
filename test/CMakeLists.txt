
add_executable(test test.cpp)
target_link_libraries(test example)
target_include_directories(test PUBLIC ${CMAKE_SOURCE_DIR}/src)