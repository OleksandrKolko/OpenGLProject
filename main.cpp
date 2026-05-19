#include <glad/glad.h>
#include <GLFW/glfw3.h>
#include <glm/glm.hpp>
#include <glm/gtc/matrix_transform.hpp>
#include <glm/gtc/type_ptr.hpp>
#include <iostream>
#include <chrono>
#include <thread>

#define STB_IMAGE_IMPLEMENTATION
#include "stb_image.h"

const unsigned int SCR_WIDTH = 800;
const unsigned int SCR_HEIGHT = 600;

float rotationAngle = 0.0f;
bool isAnimating = true;
float lastTime = 0.0f;

void limitFPS(float targetFPS) {
    static auto lastFrameTime = std::chrono::steady_clock::now();
    float frameDuration = 1.0f / targetFPS;
    auto currentTime = std::chrono::steady_clock::now();
    float delta = std::chrono::duration<float>(currentTime - lastFrameTime).count();
    if (delta < frameDuration) {
        std::this_thread::sleep_for(std::chrono::milliseconds((int)((frameDuration - delta) * 1000)));
    }
    lastFrameTime = std::chrono::steady_clock::now();
}

unsigned int loadTexture(const char* path) {
    unsigned int textureID;
    glGenTextures(1, &textureID);

    int width, height, nrChannels;
    unsigned char* data = stbi_load(path, &width, &height, &nrChannels, 0);

    if (data) {
        GLenum format;
        if (nrChannels == 1)
            format = GL_RED;
        else if (nrChannels == 3)
            format = GL_RGB;
        else if (nrChannels == 4)
            format = GL_RGBA;
        else
            format = GL_RGB;

        glBindTexture(GL_TEXTURE_2D, textureID);
        glTexImage2D(GL_TEXTURE_2D, 0, format, width, height, 0, format, GL_UNSIGNED_BYTE, data);
        glGenerateMipmap(GL_TEXTURE_2D);

        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT);
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT);
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR);
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR);

        std::cout << "Texture loaded successfully: " << path << " (ID: " << textureID << ")" << std::endl;
        stbi_image_free(data);
    }
    else {
        std::cout << "Failed to load texture: " << path << std::endl;
        // Створюємо просту текстуру-заглушку
        unsigned char dummyData[64 * 64 * 3];
        for (int i = 0; i < 64 * 64 * 3; i += 3) {
            dummyData[i] = 255;     // R
            dummyData[i + 1] = 0;     // G
            dummyData[i + 2] = 255;   // B
        }

        glBindTexture(GL_TEXTURE_2D, textureID);
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, 64, 64, 0, GL_RGB, GL_UNSIGNED_BYTE, dummyData);
        glGenerateMipmap(GL_TEXTURE_2D);
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT);
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT);
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR);
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR);

        std::cout << "Created fallback texture (ID: " << textureID << ")" << std::endl;
    }

    return textureID;
}

const char* vertexShaderSource = "#version 330 core\n"
"layout (location = 0) in vec3 aPos;\n"
"layout (location = 1) in vec2 aTexCoord;\n"
"out vec2 TexCoord;\n"
"uniform mat4 transform;\n"
"void main() {\n"
"    gl_Position = transform * vec4(aPos, 1.0);\n"
"    TexCoord = aTexCoord;\n"
"}\0";

const char* fragmentShaderSource = "#version 330 core\n"
"out vec4 FragColor;\n"
"in vec2 TexCoord;\n"
"uniform sampler2D ourTexture;\n"
"void main() {\n"
"    FragColor = texture(ourTexture, TexCoord);\n"
"}\0";

unsigned int createShaderProgram() {
    unsigned int vertexShader = glCreateShader(GL_VERTEX_SHADER);
    glShaderSource(vertexShader, 1, &vertexShaderSource, NULL);
    glCompileShader(vertexShader);

    // Перевірка компіляції вертексного шейдера
    int success;
    char infoLog[512];
    glGetShaderiv(vertexShader, GL_COMPILE_STATUS, &success);
    if (!success) {
        glGetShaderInfoLog(vertexShader, 512, NULL, infoLog);
        std::cout << "Vertex shader compilation failed:\n" << infoLog << std::endl;
    }

    unsigned int fragmentShader = glCreateShader(GL_FRAGMENT_SHADER);
    glShaderSource(fragmentShader, 1, &fragmentShaderSource, NULL);
    glCompileShader(fragmentShader);

    // Перевірка компіляції фрагментного шейдера
    glGetShaderiv(fragmentShader, GL_COMPILE_STATUS, &success);
    if (!success) {
        glGetShaderInfoLog(fragmentShader, 512, NULL, infoLog);
        std::cout << "Fragment shader compilation failed:\n" << infoLog << std::endl;
    }

    unsigned int program = glCreateProgram();
    glAttachShader(program, vertexShader);
    glAttachShader(program, fragmentShader);
    glLinkProgram(program);

    // Перевірка лінковки
    glGetProgramiv(program, GL_LINK_STATUS, &success);
    if (!success) {
        glGetProgramInfoLog(program, 512, NULL, infoLog);
        std::cout << "Shader program linking failed:\n" << infoLog << std::endl;
    }

    glDeleteShader(vertexShader);
    glDeleteShader(fragmentShader);
    return program;
}

