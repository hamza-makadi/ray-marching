#version 330 core


out vec4 fragColor;

uniform float screenWidth;
uniform float screenHeight;

uniform float time;

vec2 Resolution = vec2(screenWidth, screenHeight);

//define some constante
const float FOV = 1.0;
const int MAX_STEPS = 256;
const float MAX_DIST = 500;
const float EPSILON = 0.001;

////////////////////////////////////////////
//SDF functions
//you can find all this functions here >>> https://mercury.sexy/hg_sdf/ <<<

//SDF sphere
float fSphere(vec3 p, float r) {
    return length(p) - r;
}

// Plane with normal n (n is normalized) at some distance from the origin
float fPlane(vec3 p, vec3 n, float distanceFromOrigin) {
    return dot(p, n) + distanceFromOrigin;
}

// Repeat in three dimensions
vec3 pMod3(inout vec3 p, vec3 size) {
    vec3 c = floor((p + size*0.5)/size);
    p = mod(p + size*0.5, size) - size*0.5;
    return c;
}

/////////////////////////////////////////////

//Union finction
vec2 fOpUnionID(vec2 res1, vec2 res2){
    return (res1.x < res2.x) ? res1 : res2 ;
}


vec2 map(vec3 p){   
    //plane
    float planeDIST = fPlane(p, vec3(0,1,0), 1.0);
    float planeID = 2.0;
    vec2 plane = vec2(planeDIST, planeID);
    //sphere
    float sphereDIST = fSphere(p,1.0);
    float sphereID = 1.0;
    vec2 sphere = vec2(sphereDIST, sphereID);
    //result
    vec2 res = fOpUnionID(sphere,plane);
    return res;
}

//the actual ray march algorithm 
//this function returns a vec2 where the x is the distance and y is the color

vec2 rayMarch(vec3 rayOrigin, vec3 rayDir){

    vec2 hit,object;

    for(int i=0 ;i < MAX_STEPS; i++){

        vec3 p = rayOrigin + object.x * rayDir;
        hit = map(p);

        object.x += hit.x;
        object.y = hit.y;

        if(abs(hit.x) < EPSILON || object.x > MAX_DIST) break; 
    }
    return object;
}

void render(inout vec3 col,in vec2 uv){
    //define ray origine and normilaized ray direction
    vec3 rayOrigin = vec3(0.0, 0.0, -3.0);
    vec3 rayDir = normalize(vec3(uv,FOV));

    vec2 object = rayMarch(rayOrigin, rayDir);

    if(object.x < MAX_DIST){
        col += 3.0 / object.x;
    }
}

void main() {
    
    vec2 uv = (gl_FragCoord.xy * 2 - Resolution) / Resolution.y;

    vec3 col;
    render(col,uv);

    fragColor = vec4(col, 1.0);
}
