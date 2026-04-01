cmake_minimum_required(VERSION 3.10)
project(OpenGLProject)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Шляхи до бібліотек
set(GLFW_DIR ${CMAKE_SOURCE_DIR}/libs/glfw)
set(GLAD_INCLUDE_DIR ${CMAKE_SOURCE_DIR}/libs/glad/include)
set(GLAD_SRC ${CMAKE_SOURCE_DIR}/libs/glad/src/glad.c)
set(GLM_INCLUDE_DIR ${CMAKE_SOURCE_DIR}/include)

# Пошук GLFW
find_path(GLFW_INCLUDE_DIR 
    NAMES GLFW/glfw3.h
    PATHS ${GLFW_DIR}/include
)

find_library(GLFW_LIBRARY
    NAMES glfw3
    PATHS ${GLFW_DIR}/lib
)

# Додавання GLAD
add_library(glad STATIC ${GLAD_SRC})
target_include_directories(glad PUBLIC ${GLAD_INCLUDE_DIR})

# Створення виконуваного файлу
add_executable(OpenGLProject src/main.cpp)

# Підключення бібліотек
target_include_directories(OpenGLProject PRIVATE
    ${GLFW_INCLUDE_DIR}
    ${GLAD_INCLUDE_DIR}
    ${GLM_INCLUDE_DIR}
)

target_link_libraries(OpenGLProject
    ${GLFW_LIBRARY}
    glad
)

# Для Windows
if(WIN32)
    target_link_libraries(OpenGLProject
        opengl32
    )
endif()