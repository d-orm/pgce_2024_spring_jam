#version 300 es
precision highp float;

#include "uniforms"

in vec2 fragCoord;
out vec4 fragColor;

void main()
{
    float t = iTime*.75;
	
    vec2 uv = fragCoord;
    uv -= 0.5;
    uv.y += 0.5;

    float size = 0.01 + 0.02 * pow(1.0 -abs(fract(t + 0.45) -0.5), 4.0);
    float dist = length(max(abs(uv) - size, 0.0));
    float glow = 2.0 / (dist * 11.0 + 0.5);
    
    vec3 col;

    if (iTempValue > 80.0) {
        col = vec3(0.6, 0.1, 0.1);
    }
    if (iTempValue < 20.0) {
        col = vec3(0.1, 0.8, 1.0);
    }
    if (iTempValue >= 20.0 && iTempValue <= 80.0) {
        col = vec3(0.1, 0.3, 0.1);
        glow /= 2.0;
    }

    fragColor = vec4(glow * col, glow);
}

