############################################################################
# LGPL License                                                             #
#                                                                          #
# This file is part of the Machine Learning Framework.                     #
# Copyright (c) 2010, Philipp Kraus, <philipp.kraus@flashpixx.de>          #
# This program is free software: you can redistribute it and/or modify     #
# it under the terms of the GNU Lesser General Public License as           #
# published by the Free Software Foundation, either version 3 of the       #
# License, or (at your option) any later version.                          #
#                                                                          #
# This program is distributed in the hope that it will be useful,          #
# but WITHOUT ANY WARRANTY; without even the implied warranty of           #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the            #
# GNU Lesser General Public License for more details.                      #
#                                                                          #
# You should have received a copy of the GNU Lesser General Public License #
# along with this program. If not, see <http://www.gnu.org/licenses/>.     #
############################################################################

# -*- coding: utf-8 -*-
import os
import urllib2
import re
import shutil
import subprocess
import glob
import sys
Import("*")


#=== help function ===================================================================================================================
def runsyscmd(cmd, env) :
    ret = subprocess.call( cmd, shell=True )
    if ret <> 0 and not(env["skipbuilderror"]) :
        print "\nan error occurred during building"
        res = ""
        while res != "a" and res != "c" :
            res = raw_input("(a)bort or (c)ontinue: ")
            if res == "a" :
                sys.exit(1)
        
                        
def downloadfile(url, file)  :
    if os.path.isfile(file) :
        return
                
    target = open( file, "w" )
    f = urllib2.urlopen(url)
    target.write(f.read())
    target.close()
    f.close()
    
    
def clearbuilddir(target, source, env) :
    clearlist = []
    for i in os.listdir("install") :
        if os.path.isfile(os.path.join("install", i)) :
            continue
        if i <> "build" :
            clearlist.append(i)
    
    for i in clearlist :
        for pathentry in os.walk(os.path.join("install", i), False):
            for dir in pathentry[1]:
                path = os.path.join(pathentry[0], dir)
                if os.path.islink(path):
                    os.unlink(path)
                else:
                    os.rmdir(path)

            for file in pathentry[2]:
                path = os.path.join(pathentry[0], file)
                os.unlink(path)
       
        os.removedirs(os.path.join("install", i))
    
    return []



#=== download packages ===============================================================================================================
def download_boost(target, source, env)  :
    # under Cygwin the BZip2 and ZLib must be installed so we do this first
    if env["PLATFORM"].lower() == "cygwin" :
        # get ZLib
        f = urllib2.urlopen("http://www.zlib.net/")
        html = f.read()
        f.close()

        found = re.search("http://zlib.net/zlib-(.*).tar.gz", html)
        if found == None :
            raise RuntimeError("ZLib Download URL not found")
        downloadfile(found.group(0), os.path.join("install", "zlib.tar.gz"))
       
        # get BZip2
        f = urllib2.urlopen("http://www.bzip.org/downloads.html")
        html = f.read()
        f.close()
        
        found = re.search("<a href=\"/(.*)/bzip2-(.*).tar.gz\">", html)
        if found == None :
            raise RuntimeError("BZip2 Download URL not found")
        
        downloadurl = found.group(0)
        downloadurl = downloadurl.replace("<a href=\"", "")
        downloadurl = downloadurl.replace("\">", "")
        downloadurl = "http://www.bzip.org" + downloadurl
        
        downloadfile(downloadurl, os.path.join("install", "bzip2.tar.gz"))
        

    # read download path of the Boost (latest version)
    f = urllib2.urlopen("http://www.boost.org/users/download/")
    html = f.read()
    f.close()
    
    found = re.search("<a href=\"http://sourceforge.net/projects/boost/files/(.*)\">Download</a>", html)
    if found == None :
        raise RuntimeError("Boost Download URL not found")
        
    downloadurl = found.group(0)
    downloadurl = downloadurl.replace("<a href=\"", "")
    downloadurl = downloadurl.replace("\">Download</a>", "")
    
    # read url of the tar.bz2
    f = urllib2.urlopen(downloadurl)
    html = f.read()
    f.close()

    found = re.search("<a href=\"http://sourceforge.net/projects/boost/files/boost(.*).tar.bz2/download", html)
    if found == None :
        raise RuntimeError("Boost Download URL not found")

    downloadurl = found.group(0)
    downloadurl = downloadurl.replace("<a href=\"", "")

    downloadfile(downloadurl, os.path.join("install", "boost.tar.bz2"))
    return []


