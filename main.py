from OpenGL.GL import *
from OpenGL.GL.shaders import compileShader, compileProgram
import glfw, time


def capture_frame(filename, width, height):
    import numpy as np
    from PIL import Image
    data = glReadPixels(0, 0, width, height, GL_RGB, GL_UNSIGNED_BYTE)
    image = Image.frombytes("RGB", (width, height), data)
    image = image.transpose(Image.FLIP_TOP_BOTTOM)  # OpenGL renders bottom to top, so flip the image
    image.save(filename)


def load_fragment_file(file_path):
    try:
        with open(file_path, 'r') as file:
            fragment_content = file.read()
        return fragment_content
    except FileNotFoundError:
        print("File not found.")
        return None

def compile_shader(shader_type, source):
    shader = glCreateShader(shader_type)
    glShaderSource(shader, source)
    glCompileShader(shader)
    return shader

def load_shader_program(vertex_shader_source, fragment_shader_source):
    vertex_shader = compile_shader(GL_VERTEX_SHADER, vertex_shader_source)
    fragment_shader = compile_shader(GL_FRAGMENT_SHADER, fragment_shader_source)
    program = glCreateProgram()
    glAttachShader(program, vertex_shader)
    glAttachShader(program, fragment_shader)
    glLinkProgram(program)
    glUseProgram(program)
    return program



def main():

    # Initialize time variable
    start_time = time.time()


    # Initialize GLFW
    if not glfw.init():
        return

    # Create a window
    window = glfw.create_window(1200, 600, "Shader", None, None)
    if not window:
        glfw.terminate()
        return

    # Make the window's context current
    glfw.make_context_current(window)

    vertex_shader_source = load_fragment_file("vertex.vert")

    fragment_shader_source = load_fragment_file("fragment.frag")

    # Load and compile shader program
    shader_program = load_shader_program(vertex_shader_source, fragment_shader_source)

    # Get window size
    window_width, window_height = glfw.get_framebuffer_size(window)

    #Get the locations of the uniform variables in the shader
    screen_width_uniform_location = glGetUniformLocation(shader_program, "screenWidth")
    screen_height_uniform_location = glGetUniformLocation(shader_program, "screenHeight")
    time_uniform_location = glGetUniformLocation(shader_program, "time")
    
    
    # Define vertices for a fullscreen quad
    vertices = [
        -1.0, -1.0,  # bottom-left corner
         1.0, -1.0,  # bottom-right corner
         1.0,  1.0,  # top-right corner
        -1.0,  1.0   # top-left corner
    ]
    vertices = (GLfloat * len(vertices))(*vertices)

    # Define indices for the fullscreen quad
    indices = [
        0, 1, 2,  # first triangle
        0, 2, 3   # second triangle
    ]
    indices = (GLuint * len(indices))(*indices)

    # Create vertex array object (VAO) and vertex buffer object (VBO)
    vao = glGenVertexArrays(1)
    vbo = glGenBuffers(1)
    ebo = glGenBuffers(1)

    glBindVertexArray(vao)

    # Bind the VBO and upload vertex data
    glBindBuffer(GL_ARRAY_BUFFER, vbo)
    glBufferData(GL_ARRAY_BUFFER, len(vertices) * sizeof(GLfloat), vertices, GL_STATIC_DRAW)

    # Bind the EBO and upload index data
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, ebo)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, len(indices) * sizeof(GLuint), indices, GL_STATIC_DRAW)

    # Configure vertex attribute pointers
    glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, 2 * sizeof(GLfloat), ctypes.c_void_p(0))
    glEnableVertexAttribArray(0)

    # Unbind VAO (it's always a good habit to unbind any buffer/array to prevent strange bugs)
    glBindVertexArray(0)

    # Main loop
    while not glfw.window_should_close(window):

        


        # Set the values of the uniform variables
        glUniform1f(screen_width_uniform_location, window_width)
        glUniform1f(screen_height_uniform_location, window_height)

        # Poll for and process events
        glfw.poll_events()

        current_time = time.time() - start_time

        # Set the value of the uniform variable for time
        glUseProgram(shader_program)
        glUniform1f(time_uniform_location, current_time)

        # Render
        glClear(GL_COLOR_BUFFER_BIT)

        # Use the shader program
        glUseProgram(shader_program)

        # Bind the VAO
        glBindVertexArray(vao)

        # Draw the fullscreen quad
        glDrawElements(GL_TRIANGLES, len(indices), GL_UNSIGNED_INT, None)

        # Unbind the VAO
        glBindVertexArray(0)

        #capture_frame(f"frames/frame_{glfw.get_time()}.png", window_width, window_height)

        # Swap the front and back buffers
        glfw.swap_buffers(window)

    # Clean up
    glDeleteVertexArrays(1, [vao])
    glDeleteBuffers(1, [vbo])
    glDeleteBuffers(1, [ebo])
    glDeleteProgram(shader_program)

    # Terminate GLFW
    glfw.terminate()

if __name__ == "__main__":
    main()
