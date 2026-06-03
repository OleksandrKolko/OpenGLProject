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

// Глобальні змінні для руху прямокутника
float rectX = 0.0f;           // позиція по X
float rectY = 0.0f;           // позиція по Y
float rectSpeed = 0.01f;      // швидкість руху

// Глобальні змінні для миші
double mouseX = 0.0f, mouseY = 0.0f;     // позиція курсора
bool isMouseOverRect = false;             // чи курсор над прямокутником
float rotationAngleFromMouse = 0.0f;      // кут обертання від миші

// Змінні для обмеження FPS
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

        std::cout << "Texture loaded successfully: " << path << std::endl;
        stbi_image_free(data);
    }
    else {
        std::cout << "Failed to load texture: " << path << std::endl;
        // Створюємо просту текстуру-заглушку (рожевий квадрат)
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

        std::cout << "Created fallback texture" << std::endl;
    }

    return textureID;
}

// Функція обробки натискань клавіш (клавіатура)
void keyCallback(GLFWwindow* window, int key, int scancode, int action, int mods) {
    // Якщо клавіша натиснута або затиснута
    if (action == GLFW_PRESS || action == GLFW_REPEAT) {
        switch (key) {
        case GLFW_KEY_LEFT:
            rectX -= rectSpeed;
            std::cout << "Moving left, X: " << rectX << std::endl;
            break;
        case GLFW_KEY_RIGHT:
            rectX += rectSpeed;
            std::cout << "Moving right, X: " << rectX << std::endl;
            break;
        case GLFW_KEY_UP:
            rectY += rectSpeed;
            std::cout << "Moving up, Y: " << rectY << std::endl;
            break;
        case GLFW_KEY_DOWN:
            rectY -= rectSpeed;
            std::cout << "Moving down, Y: " << rectY << std::endl;
            break;
        case GLFW_KEY_ESCAPE:
            glfwSetWindowShouldClose(window, true);
            break;
        }
    }
}

// Функція перевірки, чи курсор над прямокутником
bool isPointOverRect(double mouseX, double mouseY, float rectCenterX, float rectCenterY, float rectWidth, float rectHeight) {
    // Конвертуємо координати миші з екрану в координати OpenGL
    double glX = (mouseX / SCR_WIDTH) * 2.0 - 1.0;
    double glY = 1.0 - (mouseY / SCR_HEIGHT) * 2.0;

    // Перевіряємо, чи курсор в межах прямокутника
    float halfWidth = rectWidth / 2.0f;
    float halfHeight = rectHeight / 2.0f;

    bool inside = (glX > rectCenterX - halfWidth && glX < rectCenterX + halfWidth &&
        glY > rectCenterY - halfHeight && glY < rectCenterY + halfHeight);

    return inside;
}

