add_subdirectory(libs)

if (NOT LIBRARY_ONLY)
    add_executable(lab1 lab1/main.cpp)
    add_executable(lab2 lab2/main.cpp)
    # target_link_libraries(lab1 alg)
endif()