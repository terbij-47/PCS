// cloth/frag.glsl

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

vec3 kdc = kd;

vec3 Shade( vec3 Pos, vec3 Norm )
{
  // light params
  vec3 LightDir = -normalize(vec3(0.5, -2, 0));
  vec3 LightColor = vec3(1);
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

  vec4 LightInfluence = vec4(Shade(Pos, Normal), 0);

  OutColor = LightInfluence * 1.0000001 + vec4(Pos.x, -Pos.y / 10, Pos.z, 0) * 0.00001 + vec4(Normal, 0) * 0.0001;
}






