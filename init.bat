if not exist modules\cpp\build mkdir modules\cpp\build
cmake -G "Visual Studio 17 2022" -A x64 -S modules\cpp -B modules\cpp\build
cmake --build modules\cpp\build --config Release
copy modules\cpp\build\Release\* modules\cpp\