def download_hdf(target, source, env) :
    # read download path of the HDF
    f = urllib2.urlopen("http://www.hdfgroup.org/ftp/HDF5/current/src/")
    html = f.read()
    f.close()
    
    found = re.search("<a href=\"(.*)tar.bz2\">", html)
    if found == None :
        raise RuntimeError("HDF Download URL not found")
    downloadurl = found.group(0)

    downloadurl = downloadurl.replace("<a href=\"", "")
    downloadurl = downloadurl.replace("\">", "")
    downloadurl = "http://www.hdfgroup.org/ftp/HDF5/current/src/" + downloadurl

    # download the package
    downloadfile(downloadurl, os.path.join("install", "hdf.tar.bz2"))
    return []


def download_atlaslapack(target, source, env) :
    # read download path of the LAPack (latest version)
    f = urllib2.urlopen("http://www.netlib.org/lapack/")
    html = f.read()
    f.close()
    
    found = re.search("<a href=\"http://www.netlib.org/lapack/(.*)tgz\">", html)
    if found == None :
        raise RuntimeError("LAPack Download URL not found")
        
    downloadurl = found.group(0)
    downloadurl = downloadurl.replace("<a href=\"", "")
    downloadurl = downloadurl.replace("\">", "")
    
    downloadfile(downloadurl, os.path.join("install", "lapack.tgz"))
    downloadfile("http://sourceforge.net/projects/math-atlas/files/latest/download?source=files", os.path.join("install", "atlas.tar.bz2"))
    
    # extract ATLAS tar here, because errors are ignored
    os.system("tar xfvj "+os.path.join("install", "atlas.tar.bz2")+" -C install")
    
    return []


def download_ginaccln(target, source, env) :
    # read download path of the GiNaC (latest version)
    f = urllib2.urlopen("http://www.ginac.de/Download.html")
    html = f.read()
    f.close()
    
    found = re.search("<a href=\"http://www.ginac.de/(.*).tar.bz2\">this link</a>", html)
    if found == None :
        raise RuntimeError("GiNaC Download URL not found")
    
    downloadurl = found.group(0)
    downloadurl = downloadurl.replace("<a href=\"", "")
    downloadurl = downloadurl.replace("\">this link</a>", "")
    
    downloadfile(downloadurl, os.path.join("install", "ginac.tar.bz2"))

    
    # read download path of the CLN (latest version)
    f = urllib2.urlopen("http://www.ginac.de/CLN/")
    html = f.read()
    f.close()
    
    found = re.search("<a href=\"(.*).tar.bz2\">from here</a>", html)
    if found == None :
        raise RuntimeError("CLN Download URL not found")
    
    downloadurl = found.group(0)
    downloadurl = downloadurl.replace("<a href=\"", "")
    downloadurl = "http://www.ginac.de/CLN/" + downloadurl.replace("\">from here</a>", "")
    
    downloadfile(downloadurl, os.path.join("install", "cln.tar.bz2"))
    return []


def download_jsoncpp(target, source, env) :
    downloadfile("http://sourceforge.net/projects/jsoncpp/files/latest/download?source=files", os.path.join("install", "jsoncpp.tar.gz"))
    return []
    

def download_xml(target, source, env) :
    downloadfile("ftp://xmlsoft.org/libxml2/LATEST_LIBXML2", os.path.join("install", "xml.tar.gz"))
    return []


