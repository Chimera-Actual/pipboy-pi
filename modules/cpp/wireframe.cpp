#include "math.hpp"
#include "obj_loader.hpp"
#include <vector>
#include <string>
#include <cmath>
#include <algorithm>
#include <utility>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;

class WireframeRenderer
{
public:
  WireframeRenderer(int width, int height, float focal = 50.0f)
      : width(width), height(height), focal_l(focal), rot_y(0.0f), running(false)
  {
    camera = {0, 0, 10};
  }
  void load_model(const std::string &path)
  {
    obj = Obj(path);
    original_v = obj.v;
  }
  void set_camera(float x, float y, float z)
  {
    camera = {x, y, z};
  }

  void set_rotation(float x, float y, float z)
  {
    rot = {deg_to_rad(x), deg_to_rad(y), deg_to_rad(z)};
  }

  // Lifecycle
  void start() { running = true; }
  void stop() { running = false; }

  bool is_running() const { return running; }

  std::vector<Line2D> render()
  {
    if (!running)
      return {};
    std::vector<Line2D> lines;
    Obj obj_new = obj;
    obj_new.v = original_v;

    rot_y += deg_to_rad(5.0f); // 1 degree per frame
    if (rot_y > 2 * M_PI)
      rot_y -= 2 * M_PI;

    Point3D rot_rad = {rot.x, rot.y + rot_y, rot.z};
    rot_v(rot_rad, obj_new.v);
    mv_v(camera, obj_new.v);

    float factor = (width < height) ? (float)width / 100.0f : (float)height / 100.0f;

    std::vector<Point2DInt> new_v;
    new_v.resize(obj_new.v.size());
    for (size_t i = 0; i < obj_new.v.size(); i++)
    {
      new_v[i] = conv_screen_space(obj_new.v[i], height, width, factor, focal_l);
    }

    for (const Face &f : obj_new.f)
    {
      if (std::max({f.v1, f.v2, f.v3}) >= (int)new_v.size())
        continue;

      add_line(lines, new_v[f.v1], new_v[f.v2]);
      add_line(lines, new_v[f.v2], new_v[f.v3]);
      add_line(lines, new_v[f.v3], new_v[f.v1]);
    }
    return lines;
  }

private:
  int width, height;
  float focal_l;
  Point3D camera;
  Point3D rot = {0, 0, 0};
  float rot_y;
  bool running;

  Obj obj;
  std::vector<Point3D> original_v;

  static Point2DInt conv_screen_space(const Point3D &vertex, int rows, int cols, float factor, float focal_l)
  {
    const float EPS_Z = 0.0001f;
    if (vertex.z <= EPS_Z)
      return {-1, -1};
    int sx = static_cast<int>(round(((vertex.x * focal_l / vertex.z) * factor) + (cols * 0.5f)));
    int sy = static_cast<int>(round(((vertex.y * focal_l / vertex.z) * factor) + (rows * 0.5f)));
    return {sx, sy};
  }

  static void add_line(std::vector<Line2D> &out, const Point2DInt &a, const Point2DInt &b)
  {
    if (a.x < 0 || b.x < 0 || a.y < 0 || b.y < 0)
      return;
    out.push_back({a.x, a.y, b.x, b.y});
  }
};

// PyBind11 module
PYBIND11_MODULE(wireframe, m)
{
  py::class_<Line2D>(m, "Line2D")
      .def_readonly("x1", &Line2D::x1)
      .def_readonly("y1", &Line2D::y1)
      .def_readonly("x2", &Line2D::x2)
      .def_readonly("y2", &Line2D::y2);

  py::class_<WireframeRenderer>(m, "WireframeRenderer")
      .def(py::init<int, int, float>())
      .def("load_model", &WireframeRenderer::load_model)
      .def("set_camera", &WireframeRenderer::set_camera)
      .def("set_rotation", &WireframeRenderer::set_rotation)
      .def("start", &WireframeRenderer::start)
      .def("stop", &WireframeRenderer::stop)
      .def("is_running", &WireframeRenderer::is_running)
      .def("render", &WireframeRenderer::render);
}