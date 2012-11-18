/** 
 @cond
 ############################################################################
 # LGPL License                                                             #
 #                                                                          #
 # This file is part of the Machine Learning Framework.                     #
 # Copyright (c) 2010-2012, Philipp Kraus, <philipp.kraus@flashpixx.de>     #
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
 @endcond
 **/

/** interface file for the supervived reduce class,
 * the class must be abstract, so we disable all generator parts
 **/


#ifdef SWIGJAVA
%module "supervicedreduceemodule"

%typemap(javaclassmodifiers) machinelearning::dimensionreduce::supervised::reduce<double, std::string> "public abstract class"
%typemap(javabody)           machinelearning::dimensionreduce::supervised::reduce<double, std::string> ""
%typemap(javafinalize)       machinelearning::dimensionreduce::supervised::reduce<double, std::string> ""
%typemap(javadestruct)       machinelearning::dimensionreduce::supervised::reduce<double, std::string> ""

%typemap(javaclassmodifiers) machinelearning::dimensionreduce::supervised::reduce<double, std::size_t> "public abstract class"
%typemap(javabody)           machinelearning::dimensionreduce::supervised::reduce<double, std::size_t> ""
%typemap(javafinalize)       machinelearning::dimensionreduce::supervised::reduce<double, std::size_t> ""
%typemap(javadestruct)       machinelearning::dimensionreduce::supervised::reduce<double, std::size_t> ""
#endif


%nodefaultctor              machinelearning::dimensionreduce::supervised::reduce<double, std::string>;
%nodefaultdtor              machinelearning::dimensionreduce::supervised::reduce<double, std::string>;

%nodefaultctor              machinelearning::dimensionreduce::supervised::reduce<double, std::size_t>;
%nodefaultdtor              machinelearning::dimensionreduce::supervised::reduce<double, std::size_t>;


%include "reduce.hpp"
%template(ReduceString) machinelearning::dimensionreduce::supervised::reduce<double, std::string>;
%template(ReduceLong) machinelearning::dimensionreduce::supervised::reduce<double, std::size_t>;