#=== building libraries ==============================================================================================================
def build_boost(target, source, env)  :
    boostpath = glob.glob(os.path.join("install", "boost_*"))
    if boostpath == None or not(boostpath) :
        raise RuntimeError("Boost Build Directory not found")

    boostpath     = boostpath[0]
    
    # extract the version part
    boostversion  = boostpath.replace(os.path.join("install", "boost_"), "")
    boostversion  = boostversion.replace("_", ".")

    # for calling bootstrap.sh change the current work directory
    runsyscmd("cd "+boostpath+"; ./bootstrap.sh", env)
    
    # call the bjam command
    toolset = "gcc"
    if env["PLATFORM"].lower() == "darwin" :
        toolset = "darwin"
        
    # if MPI is set, compile Boost with MPI support
    mpi = ""
    if env["withmpi"] :
        oFile = open(os.path.join(boostpath, "tools", "build", "v2", "user-config.jam"), "a+")
        oFile.write("\n using mpi ;\n")
        oFile.close()
        mpi = "--with-mpi"
            
    # build the Boost (on Cygwin the path to BZip2 and ZLib ist set manually)
    zipprefix = ""
    if env["PLATFORM"].lower() == "cygwin" :
        zipprefix += "export BZIP2_BINARY=bz2; export ZLIB_BINARY=z; "
        
        zlibpath = glob.glob(os.path.join("install", "build", "zlib", "*"))
        if zlibpath == None or not(zlibpath) :
            raise RuntimeError("ZLib Install Directory not found")
        zlibpath = zlibpath[0]
            
        zipprefix += "export ZLIB_INCLUDE="+os.path.abspath(os.path.join(zlibpath, "include"))+"; "
        zipprefix += "export ZLIB_LIBPATH="+os.path.abspath(os.path.join(zlibpath, "lib"))+"; "
        
        bzippath = glob.glob(os.path.join("install", "build", "bzip2", "*"))
        if bzippath == None or not(bzippath) :
            raise RuntimeError("ZLib Install Directory not found")
        bzippath = bzippath[0]

        zipprefix += "export BZIP2_INCLUDE="+os.path.abspath(os.path.join(bzippath, "include"))+"; "
        zipprefix += "export BZIP2_LIBPATH="+os.path.abspath(os.path.join(bzippath, "lib"))+"; "
    
    runsyscmd(zipprefix+"cd "+boostpath+"; ./b2 "+mpi+" --with-exception --with-filesystem --with-math --with-random --with-regex --with-date_time --with-thread --with-system --with-program_options --with-serialization --with-iostreams --disable-filesystem2 threading=multi runtime-link=shared variant=release toolset="+toolset+" install --prefix="+os.path.abspath(os.path.join("install", "build", "boost", boostversion)), env)

    # checkout the numerical binding
    runsyscmd("svn checkout http://svn.boost.org/svn/boost/sandbox/numeric_bindings/ "+os.path.join("install", "build", "boost", "sandbox", "numeric_bindings"), env )

    return []
    
    
def build_zlib(target, source, env) :
    zlibpath = glob.glob(os.path.join("install", "zlib-*"))
    if zlibpath == None or not(zlibpath) :
        raise RuntimeError("ZLib Build Directory not found")

    zlibpath     = zlibpath[0]
    zlibversion  = zlibpath.replace(os.path.join("install", "zlib-"), "")

    # the "make install" creates problems under Cygwin so do it manually
    runsyscmd( "cd "+zlibpath+"; ./configure --prefix="+os.path.abspath(os.path.join("install", "build", "zlib", zlibversion))+ "; make", env )
    
    # do install and copy headerfiles
    os.system( "cd "+zlibpath+"; make install" )
    
    try :
        os.makedirs(os.path.join("install", "build", "zlib", zlibversion, "include"))
    except :
        pass
    try :
        headerfiles = glob.glob(os.path.join(zlibpath, "*.h"))
        for i in headerfiles :
            shutil.copyfile(i, os.path.join("install", "build", "zlib", zlibversion, "include", os.path.basename(i)))
    except :
        pass
    return []
    

def build_bzip2(target, source, env) :
    bzippath = glob.glob(os.path.join("install", "bzip2-*"))
    if bzippath == None or not(bzippath) :
        raise RuntimeError("BZip2 Build Directory not found")

    bzippath     = bzippath[0]
    bzipversion  = bzippath.replace(os.path.join("install", "bzip2-"), "")

    runsyscmd( "cd "+bzippath+"; make; make install PREFIX="+os.path.abspath(os.path.join("install", "build", "bzip2", bzipversion)), env )
    return []
    
    
