cmake_minimum_required(VERSION 3.12)
project(TakeSharedMemoryPhoto)


set(CMAKE_CXX_STANDARD 11)


add_executable(takephoto
src/main.cpp
)

set_target_properties(takephoto PROPERTIES
RUNTIME_OUTPUT_DIRECTORY ../)

target_include_directories(takephoto PRIVATE
/usr/include/gphoto2,
/usr/include/libexif,
)

target_link_libraries(takephoto PRIVATE
/usr/lib/aarch64-linux-gnu/libgphoto2.so
rt
/usr/lib/aarch64-linux-gnu/libcurl.so.4
)
