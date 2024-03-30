#version 300 es
precision highp float;

#include "uniforms"

in vec2 fragCoord;
out vec4 fragColor;

#define TWO_PI 6.28
#define MAX_ITERATIONS 5
#define INITIAL_INTENSITY .003
#define TIME_OFFSET 23.0
#define COLOR_BOOST 1.17
#define COLOR_POWER 1.4
#define INTENSITY_POWER 14.0
#define SWIRL_STRENGTH 0.10515 // Strength of the swirl effect.

vec4 bgEffect(vec3 backgroundColor, float animationSpeed) {
    vec2 textureCoordinates = fragCoord.xy - 0.5;
    float adjustedTime = iTime * animationSpeed + TIME_OFFSET;

    // Swirl effect
    float distance = length(textureCoordinates - vec2(0., 0.)); // Distance from center
    float angle = distance * SWIRL_STRENGTH * adjustedTime; // Angle for swirling based on distance and time
    vec2 center = vec2(0.5, 0.5); // Center of the swirl
    vec2 direction = textureCoordinates - center;
    vec2 swirledCoordinates = vec2(
        cos(angle) * direction.x - sin(angle) * direction.y,
        sin(angle) * direction.x + cos(angle) * direction.y
    ) + center;

    vec2 wrappedCoordinates = mod(swirledCoordinates*TWO_PI, TWO_PI) - 250.0;
    vec2 iterationCoordinates = vec2(wrappedCoordinates);
    float colorIntensity = 1.0;
    float baseIntensity = INITIAL_INTENSITY;

    for (int iteration = 0; iteration < MAX_ITERATIONS; iteration++) {
        float timeFactor = adjustedTime * (1.0 - (3.5 / float(iteration + 1)));
        iterationCoordinates = wrappedCoordinates + vec2(cos(timeFactor - iterationCoordinates.x) + sin(timeFactor + iterationCoordinates.y), sin(timeFactor - iterationCoordinates.y) + cos(timeFactor + iterationCoordinates.x));
        colorIntensity += 1.0/length(vec2(wrappedCoordinates.x / (sin(iterationCoordinates.x + timeFactor)/baseIntensity), wrappedCoordinates.y / (cos(iterationCoordinates.y + timeFactor)/baseIntensity)));
    }
    colorIntensity /= float(MAX_ITERATIONS);
    colorIntensity = COLOR_BOOST - pow(colorIntensity, COLOR_POWER);
    vec3 effectColor = vec3(pow(abs(colorIntensity), INTENSITY_POWER));
    effectColor = clamp(effectColor + backgroundColor, 0.0, 1.0);
    
    return vec4(effectColor, 1.0);
}


void main() {
    if (iTempMode == 1.0) {
        vec3 color = vec3(0.0, 0.75, 0.75);
        fragColor = bgEffect(color, 0.2);        
        return;
    }
    if (iTempMode == 2.0) {
        vec3 color = vec3(0.0, 0.5, 0.0);
        fragColor = bgEffect(color, 0.7);        
        return;
    }
    if (iTempMode == 3.0) {
        vec3 color = vec3(0.5, 0.0, 0.0);
        fragColor = bgEffect(color, 1.5);        
        return;
    }
}
