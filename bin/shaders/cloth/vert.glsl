// cloth/vert.glsl

#version 420 core

layout (location = 2) in vec2 InTexCoord;

layout (std140, binding = 0) uniform view_struct
{
  mat4 matr_vp;
  vec4 cam_loc;
};

layout (std140, binding = 1) uniform ubo_points
{
  vec4 points[];
};

out vec3 Normal;
out vec3 Pos;
out vec4 CamLoc;
out vec2 TexCoord;

uniform int w;
uniform int h;

void main()
{
  int i = gl_VertexID;
  Pos = points[int(gl_VertexID)].xyz;
  gl_Position = matr_vp * vec4(Pos, 1);
  Normal = vec3(0, 1, 0);

  if (i - w - 1 >= 0 && i + w + 1 < w * h)
  {
    vec3 n1 = normalize(cross(normalize(points[i-w].xyz - Pos), normalize(points[i-w-1].xyz - Pos)));
    vec3 n2 = normalize(cross(normalize(points[i-w-1].xyz - Pos), normalize(points[i-1].xyz - Pos)));
    vec3 n3 = normalize(cross(normalize(points[i-1].xyz - Pos), normalize(points[i+w].xyz - Pos)));
    vec3 n4 = normalize(cross(normalize(points[i+w].xyz - Pos), normalize(points[i+w+1].xyz - Pos)));
    vec3 n5 = normalize(cross(normalize(points[i+w+1].xyz - Pos), normalize(points[i+1].xyz - Pos)));
    vec3 n6 = normalize(cross(normalize(points[i+1].xyz - Pos), normalize(points[i-w].xyz - Pos)));
    Normal = normalize(n1 + n2 + n3 + n4 + n5 + n6);
  }

  CamLoc = cam_loc;
  TexCoord = InTexCoord;
}