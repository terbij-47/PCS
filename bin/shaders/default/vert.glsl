// default/vert.glsl

#version 420 core

layout (location = 0) in vec3 InPosition;
layout (location = 1) in vec3 InNormal;
layout (location = 2) in vec2 InTexCoord;
layout (location = 3) in vec4 InColor;

layout (std140, binding = 0) uniform view_struct
{
  mat4 matr_vp;
  vec4 cam_loc;
};

layout (std140, binding = 1) uniform instance_transforms
{
  mat4 worlds[];
};

out vec3 Normal;
out vec3 Pos;
out vec4 CamLoc;
out vec2 TexCoord;

uniform int instance_count;

void main()
{
  mat4 wvp = matr_vp * worlds[gl_InstanceID * 2];
  vec4 v = wvp * vec4(InPosition, 1);
  Pos = (worlds[gl_InstanceID * 2] * vec4(InPosition, 1)).xyz;
  gl_Position = v;
  Normal = (worlds[gl_InstanceID * 2 + 1] * vec4(InNormal, 1)).xyz;

  CamLoc = cam_loc;
  TexCoord = InTexCoord;
}