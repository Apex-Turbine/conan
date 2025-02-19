from conan import ConanFile
from conan.tools.cmake import CMakeToolchain, CMake, cmake_layout, CMakeDeps
from conan.tools.files import apply_conandata_patches, export_conandata_patches, get
from conan.tools.files import unzip, copy
import os, sys


class phantomRecipe(ConanFile):
    name = "phantom"
    user="apexturbine"
    channel="stable"
    package_type = "shared-library"
    no_copy_source = True

    # Optional metadata
    url = "http://www.phantomhighspeed.com"
    description = "SDK supporting Phantom High Speed Cameras"
    topics = ("phantom", "highspeed", "computervision")

    # Binary configuration
    settings = "os", "compiler", "build_type", "arch"
    options = {}
    default_options = {}

    libPath = ""
    binPath = ""
    includePath = ""

    def config_options(self):
        pass

    def configure(self):
        pass

    def export_sources(self):
        export_conandata_patches(self)
        copy(self,"*.zip", src=self.recipe_folder, dst=self.export_folder)

    def source(self):
        print(self.conan_data)

    def layout(self):
        cmake_layout(self, src_folder="src")

    def generate(self):
        deps = CMakeDeps(self)
        deps.generate()
        tc = CMakeToolchain(self)
        tc.generate()

    def build(self):
        cpath = os.path.dirname(os.path.realpath(__file__))
        zipfile = f'SDK {self.version}.zip'
        unzip(self, os.path.join(cpath,zipfile), destination='src')
        print(self.conan_data)
        sdkversion = self.conan_data["sources"][self.version]["sdkVersion"]
        tag = self.conan_data["sources"][self.version]["tag"]
        baseFolder = os.path.join('src', f'SDK CD Image {self.version}{tag}', 'Manual Install', f'SDK {sdkversion}')
        self.includePath = os.path.join(baseFolder,f'{self.conan_data["sources"][self.version]["includeFolder"]}')
        osFolder = 'Win64' if self.settings.os == 'Windows' else 'Linux64'
        self.libPath = os.path.join(baseFolder,f'{self.conan_data["sources"][self.version]["libFolder"]}','x64')
        self.binPath = os.path.join(baseFolder,f'{self.conan_data["sources"][self.version]["binFolder"]}',osFolder)

    def package(self):
        print(f'Include Path: {self.includePath}')
        print(f'Lib Path: {self.libPath}')
        print(f'Bin Path: {self.binPath}')
        print(f'Build Folder: {self.build_folder}')
        print(f'Package Folder: {self.package_folder}')

        copy(self,"*.h", dst=os.path.join(self.package_folder,'include','phantom'), src=os.path.join(self.build_folder,self.includePath))
        copy(self,"*.lib", dst=os.path.join(self.package_folder,'lib'), src=os.path.join(self.build_folder,self.libPath))
        copy(self,"*.dll", dst=os.path.join(self.package_folder,"bin"), src=os.path.join(self.build_folder,self.binPath))
        copy(self,"*.Dll", dst=os.path.join(self.package_folder,"bin"), src=os.path.join(self.build_folder,self.binPath))
        copy(self,"*.so", dst=os.path.join(self.package_folder,"lib"), src=os.path.join(self.build_folder,self.libPath))
        copy(self,"*.a", dst=os.path.join(self.package_folder,"lib"), src=os.path.join(self.build_folder,self.libPath))
        

    def package_info(self):
        self.cpp_info.libs = ["PhFile", "PhInt", "PhCon", "PhRange", "PhSig", "PhSigV"]
        self.cpp_info.libdirs = ["lib"]
        self.cpp_info.bindirs = ["bin"]
        self.cpp_info.includedirs = ["include"]
        
    

    
