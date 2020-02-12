from conans import ConanFile, CMake, tools

class UnmmsmptoolkitConan(ConanFile):
    name = "unmmsmptoolkit"
    version = "1.0.0"
    license = "<Put the package license here>"
    url = "<Package recipe repository url here, for issues about the package>"
    description = "<Description of unmmsmptoolkit here>"
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake"
    exports_sources = "*", "!conanfile.py", "!build*"
    no_copy_source = True
    options = {"with_stlport": [True, False], "read_only":[True, False]}
    default_options = "with_stlport=False", "read_only=False"      
    requires = ("unmutils/1.0.0@core/stable", "unmerrorcode_platform/[~=2.0]@platform/stable")
    
    def requirements(self):
        self.requires("unmslice_platform/1.0.0@platform/%s" % self.channel)
        self.requires("unmslice_msmp/1.0.0@msmp/%s" % self.channel)  
        self.requires("unmplatformapi/1.0.0@platform/%s" % self.channel)  
        self.requires("unmtransaction/1.0.0@msmp/%s" % self.channel)  
        self.requires("unmmsmpdbapi/1.0.0@msmp/%s" % self.channel) 
        self.requires("unmspi/1.0.0@platform/%s" % self.channel) 
        self.requires("unmmsmpservice/1.0.0@msmp/%s" % self.channel) 
        self.requires("unmneservice/1.0.0@msmp/%s" % self.channel) 
        self.requires("unmmsmpspi/1.0.0@msmp/%s" % self.channel)
        self.requires("unmerrorcode_msmp/1.0.0@msmp/%s" % self.channel)
        
    def configure(self):
        self.options["unmutils"].with_stlport = self.options.with_stlport
        self.options["unmslice_platform"].with_stlport = self.options.with_stlport
        self.options["unmslice_msmp"].with_stlport = self.options.with_stlport
        self.options["unmplatformapi"].with_stlport = self.options.with_stlport
        self.options["unmmsmpdbapi"].with_stlport = self.options.with_stlport
        self.options["unmmsmpservice"].with_stlport = self.options.with_stlport
        self.options["unmneservice"].with_stlport = self.options.with_stlport
        self.options["unmtransaction"].with_stlport = self.options.with_stlport

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        self.copy("*.lib", dst="lib", keep_path=False)
        self.copy("*.exe", dst="bin", keep_path=False)
        self.copy("*.dll", dst="bin", keep_path=False)
        self.copy("*.pdb", dst="bin", src="bin", keep_path=False)
        self.copy("*.so", dst="lib", keep_path=False)
        self.copy("*.dylib", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)

