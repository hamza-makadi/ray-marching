#version 330 core

out vec4 fragColor;

uniform float screenWidth;
uniform float screenHeight;

uniform float time;

vec2 Resolution = vec2(screenWidth, screenHeight);

void main() {
    
    vec2 uv = (gl_FragCoord.xy * 2 - Resolution) / Resolution.y;

    fragColor = vec4(uv, 0.0, 1.0);
}
