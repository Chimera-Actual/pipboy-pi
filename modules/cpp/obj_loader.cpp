#include "obj_loader.hpp"
#include "math.hpp"
#include <fstream>
#include <iostream>
#include <iterator>
#include <sstream>

Obj::Obj(const std::string &file_path)
{

    parse_file(file_path);
};

void Obj::parse_file(const std::string &file_path)
{
    std::ifstream file(file_path);
    std::string current_line;
    if (file.is_open())
    {
        while (getline(file, current_line))
        {
            switch (current_line[0])
            {
            case 'o':
                // parse object name
                name = current_line.substr(2, std::string::npos);
                break;
            case 'v':
                // parce vertices
                float x, y, z;
                std::istringstream(current_line.substr(2, std::string::npos)) >> x >> y >> z;
                v.push_back({x, y, z});
                break;
            case 'f':
                std::string part;
                unsigned int v1, v2, v3;
                std::istringstream ss(current_line.substr(2)); // skip "f "

                // Read first vertex
                ss >> part;
                v1 = std::stoi(part.substr(0, part.find('/')));

                // Second vertex
                ss >> part;
                v2 = std::stoi(part.substr(0, part.find('/')));

                // Third vertex
                ss >> part;
                v3 = std::stoi(part.substr(0, part.find('/')));

                f.push_back({v1 - 1, v2 - 1, v3 - 1}); // 0-based indexing
                break;
            }
        }
        file.close();
    }
    else
    {
        std::cerr << "Unable to open file " << file_path << std::endl;
    }
};
