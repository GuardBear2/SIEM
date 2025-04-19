cmake_minimum_required(VERSION 3.12.4)

project(guardbear-keystore_tool)

add_executable(${PROJECT_NAME} main.cpp)
target_link_libraries(${PROJECT_NAME} PRIVATE keystore OpenSSL::SSL OpenSSL::Crypto base)
