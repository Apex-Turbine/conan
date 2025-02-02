from conan import ConanFile
from conan.tools.cmake import CMakeToolchain, CMake, cmake_layout, CMakeDeps
from conan.tools.files import apply_conandata_patches, export_conandata_patches, replace_in_file
from conan.tools.scm import Git, Version
from pathlib import Path
import os, sys


class vtkRecipe(ConanFile):
    name = "vtk"
    user="apexturbine"
    channel="stable"
    package_type = "library"
    no_copy_source = True

    # Optional metadata
    url = "https://github.com/kitware/vtk"
    description = "The Visualization Toolkit (VTK) is an open-source, freely available software system for 3D computer graphics, image processing, and visualization."
    topics = ("vtk", "models", "3d")

    # Binary configuration
    settings = "os", "compiler", "build_type", "arch"
    options = {
        "shared": [True, False],
        "enable_standalone": [True, False],
        "enable_qt": [True, False],
        "qt_version": ["5", "6"],
        "wrap_python": [True, False],
        "wrap_tcl": [True, False],
        "wrap_java": [True, False],
        "install_sdk": [True, False],
        "install_headers": [True, False],
        "install_versioned_libs": [True, False],
        "enable_examples": [True, False],
        "enable_testing": [True, False],
        "exclude_data": [True, False],
        "install_no_development": [True, False],
        "smp_type": ["STDThreads", "serial", "OpenMP"],
        "lib_install_dir": ["ANY"],
        "bin_install_dir": ["ANY"],
        "ar_install_dir": ["ANY"],
    }
    default_options = {
        "shared": True,
        "enable_standalone": True,
        "enable_qt": True,
        "qt_version": "6",
        "wrap_python": False,
        "wrap_tcl": False,
        "wrap_java": False,
        "install_sdk": True,
        "install_headers": True,
        "install_versioned_libs": False,
        "enable_examples": False,
        "enable_testing": False,
        "exclude_data": True,
        "install_no_development": True,
        "smp_type": "STDThreads",
        "lib_install_dir": "lib",
        "bin_install_dir": "bin",
        "ar_install_dir": "lib",
    }

    requires = [
        "nlohmann_json/[~3.11]",
    ]

    def config_options(self):
        pass

    def configure(self):
        pass

    def layout(self):
        cmake_layout(self, build_folder="build", src_folder="vtk")

    def source(self):
        git = Git(self)
        git.clone(self.conan_data["sources"][self.version]["url"], 
                  args=["--depth", "1", "--branch", self.conan_data["sources"][self.version]["tag"]],
                  target='.')

    def generate(self):
        #If the compiler is clang, then we need to set the cxx and c flag to include -fcommon for libtiff
        #this should be added to the libtif cmake file
        if self.settings.compiler == "clang":
            print(self.source_folder)
            replace_in_file(self, Path(self.source_folder)/"ThirdParty/tiff/vtktiff/CMakeLists.txt", "add_subdirectory(libtiff)", "add_subdirectory(libtiff)\ntarget_compile_options(tiff PRIVATE -fcommon)")

        tc = CMakeToolchain(self)
        tc.variables["BUILD_SHARED_LIBS"] = "ON" if self.options.shared else "OFF"
        tc.variables["VTK_GROUP_ENABLE_STANDALONE"] = self.options.enable_standalone
        tc.variables["VTK_GROUP_ENABLE_Qt"] = "YES" if self.options.enable_qt else "NO"
        tc.variables["VTK_QT_VERSION"] = self.options.qt_version
        tc.variables["VTK_WRAP_PYTHON"] = "ON" if self.options.wrap_python else "OFF"
        tc.variables["VTK_WRAP_TCL"] = "ON" if self.options.wrap_tcl else "OFF"
        tc.variables["VTK_WRAP_JAVA"] = "ON" if self.options.wrap_java else "OFF"
        tc.variables["VTK_INSTALL_SDK"] = "ON" if self.options.install_sdk else "OFF"
        tc.variables["VTK_INSTALL_HEADERS"] = "ON" if self.options.install_headers else "OFF"
        tc.variables["VTK_VERSIONED_INSTALL"] = "ON" if self.options.install_versioned_libs else "OFF"
        tc.variables["VTK_BUILD_EXAMPLES"] = "ON" if self.options.enable_examples else "OFF"
        tc.variables["VTK_BUILD_TESTING"] = "ON" if self.options.enable_testing else "OFF"
        tc.variables["VTK_DATA_EXCLUDE_FROM_ALL"] = "ON" if self.options.exclude_data else "OFF"
        tc.variables["VTK_INSTALL_NO_DEVELOPMENT"] = "ON" if self.options.install_no_development else "OFF"
        tc.variables["VTK_SMP_IMPLEMENTATION_TYPE"] = self.options.smp_type
        tc.variables["VTK_LIBRARY_DESTINATION"] = self.options.lib_install_dir
        tc.variables["VTK_RUNTIME_DESTINATION"] = self.options.bin_install_dir
        tc.variables["VTK_ARCHIVE_DESTINATION"] = self.options.ar_install_dir
        tc.variables["VTK_MODULE_USE_EXTERNAL_VTK_nlohmannjson"] = "ON"            
        
        tc.generate()

        deps = CMakeDeps(self)
        deps.generate()

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        cmake = CMake(self)
        cmake.install()

    def package_info(self):
        self.cpp_info.set_property("cmake_find_mode","none")
        self.cpp_info.builddirs = ["lib/cmake/vtk"]
        self.cpp_info.build_modules = ["lib/cmake/vtk/vtk-config.cmake"]
        self.cpp_info.include_dirs = ["include","include/vtk"]
        self.cpp_info.names["cmake_find_package"] = "VTK"
        self.cpp_info.names["cmmake_find_package_multi"] = "VTK"