def build_hdf(target, source, env) :
    hdfpath = glob.glob(os.path.join("install", "hdf?-*"))
    if hdfpath == None or not(hdfpath) :
        raise RuntimeError("HDF Build Directory not found")

    hdfpath     = hdfpath[0]
    hdfversion  = hdfpath.replace(os.path.join("install", "hdf"), "")

    runsyscmd( "cd "+hdfpath+"; ./configure --enable-cxx --prefix="+os.path.abspath(os.path.join("install", "build", "hdf", hdfversion))+ "; make; make install", env )
    return []
    

def build_atlaslapack(target, source, env) :
    f = urllib2.urlopen("http://sourceforge.net/projects/math-atlas/files/")
    html = f.read()
    f.close()

    found = re.search("<small title=\"(.*)tar.bz2\">(.*)</small>", html)
    if found == None :
        raise RuntimeError("ATLAS Version can not be detected")

    atlasversion = found.group(2)
    atlasversion = atlasversion.replace("atlas", "")
    atlasversion = atlasversion.replace(".tar.bz2", "")

    ptrwidth = ""
    if env["atlaspointerwidth"] == "32" :
        ptrwidth = "-b 32"
    elif env["atlaspointerwidth"] == "64" :
        ptrwidth = "-b 64"

    cputhrottle = ""
    if not(env["atlascputhrottle"]) :
        cputhrottle = "-Si cputhrchk 0"
    
    runsyscmd( "cd "+os.path.join("install", "atlasbuild")+"; ../ATLAS/configure --dylibs "+ptrwidth+" "+cputhrottle+" --with-netlib-lapack-tarfile=../lapack.tgz --prefix="+os.path.abspath(os.path.join("install", "build", "atlas", atlasversion))+ "; make", env )
    return []
    
    
def soname_atlaslapack(target, source, env) :
    oFile = open( os.path.join("install", "atlasbuild", "lib", "Makefile"), "r" )
    makefile = oFile.read()
    oFile.close()
    
    makefile = makefile.replace("(LD) $(LDFLAGS) -shared -soname $(LIBINSTdir)/$(outso) -o $(outso)", "(LD) $(LDFLAGS) -shared -soname $(outso) -o $(outso)")

    oFile = open( os.path.join("install", "atlasbuild", "lib", "Makefile"), "w" )
    oFile.write(makefile)
    oFile.close()

    return []


def install_atlaslapack(target, source, env) :
    runsyscmd( "cd "+os.path.join("install", "atlasbuild")+"; make shared; make install", env )
    return []
    
    
def build_ginaccln(target, source, env) :
    clnpath = glob.glob(os.path.join("install", "cln-*"))
    if clnpath == None or not(clnpath) :
        raise RuntimeError("CLN Build Directory not found")
    
    clnpath     = clnpath[0]
    clnversion  = clnpath.replace(os.path.join("install", "cln-"), "")
    
    ginacpath = glob.glob(os.path.join("install", "ginac-*"))
    if ginacpath == None or not(ginacpath) :
        raise RuntimeError("GiNaC Build Directory not found")
    
    ginacpath     = ginacpath[0]
    ginacversion  = ginacpath.replace(os.path.join("install", "ginac-"), "")

    runsyscmd( "cd "+clnpath+"; ./configure --prefix="+os.path.abspath(os.path.join("install", "build", "cln", clnversion))+ "; make; make install", env )
    runsyscmd( "cd "+ginacpath+"; export CLN_CFLAGS=-I"+os.path.abspath(os.path.join("install", "build", "cln", clnversion, "include"))+"; export CLN_LIBS=\"-L"+os.path.abspath(os.path.join("install", "build", "cln", clnversion, "lib"))+" -lcln\"; ./configure --prefix="+os.path.abspath(os.path.join("install", "build", "ginac", ginacversion))+ "; make; make install", env )
    return []


