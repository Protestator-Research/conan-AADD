from conan import ConanFile
from conan.tools.cmake import CMakeToolchain, CMake, cmake_layout, CMakeDeps
from conan.tools.env import Environment
from conan.tools.apple import XcodeDeps
import os
from sys import platform


class AADDRecipe(ConanFile):
    name = "aadd"
    package_type = "library"

    # Optional metadata
    license = "GPL v3"
    author = "Moritz Herzog"
    url = "https://github.com/Protestator-Research/CPP-SysMLv2"
    description = "This library defines a SysMLv2 C++ Library allowing the usage of this for other projects."
    topics = ("SysMLv2", "modeling", "library")

    # Binary configuration
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": True, "fPIC": False}

    # Sources are located in the same place as this recipe, copy them to the recipe
    exports_sources = "CMakeLists.txt", "src/*", "doc/*", "examples/*", "test/*", "AADDConfig.h.in"

    def requirements(self):
        self.requires("glpk/5.0")

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC
            self.options.shared=True

    def configure(self):
        if self.options.shared:
            self.options.rm_safe("fPIC")
            self.options["glpk/*"].shared = True
        else:
            self.options["glpk/*"].shared = False

    def layout(self):
        cmake_layout(self)

    def generate(self):
        deps = CMakeDeps(self)
        deps.generate()
        tc = CMakeToolchain(self)
        tc.user_presets_path = 'CMakePresets.json'
        tc.generate()

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def build_requirements(self):
        self.tool_requires("cmake/[>=3.30.0 <5]")
        self.test_requires("gtest/[>=1.14.0 <2]")

    def test(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.test()

    def package(self):
        cmake = CMake(self)
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = ["aadd"]
        #self.cpp_info.builddirs.append(os.path.join("lib", "cmake", "sysmlv2"))