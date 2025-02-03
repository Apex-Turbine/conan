from conan import ConanFile
from conan.tools.cmake import CMakeToolchain, CMake, cmake_layout, CMakeDeps
from conan.tools.files import apply_conandata_patches, export_conandata_patches, get
from conan.tools.scm import Git, Version
from pathlib import Path
import os, sys

class opencvRecipe(ConanFile):
    name = "opencv"
    user="apexturbine"
    channel="stable"
    package_type = "library"
    no_copy_source = True

    # Optional metadata
    url = "https://github.com/opencv/opencv.git"
    description = "Image and vision processing library"
    topics = ["opencv", "image", "vision", "processing"]

    # Binary configuration
    settings = "os", "compiler", "build_type", "arch"
    options = {
        "shared": [True, False], 
        "pic": [True, False],
        "cpu_baseline": ["", "SSE", "SSE2", "SSE3", "SSSE3", "SSE41", "SSE42", "AVX", "AVX2", "AVX512"],
        "intrinsics": [True, False],
        "optimization": [True, False],
        "ipp_gaussian_blur": [True, False],
        "ipp_mean": [True, False],
        "ipp_minmax": [True, False],
        "ipp_sum": [True, False],
        "with_cuda": [True, False],
        "with_opencl": [True, False],
        "with_png": [True, False],
        "with_jpeg": [True, False],
        "with_tiff": [True, False],
        "with_webp": [True, False],
        "with_openjpeg": [True, False],
        "with_jasper": [True, False],
        "with_openexr": [True, False],
        "with_ffmpeg": [True, False],
        "with_gdal": [True, False],
        "with_gdcm": [True, False],
        "with_gstreamer": [True, False],
        "with_i394": [True, False],
        "with_openni2": [True, False],
        "with_pvapi": [True, False],
        "with_aravis": [True, False],
        "with_ximea": [True, False],
        "with_xine": [True, False],
        "with_liberalsense": [True, False],
        "with_mfx": [True, False],
        "with_gphoto2": [True, False],
        "videoio_enable_plugins": [True, False],
        "videoio_plugins": ["ANY"],
        "with_tbb": [True, False],
        "with_openmp": [True, False],
        "with_hpx": [True, False],
        "with_qt": ["OFF", "5", "6"],
        "with_opengl": [True, False],
        "with_protobuf": [True, False],
        "build_protobuf": [True, False],
        "dnn_opencl": [True, False],
        "with_openvino": [True, False],
        "dnn_cuda": [True, False],
        "with_halide": [True, False],
        "with_vulkan": [True, False],
        "with_gtk": [True, False],
        "with_v4l": [True, False],
        "with_msmf": [True, False],
        "with_dshow": [True, False],
        "with_win32ui": [True, False],
    }
    
    default_options = {
        "shared": True,
        "pic": True,
        "cpu_baseline": "AVX2",
        "intrinsics": True,
        "optimization": True,
        "ipp_gaussian_blur": True,
        "ipp_mean": True,
        "ipp_minmax": True,
        "ipp_sum": True,
        "with_cuda": False,
        "with_opencl": True,
        "with_png": True,
        "with_jpeg": True,
        "with_tiff": True,
        "with_webp": True,
        "with_openjpeg": True,
        "with_jasper": True,
        "with_openexr": True,
        "with_gdal": False,
        "with_gdcm": False,
        "with_ffmpeg": True,
        "with_gstreamer": True,
        "with_i394": True,
        "with_openni2": False,
        "with_pvapi": False,
        "with_aravis": False,
        "with_ximea": False,
        "with_xine": False,
        "with_liberalsense": False,
        "with_mfx": False,
        "with_gphoto2": False,
        "videoio_enable_plugins": True,
        "videoio_plugins": "all",
        "with_tbb": False,
        "with_openmp": False,
        "with_hpx": False,
        "with_qt": "6",
        "with_opengl": True,
        "with_protobuf": True,
        "build_protobuf": True,
        "dnn_opencl": True,
        "with_openvino": False,
        "dnn_cuda": False,
        "with_halide": False,
        "with_vulkan": False,
        "with_gtk": False,
        "with_v4l": False,
        "with_msmf": False,
        "with_dshow": False,
        "with_win32ui": False,
    }

    def config_options(self):
        if self.settings.os == "Linux":
            del self.options.with_msmf
            del self.options.with_dshow
            del self.options.with_win32ui
            self.default_options["with_gtk"] = True
            self.default_options["with_v4l"] = True

        if self.settings.os == "Windows":
            del self.options.with_gtk
            del self.options.with_v4l
            self.default_options["with_msmf"] = True
            self.default_options["with_dshow"] = True
            self.default_options["with_win32ui"] = True

    def configure(self):
        pass

    def source(self):
        git = Git(self)
        git.clone(self.conan_data["sources"][self.version]["url"], 
                  args=["--depth", "1", "--branch", self.conan_data["sources"][self.version]["tag"]],
                  target='.')

    def layout(self):
        cmake_layout(self, build_folder='build',src_folder="opencv")

    def generate(self):
        deps = CMakeDeps(self)
        deps.generate()

        tc = CMakeToolchain(self)

        tc.variables["BUILD_SHARED_LIBS"] = "ON" if self.options.shared else "OFF"
        tc.variables["ENABLE_PIC"] = "ON" if self.options.pic else "OFF"
        tc.variables["BUILD_TESTS"] = "OFF"
        tc.variables["BUILD_PERF_TESTS"] = "OFF"
        tc.variables["BUILD_EXAMPLES"] = "OFF"
        tc.variables["BUILD_opencv_apps"] = "OFF"
        tc.variables["CPU_BASELINE"] = self.options.cpu_baseline
        tc.variables["CV_ENABLE_INTRINSICS"] = "ON" if self.options.intrinsics else "OFF"
        tc.variables["CV_DISABLE_OPTIMIZATION"] = "OFF" if self.options.optimization else "ON"
        tc.variables["WITH_IPP_GAUSSIAN_BLUR"] = "ON" if self.options.ipp_gaussian_blur else "OFF"
        tc.variables["WITH_IPP_MEAN"] = "ON" if self.options.ipp_mean else "OFF"
        tc.variables["WITH_IPP_MINMAX"] = "ON" if self.options.ipp_minmax else "OFF"
        tc.variables["WITH_IPP_SUM"] = "ON" if self.options.ipp_sum else "OFF"
        tc.variables["WITH_CUDA"] = "ON" if self.options.with_cuda else "OFF"
        tc.variables["WITH_OPENCL"] = "ON" if self.options.with_opencl else "OFF"
        tc.variables["WITH_PNG"] = "ON" if self.options.with_png else "OFF"
        tc.variables["WITH_JPEG"] = "ON" if self.options.with_jpeg else "OFF"
        tc.variables["WITH_TIFF"] = "ON" if self.options.with_tiff else "OFF"
        tc.variables["WITH_WEBP"] = "ON" if self.options.with_webp else "OFF"
        tc.variables["WITH_OPENJPEG"] = "ON" if self.options.with_openjpeg else "OFF"
        tc.variables["WITH_JASPER"] = "ON" if self.options.with_jasper else "OFF"
        tc.variables["WITH_OPENEXR"] = "ON" if self.options.with_openexr else "OFF"
        tc.variables["WITH_FFMPEG"] = "ON" if self.options.with_ffmpeg else "OFF"
        tc.variables["WITH_GDAL"] = "ON" if self.options.with_gdal else "OFF"
        tc.variables["WITH_GDCM"] = "ON" if self.options.with_gdcm else "OFF"
        tc.variables["WITH_GSTREAMER"] = "ON" if self.options.with_gstreamer else "OFF"
        tc.variables["WITH_I394"] = "ON" if self.options.with_i394 else "OFF"
        tc.variables["WITH_OPENNI2"] = "ON" if self.options.with_openni2 else "OFF"
        tc.variables["WITH_PVAPI"] = "ON" if self.options.with_pvapi else "OFF"
        tc.variables["WITH_ARAVIS"] = "ON" if self.options.with_aravis else "OFF"
        tc.variables["WITH_XIMEA"] = "ON" if self.options.with_ximea else "OFF"
        tc.variables["WITH_XINE"] = "ON" if self.options.with_xine else "OFF"
        tc.variables["WITH_LIBERALSENSE"] = "ON" if self.options.with_liberalsense else "OFF"
        tc.variables["WITH_MFX"] = "ON" if self.options.with_mfx else "OFF"
        tc.variables["WITH_GPHOTO2"] = "ON" if self.options.with_gphoto2 else "OFF"
        tc.variables["VIDEOIO_ENABLE_PLUGINS"] = "ON" if self.options.videoio_enable_plugins else "OFF"
        tc.variables["VIDEOIO_PLUGINS"] = self.options.videoio_plugins
        tc.variables["WITH_TBB"] = "ON" if self.options.with_tbb else "OFF"
        tc.variables["WITH_OPENMP"] = "ON" if self.options.with_openmp else "OFF"
        tc.variables["WITH_HPX"] = "ON" if self.options.with_hpx else "OFF"
        tc.variables["WITH_QT"] = self.options.with_qt
        tc.variables["WITH_OPENGL"] = "ON" if self.options.with_opengl else "OFF"
        tc.variables["WITH_PROTOBUF"] = "ON" if self.options.with_protobuf else "OFF"
        tc.variables["BUILD_PROTOBUF"] = "ON" if self.options.build_protobuf else "OFF"
        tc.variables["OPENCV_DNN_OPENCL"] = "ON" if self.options.dnn_opencl else "OFF"
        tc.variables["WITH_OPENVINO"] = "ON" if self.options.with_openvino else "OFF"
        tc.variables["OPENCV_DNN_CUDA"] = "ON" if self.options.dnn_cuda else "OFF"
        tc.variables["WITH_HALIDE"] = "ON" if self.options.with_halide else "OFF"
        tc.variables["WITH_VULKAN"] = "ON" if self.options.with_vulkan else "OFF"
        
        if self.settings.os == "Linux":    
            tc.variables["WITH_GTK"] = "ON" if self.options.with_gtk else "OFF"
            tc.variables["WITH_V4L"] = "ON" if self.options.with_v4l else "OFF"
        elif self.settings.os == "Windows":
            tc.variables["WITH_MSMF"] = "ON" if self.options.with_msmf else "OFF"
            tc.variables["WITH_DSHOW"] = "ON" if self.options.with_dshow else "OFF"
            tc.variables["WITH_WIN32UI"] = "ON" if self.options.with_win32ui else "OFF"

        tc.variables["MIN_VER_CMAKE"] = "3.19"
        tc.generate()

    def build(self):
        cmake = CMake(self)
        cmake.configure(cli_args=["-DCMAKE_POLICY_DEFAULT_CMP0074=NEW"])
        cmake.configure()
        cmake.build()

    def package(self):
        cmake = CMake(self)
        cmake.install()

    def package_info(self):
        self.cpp_info.set_property("cmake_find_mode","none")
        self.cpp_info.builddirs = ["."]
        self.cpp_info.include_dirs = ["include","include/opencv2"]