void processInput(GLFWwindow* window) {
    if (glfwGetKey(window, GLFW_KEY_ESCAPE) == GLFW_PRESS)
        glfwSetWindowShouldClose(window, true);

    static bool spacePressed = false;
    if (glfwGetKey(window, GLFW_KEY_SPACE) == GLFW_PRESS && !spacePressed) {
        isAnimating = !isAnimating;
        spacePressed = true;
        std::cout << "Animation " << (isAnimating ? "resumed" : "paused") << std::endl;
    }
    if (glfwGetKey(window, GLFW_KEY_SPACE) == GLFW_RELEASE) {
        spacePressed = false;
    }
}

int main() {
    // Ініціалізація GLFW
    glfwInit();
    glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, 3);
    glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, 3);
    glfwWindowHint(GLFW_OPENGL_PROFILE, GLFW_OPENGL_CORE_PROFILE);

    // Створення вікна
    GLFWwindow* window = glfwCreateWindow(SCR_WIDTH, SCR_HEIGHT, "Textured Rectangles & Rotating Square", NULL, NULL);
    if (window == NULL) {
        std::cout << "Failed to create GLFW window" << std::endl;
        glfwTerminate();
        return -1;
    }
    glfwMakeContextCurrent(window);

    // Завантаження GLAD
    if (!gladLoadGLLoader((GLADloadproc)glfwGetProcAddress)) {
        std::cout << "Failed to initialize GLAD" << std::endl;
        return -1;
    }

    // Три прямокутники з різними позиціями (щоб не перетиналися)
    // Прямокутник 1: лівий нижній кут
    float rect1[] = {
        // positions (x, y, z)    // texture coords (u, v)
        -0.8f, -0.7f, 0.0f,       0.0f, 0.0f,
        -0.2f, -0.7f, 0.0f,       1.0f, 0.0f,
        -0.2f,  0.0f, 0.0f,       1.0f, 1.0f,
        -0.8f, -0.7f, 0.0f,       0.0f, 0.0f,
        -0.2f,  0.0f, 0.0f,       1.0f, 1.0f,
        -0.8f,  0.0f, 0.0f,       0.0f, 1.0f
    };

    // Прямокутник 2: правий верхній кут
    float rect2[] = {
         0.3f,  0.2f, 0.0f,       0.0f, 0.0f,
         0.9f,  0.2f, 0.0f,       1.0f, 0.0f,
         0.9f,  0.8f, 0.0f,       1.0f, 1.0f,
         0.3f,  0.2f, 0.0f,       0.0f, 0.0f,
         0.9f,  0.8f, 0.0f,       1.0f, 1.0f,
         0.3f,  0.8f, 0.0f,       0.0f, 1.0f
    };

    // Прямокутник 3: верхній лівий кут
    float rect3[] = {
        -0.8f,  0.3f, 0.0f,       0.0f, 0.0f,
        -0.1f,  0.3f, 0.0f,       1.0f, 0.0f,
        -0.1f,  0.7f, 0.0f,       1.0f, 1.0f,
        -0.8f,  0.3f, 0.0f,       0.0f, 0.0f,
        -0.1f,  0.7f, 0.0f,       1.0f, 1.0f,
        -0.8f,  0.7f, 0.0f,       0.0f, 1.0f
    };

    // Квадрат для обертання (розташований в центрі праворуч)
    float square[] = {
        -0.25f, -0.25f, 0.0f,     0.0f, 0.0f,
         0.25f, -0.25f, 0.0f,     1.0f, 0.0f,
         0.25f,  0.25f, 0.0f,     1.0f, 1.0f,
        -0.25f, -0.25f, 0.0f,     0.0f, 0.0f,
         0.25f,  0.25f, 0.0f,     1.0f, 1.0f,
        -0.25f,  0.25f, 0.0f,     0.0f, 1.0f
    };

    // Створення VAO та VBO
    unsigned int VAOs[4], VBOs[4];
    glGenVertexArrays(4, VAOs);
    glGenBuffers(4, VBOs);

    float* rects[] = { rect1, rect2, rect3, square };
    int sizes[] = { sizeof(rect1), sizeof(rect2), sizeof(rect3), sizeof(square) };

    for (int i = 0; i < 4; i++) {
        glBindVertexArray(VAOs[i]);
        glBindBuffer(GL_ARRAY_BUFFER, VBOs[i]);
        glBufferData(GL_ARRAY_BUFFER, sizes[i], rects[i], GL_STATIC_DRAW);

        // Позиція
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 5 * sizeof(float), (void*)0);
        glEnableVertexAttribArray(0);

        // Текстурні координати
        glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 5 * sizeof(float), (void*)(3 * sizeof(float)));
        glEnableVertexAttribArray(1);
    }

    // Завантаження текстур (ВКАЖІТЬ ВАШІ ШЛЯХИ ДО ФАЙЛІВ)
    unsigned int textures[4];

    // ЗМІНІТЬ ЦІ ШЛЯХИ НА ВАШІ!
    textures[0] = loadTexture("C:/Users/ASUS/OneDrive/Desktop/png1.jpg");  // Ваш шлях
    textures[1] = loadTexture("C:/Users/ASUS/OneDrive/Desktop/png2.jpg");  // Ваш шлях
    textures[2] = loadTexture("C:/Users/ASUS/OneDrive/Desktop/png3.jpg");  // Ваш шлях
    textures[3] = loadTexture("C:/Users/ASUS/OneDrive/Desktop/png4.jpg");  // Ваш шлях

    // Якщо хочете використовувати файли в папці з проектом:
    // textures[0] = loadTexture("texture1.jpg");
    // textures[1] = loadTexture("texture2.jpg");
    // textures[2] = loadTexture("texture3.jpg");
    // textures[3] = loadTexture("texture_square.jpg");

    // Перевірка завантаження текстур
    for (int i = 0; i < 4; i++) {
        if (textures[i] == 0) {
            std::cout << "Warning: Texture " << i << " not loaded properly!" << std::endl;
        }
    }

    unsigned int shaderProgram = createShaderProgram();
    glUseProgram(shaderProgram);

    // Встановлення позиції квадрата (зміщуємо його в центр)
    glm::mat4 squareTransform = glm::mat4(1.0f);
    squareTransform = glm::translate(squareTransform, glm::vec3(0.5f, -0.3f, 0.0f));

    std::cout << "Program started. Press SPACE to pause/resume rotation" << std::endl;

    // Основний цикл
    while (!glfwWindowShouldClose(window)) {
        processInput(window);

        // Обмеження FPS
        limitFPS(60.0f);

        // Оновлення кута обертання
        float currentTime = glfwGetTime();
        float deltaTime = currentTime - lastTime;
        lastTime = currentTime;

        if (isAnimating) {
            rotationAngle += 90.0f * deltaTime;  // 90 градусів за секунду
            if (rotationAngle > 360.0f) rotationAngle -= 360.0f;
        }

        // Створення матриці трансформації для квадрата
        glm::mat4 transform = squareTransform;
        transform = glm::rotate(transform, glm::radians(rotationAngle), glm::vec3(0.0f, 0.0f, 1.0f));

        // Очищення екрану
        glClearColor(0.2f, 0.3f, 0.3f, 1.0f);
        glClear(GL_COLOR_BUFFER_BIT);

        // Малювання трьох прямокутників (без обертання)
        for (int i = 0; i < 3; i++) {
            // Одинична матриця для нерухомих прямокутників
            glm::mat4 identity = glm::mat4(1.0f);
            glUniformMatrix4fv(glGetUniformLocation(shaderProgram, "transform"), 1, GL_FALSE, glm::value_ptr(identity));
            glBindTexture(GL_TEXTURE_2D, textures[i]);
            glBindVertexArray(VAOs[i]);
            glDrawArrays(GL_TRIANGLES, 0, 6);
        }

        // Малювання квадрата з обертанням
        glUniformMatrix4fv(glGetUniformLocation(shaderProgram, "transform"), 1, GL_FALSE, glm::value_ptr(transform));
        glBindTexture(GL_TEXTURE_2D, textures[3]);
        glBindVertexArray(VAOs[3]);
        glDrawArrays(GL_TRIANGLES, 0, 6);

        glfwSwapBuffers(window);
        glfwPollEvents();
    }

    // Очищення ресурсів
    for (int i = 0; i < 4; i++) {
        glDeleteVertexArrays(1, &VAOs[i]);
        glDeleteBuffers(1, &VBOs[i]);
        glDeleteTextures(1, &textures[i]);
    }
    glDeleteProgram(shaderProgram);

    glfwTerminate();
    return 0;
}