#version 300 es
precision highp float;

// built upon from by https://www.shadertoy.com/view/lsX3z4

#include "uniforms"
#include "constants"

in vec2 fragCoord;
out vec4 fragColor;

const float distanceScaleFactor = 3.0;
const float distanceExpFactor = -4.0;
const float distanceOffset = 2.0;
const float colorOffset = 2.0;
const float colorExponentBase = 2.0;

float calculateSquaredLength(vec2 position) {
    return dot(position, position);
}

float generateNoise(vec2 position) {
    return fract(sin(fract(sin(position.x) * (123.321)) + position.y) * 123.321);
}

float calculateWorleyNoise(vec2 position) {
    float minDistance = 1e30;
    for (int xOffset = -1; xOffset <= 1; ++xOffset)
    for (int yOffset = -1; yOffset <= 1; ++yOffset) {
        vec2 targetPosition = floor(position) + vec2(xOffset, yOffset);
        minDistance = min(minDistance, calculateSquaredLength(position - targetPosition - vec2(generateNoise(targetPosition))));
    }
    return distanceScaleFactor * exp(distanceExpFactor * abs(distanceOffset * minDistance - 1.));
}

float calculateFractalWorleyNoise(vec2 position, float time) {
    return sqrt(sqrt(sqrt(
        pow(calculateWorleyNoise(position + time), 0.5) *
        calculateWorleyNoise(position * 2. + vec2(1.3, 1.3) + time * vec2(.5, .5)) *
        calculateWorleyNoise(position * 4. + vec2(2.3, 2.3) + time * vec2(.25, .25)) *
        calculateWorleyNoise(position * 8. + vec2(3.3, 3.3) + time * vec2(.125, .125)) *
        calculateWorleyNoise(position * 32. + vec2(4.3, 4.3) + time * vec2(.125, .125)) *
        sqrt(calculateWorleyNoise(position * 64. + vec2(5.3, 5.3) + time * vec2(.0625, .0625))) *
        sqrt(sqrt(calculateWorleyNoise(position * 24. + vec2(7.3, 7.3)))))));
}

vec4 generateColorOutput(vec2 uv, vec3 colorScale) {
    float time = calculateFractalWorleyNoise(uv, iTime);
    time *= exp(-calculateSquaredLength(abs(2. * uv - 1.)));
    float radius = calculateSquaredLength(abs(2. * uv - 1.) * iResolution.xy);
    vec4 finalColor = vec4(time * colorScale * vec3(1., time, colorOffset + pow(time, colorExponentBase - time)), 1.);
    return finalColor;
}

vec2 swirlAndWarp(vec2 uv, float time) {
    uv = (uv - 0.5) * 2.0;
    float r = length(uv);
    float a = atan(uv.y, uv.x);
    float f = 1.0 / r;
    f = pow(f, 0.5);
    uv = vec2(cos(a + f), sin(a + f)) * r;
    uv = (uv + 1.0) / 2.0;
    return uv;
}

void main() {
    vec2 uv = swirlAndWarp(fragCoord, iTime);

    if (iTempMode == 1.0) {
        vec3 colorScale = vec3(0.1, 1.0, 1.0);
        fragColor = generateColorOutput(uv, colorScale);
        return;
    }
    if (iTempMode == 2.0) {
        vec3 colorScale = vec3(0.1, 1.0, 0.1);
        fragColor = generateColorOutput(uv, colorScale);
        return;
    }
    if (iTempMode == 3.0) {
        vec3 colorScale = vec3(1.0, 0.1, 0.1);
        fragColor = generateColorOutput(uv, colorScale);
        return;
    }
    vec3 colorScale = vec3(1.0, 1.0, 1.0);
    fragColor = generateColorOutput(uv, colorScale);
}
