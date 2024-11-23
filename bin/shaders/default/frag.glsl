// default/frag.glsl

#version 420 core

layout (location = 0) out vec4 OutColor;
layout (binding = 0) uniform sampler2D texture_0;

uniform vec3 ka;
uniform vec3 kd;
uniform vec3 ks;
uniform float ph;
uniform float trans;
uniform int is_texture;

in vec3 Normal;
in vec3 Pos;
in vec4 CamLoc;
in vec2 TexCoord;

layout (std140, binding = 3) uniform lights_uniform
{
  vec4 lights[];
};

vec3 kdc = kd;

vec3 Shade( vec3 Pos, vec3 Norm, vec3 LightDir, vec3 LightColor )
{
  vec3 RayDir = normalize(Pos - CamLoc.xyz);
  Norm = normalize(Norm);
  Norm = faceforward(Norm, RayDir, Norm);

  // ambient
  vec3 color = ka;

  // diffuse
  color += max(dot(Norm, LightDir), 0) * kdc * LightColor;

  // specular
  vec3 Reflected = reflect(RayDir, Norm);
  color += pow(max(0, dot(Reflected, LightDir)), ph) * ks * LightColor;

  return color;
}

void main()
{
  vec4 tex = vec4(0);

  if (is_texture > 0)
  {
    tex = texture(texture_0, TexCoord);
    kdc = tex.xyz;    
  }
  vec3 LightInfluence = vec3(0);

  for (int i = 0; i < int(lights[1].w + 0.001); i++)
  {
    vec3 dir = normalize(lights[2 * i].xyz - Pos) * lights[2 * i].w + lights[2 * i].xyz * (1 - lights[2 * i].w);
    vec3 color = lights[2 * i + 1].xyz;
    LightInfluence += Shade(Pos, Normal,  dir, color);
  }

  OutColor = vec4(LightInfluence, 0);
}