def build_jsoncpp(target, source, env) :
    jsonpath = glob.glob(os.path.join("install", "jsoncpp-src-*"))
    if jsonpath == None or not(jsonpath) :
        raise RuntimeError("JSON CPP Build Directory not found")

    jsonpath     = jsonpath[0]
    jsonversion  = jsonpath.replace(os.path.join("install", "jsoncpp-src-"), "")
    
    #on cygwin the SConstruct file must be changed, otherwise it creates a build error
    if env["PLATFORM"].lower() == "cygwin" :
        oFile = open( os.path.join(jsonpath, "SConstruct"), "r" )
        makefile = oFile.read()
        oFile.close()
    
        makefile = makefile.replace("buildProjectInDirectory( 'src/jsontestrunner' )", "")
        makefile = makefile.replace("buildProjectInDirectory( 'src/test_lib_json' )", "")

        oFile = open( os.path.join(jsonpath, "SConstruct"), "w" )
        oFile.write(makefile)
        oFile.close()
    

    
    runsyscmd("cd "+jsonpath+"; scons platform=linux-gcc", env)
    
    # manual copy of the data
    try :
        os.makedirs(os.path.join("install", "build", "jsoncpp", jsonversion))
    except :
        pass
    try :
        os.makedirs(os.path.join("install", "build", "jsoncpp", jsonversion, "lib"))
    except :
        pass
    try :
        shutil.copytree(os.path.join(jsonpath, "include"), os.path.join("install", "build", "jsoncpp", jsonversion, "include"))
    except :
        pass

    files = []
    files.extend( glob.glob(os.path.join(jsonpath, "libs", "**", "*"+env["SHLIBSUFFIX"])) )
    files.extend( glob.glob(os.path.join(jsonpath, "libs", "**", "*"+env["LIBSUFFIX"])) )
    installpath = os.path.join("install", "build", "jsoncpp", jsonversion, "lib")
    for i in files :
        filename =os.path.split(i)[-1]
        shutil.copy(i, os.path.join(installpath, filename))
        os.symlink(os.path.join("./", filename), os.path.join(installpath, "libjson" + os.path.splitext(filename)[1]))

    return []
    
    
def build_xml(target, source, env) :
    xmlpath = glob.glob(os.path.join("install", "libxml2-*"))
    if xmlpath == None or not(xmlpath) :
        raise RuntimeError("XML Build Directory not found")
    
    xmlpath     = xmlpath[0]
    xmlversion  = xmlpath.replace(os.path.join("install", "libxml2-"), "")
    
    runsyscmd( "cd "+xmlpath+"; ./configure --prefix="+os.path.abspath(os.path.join("install", "build", "xml2", xmlversion))+ "; make; make install", env )
    return []


#=== configuration ===================================================================================================================
def showconfig(target, source, env) :
    #detect builded packages and shows PATH, CPPPATH, LIBRARY_PATH for installation
    includes = glob.glob(os.path.join("install", "build", "**", "**", "include"))
    
    #replace "install/build" to "<installation dir>"
    cpppath = []
    for i in includes :
        cpppath.append( os.path.join("<installation dir>", os.path.sep.join(i.split(os.path.sep)[2:])) )
        
    # detect Boost Numeric Bindings
    if os.path.isdir( os.path.join("install", "build", "boost", "sandbox", "numeric_bindings") ) :
        cpppath.append( os.path.join("<installation dir>", "boost", "sandbox", "numeric_bindings") )
        
        
    libs = glob.glob(os.path.join("install", "build", "**", "**", "lib"))
    libpath = []
    for i in libs :
        libpath.append( os.path.join("<installation dir>", os.path.sep.join(i.split(os.path.sep)[2:])) )
    
    # on Cygwin some "bin" directories must be added to the library path
    if env["PLATFORM"].lower() == "cygwin" :
        libs = glob.glob(os.path.join("install", "build", "**", "**", "bin"))
        for i in libs :
            path = i.split(os.path.sep)[2:];
            if path[0] == "boost" or path[0] == "xml2" :
                libpath.append( os.path.join("<installation dir>", os.path.sep.join(path)) )
    
        
    print "--------------------------------------------------------------------------"
    print "Warning: move the install/build directory out of the framework directory,"
    print "because the a clean target remove the compiled libraries"
    print "add the following variables / content to your environment and replace"
    print "<installation dir> to the directory path whitch stores the build directory"
    print "\n"
    print "CPPPATH="+os.pathsep.join(cpppath)
    print ""
    
    if env["PLATFORM"].lower() == "cygwin" :
        print "PATH="+os.pathsep.join(libpath)
    else :
        print "LIBRARY_PATH="+os.pathsep.join(libpath)
    
    if env["PLATFORM"].lower() == "darwin" :
        print ""
        print "it is recommand to add the following line to your /etc/profile or ~/.profile"
        print "export DYLD_LIBRARY_PATH=$LIBRARY_PATH"
    elif env["PLATFORM"].lower() == "cygwin" :
        print ""
        print "add also Cygwin bin directory to the path for using compiled program outside of Cygwin"
    
    print "--------------------------------------------------------------------------"
    return []

