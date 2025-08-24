#include "math.hpp"
#include <cmath>

float deg_to_rad(const float &deg) { return deg * (M_PI / 180.0f); }

void mv_v(const Point3D &pos, std::vector<Point3D> &v)
{
  for (auto &i : v)
  {
    i.x += pos.x;
    i.y += pos.y;
    i.z += pos.z;
  }
}

void rot_v(const Point3D &rot, std::vector<Point3D> &v)
{
  const double cx = cos(rot.x), sx = sin(rot.x);
  const double cy = cos(rot.y), sy = sin(rot.y);
  const double cz = cos(rot.z), sz = sin(rot.z);

  for (auto &p : v)
  {
    double x = p.x;
    double y = p.y;
    double z = p.z;

    // rotate around Y
    double x1 = x * cy + z * sy;
    double z1 = -x * sy + z * cy;

    // rotate around X (use z1)
    double y2 = y * cx - z1 * sx;
    double z2 = y * sx + z1 * cx;

    // rotate around Z (use x1, y2)
    double x3 = x1 * cz - y2 * sz;
    double y3 = x1 * sz + y2 * cz;

    p.x = static_cast<float>(x3);
    p.y = static_cast<float>(y3);
    p.z = static_cast<float>(z2);
  }
}

Point3D sub_v(const Point3D &v1, const Point3D &v2)
{
  return {v1.x - v2.x, v1.y - v2.y, v1.z - v1.z};
}

Point3D cross_v(const Point3D &v1, const Point3D &v2)
{
  return {
      (v1.y * v2.z - v2.z * v1.y),
      (v1.z * v2.x - v1.x * v2.z),
      (v1.x * v2.y - v1.y * v2.x)};
}

Point3D div_v(const Point3D &v, const float &fact)
{
  return {v.x / fact, v.y / fact, v.z / fact};
}

Point3D norm(const Point3D &n)
{
  float len = sqrt(n.x * n.x + n.y * n.y + n.z * n.z);
  if (len == 0.0f)
    return {0, 0, 0};
  return div_v(n, len);
}