// Функція обробки руху миші
void mouseCallback(GLFWwindow* window, double xpos, double ypos) {
    mouseX = xpos;
    mouseY = ypos;

    // Перевіряємо, чи курсор над прямокутником (прямокутник шириною 0.5, висотою 0.5)
    bool wasOver = isMouseOverRect;
    isMouseOverRect = isPointOverRect(mouseX, mouseY, rectX, rectY, 0.5f, 0.5f);

    // Якщо стан змінився, виводимо повідомлення
    if (wasOver != isMouseOverRect) {
        if (isMouseOverRect) {
            std::cout << "=== MOUSE ENTERED RECTANGLE! Starting rotation ===" << std::endl;
        }
        else {
            std::cout << "=== MOUSE LEFT RECTANGLE! Stopping rotation ===" << std::endl;
        }
    }
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

int main() {
    // Ініціалізація GLFW
    glfwInit();
    glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, 3);
    glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, 3);
    glfwWindowHint(GLFW_OPENGL_PROFILE, GLFW_OPENGL_CORE_PROFILE);

    // Створення вікна
    GLFWwindow* window = glfwCreateWindow(SCR_WIDTH, SCR_HEIGHT, "Textured Rectangle with Keyboard and Mouse", NULL, NULL);
    if (window == NULL) {
        std::cout << "Failed to create GLFW window" << std::endl;
        glfwTerminate();
        return -1;
    }
    glfwMakeContextCurrent(window);

    // ВСТАНОВЛЕННЯ CALLBACK-ФУНКЦІЙ ДЛЯ КЛАВІАТУРИ ТА МИШІ
    glfwSetKeyCallback(window, keyCallback);        // для клавіатури
    glfwSetCursorPosCallback(window, mouseCallback); // для миші

    // Завантаження GLAD
    if (!gladLoadGLLoader((GLADloadproc)glfwGetProcAddress)) {
        std::cout << "Failed to initialize GLAD" << std::endl;
        return -1;
    }

    // Дані для прямокутника (квадрата) - 2 трикутники
    float vertices[] = {
        // positions (x, y, z)    // texture coords (u, v)
        -0.25f, -0.25f, 0.0f,     0.0f, 0.0f,  // нижній лівий
         0.25f, -0.25f, 0.0f,     1.0f, 0.0f,  // нижній правий
         0.25f,  0.25f, 0.0f,     1.0f, 1.0f,  // верхній правий
        -0.25f, -0.25f, 0.0f,     0.0f, 0.0f,  // нижній лівий
         0.25f,  0.25f, 0.0f,     1.0f, 1.0f,  // верхній правий
        -0.25f,  0.25f, 0.0f,     0.0f, 1.0f   // верхній лівий
    };

    // Створення VAO та VBO
    unsigned int VAO, VBO;
    glGenVertexArrays(1, &VAO);
    glGenBuffers(1, &VBO);

    glBindVertexArray(VAO);
    glBindBuffer(GL_ARRAY_BUFFER, VBO);
    glBufferData(GL_ARRAY_BUFFER, sizeof(vertices), vertices, GL_STATIC_DRAW);

    // Позиція (x, y, z)
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 5 * sizeof(float), (void*)0);
    glEnableVertexAttribArray(0);

    // Текстурні координати (u, v)
    glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 5 * sizeof(float), (void*)(3 * sizeof(float)));
    glEnableVertexAttribArray(1);

    unsigned int texture;
    texture = loadTexture("C:/Users/ASUS/OneDrive/Desktop/png1.jpg");

    // Якщо хочете використовувати файл в папці з проектом:
    // texture = loadTexture("texture.jpg");

    unsigned int shaderProgram = createShaderProgram();
    glUseProgram(shaderProgram);

    std::cout << "\n=== PROGRAM STARTED ===" << std::endl;
    std::cout << "Controls:" << std::endl;
    std::cout << "  Arrow keys - move rectangle" << std::endl;
    std::cout << "  Mouse hover over rectangle - rotate" << std::endl;
    std::cout << "  ESC - exit" << std::endl;
    std::cout << "========================\n" << std::endl;

    // Основний цикл
    while (!glfwWindowShouldClose(window)) {
        // Обмеження FPS до 60
        limitFPS(60.0f);

        // Оновлення кута обертання, якщо курсор над прямокутником
        float currentTime = glfwGetTime();
        float deltaTime = currentTime - lastTime;
        lastTime = currentTime;

        if (isMouseOverRect) {
            // Обертаємо зі швидкістю 90 градусів за секунду
            rotationAngleFromMouse += 90.0f * deltaTime;
            if (rotationAngleFromMouse > 360.0f) {
                rotationAngleFromMouse -= 360.0f;
            }
        }
        else {
            // Поступово зупиняємо обертання
            rotationAngleFromMouse *= 0.98f;
        }

        // Створення матриці трансформації
        glm::mat4 transform = glm::mat4(1.0f);
        transform = glm::translate(transform, glm::vec3(rectX, rectY, 0.0f));  // рух
        transform = glm::rotate(transform, glm::radians(rotationAngleFromMouse), glm::vec3(0.0f, 0.0f, 1.0f)); // обертання

        // Очищення екрану
        glClearColor(0.2f, 0.3f, 0.3f, 1.0f);
        glClear(GL_COLOR_BUFFER_BIT);

        // Малювання прямокутника
        glUniformMatrix4fv(glGetUniformLocation(shaderProgram, "transform"), 1, GL_FALSE, glm::value_ptr(transform));
        glBindTexture(GL_TEXTURE_2D, texture);
        glBindVertexArray(VAO);
        glDrawArrays(GL_TRIANGLES, 0, 6);

        glfwSwapBuffers(window);
        glfwPollEvents();
    }

    // Очищення ресурсів
    glDeleteVertexArrays(1, &VAO);
    glDeleteBuffers(1, &VBO);
    glDeleteTextures(1, &texture);
    glDeleteProgram(shaderProgram);

    glfwTerminate();
    return 0;
}