#=== target structure ================================================================================================================
skiplist = str(env["skipbuild"]).split(",")
if ("librarybuild" in COMMAND_LINE_TARGETS) and ("all" in skiplist) :
    raise RuntimeError("nothing to build")

#build into a temp dir
lst = []
lst.append( env.Command("mkinstalldir", "", Mkdir("install")) )
lst.append( env.Command("mkbuilddir", "", Mkdir(os.path.join("install", "build"))) )

#clear install directories before compiling
lst.append( env.Command("cleanbeforebuilddir", "", clearbuilddir) )

#download LAPack & ATLAS, extract & install
if not("atlas" in skiplist) :
    lst.append( env.Command("downloadlapackatlas", "", download_atlaslapack) )
    lst.append( env.Command("mkatlasbuilddir", "", Mkdir(os.path.join("install", "atlasbuild"))) )
    lst.append( env.Command("buildatlaslapack", "", build_atlaslapack) )
    if env["PLATFORM"].lower() == "posix" or env["PLATFORM"].lower() == "cygwin" :
        lst.append( env.Command("sonameatlaslapack", "", soname_atlaslapack) )
    lst.append( env.Command("installatlaslapack", "", install_atlaslapack) )

# download Boost, extract & install
if not("boost" in skiplist) :
    lst.append( env.Command("downloadboost", "", download_boost) )
    if env["PLATFORM"].lower() == "cygwin" :
        lst.append( env.Command("extractzlib", "", "tar xfvz "+os.path.join("install", "zlib.tar.gz")+" -C install") )
        lst.append( env.Command("buildzlib", "", build_zlib) )
        lst.append( env.Command("extractbzip2", "", "tar xfvz "+os.path.join("install", "bzip2.tar.gz")+" -C install") )
        lst.append( env.Command("buildbzip2", "", build_bzip2) )
    lst.append( env.Command("extractboost", "", "tar xfvj "+os.path.join("install", "boost.tar.bz2")+" -C install") )
    lst.append( env.Command("buildboost", "", build_boost) )

# download HDF, extract & install
if not("hdf" in skiplist) :
    lst.append( env.Command("downloadhdf", "", download_hdf) )
    lst.append( env.Command("extracthdf", "", "tar xfvj "+os.path.join("install", "hdf.tar.bz2")+" -C install") )
    lst.append( env.Command("buildhdf", "", build_hdf) )

#download GiNaC & CLN, extract & install
if not("ginac" in skiplist) :
    lst.append( env.Command("downloadginaccln", "", download_ginaccln) )
    lst.append( env.Command("extractginac", "", "tar xfvj "+os.path.join("install", "ginac.tar.bz2")+" -C install") )
    lst.append( env.Command("extractcln", "", "tar xfvj "+os.path.join("install", "cln.tar.bz2")+" -C install") )
    lst.append( env.Command("buildginaccln", "", build_ginaccln) )

#download JSON library, extract & install
if not("json" in skiplist) :
    lst.append( env.Command("downloadjsoncpp", "", download_jsoncpp) )
    lst.append( env.Command("extractjsoncpp", "", "tar xfvz "+os.path.join("install", "jsoncpp.tar.gz")+" -C install") )
    lst.append( env.Command("buildjsoncpp", "", build_jsoncpp) )
    
# download libxml2, extract & install (only cygwin)
if env["PLATFORM"].lower() == "cygwin" and not("xml" in skiplist) :
    lst.append( env.Command("downloadxml", "", download_xml) )
    lst.append( env.Command("extractjsoncpp", "", "tar xfvz "+os.path.join("install", "xml.tar.gz")+" -C install") )
    lst.append( env.Command("buildxml", "", build_xml) )


#clear install directories after compiling
lst.append( env.Command("cleanafterbuilddir", "", clearbuilddir) )

#show the config path
lst.append( env.Command("showconfig", "", showconfig) )


env.Alias("librarybuild", lst)