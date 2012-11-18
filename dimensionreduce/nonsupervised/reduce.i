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

/** interface file for the nonsupervived reduce class,
 * the class must be abstract, so we disable all generator parts
 **/


#ifdef SWIGJAVA
%module "nonsupervicedreduceemodule"

%typemap(javaclassmodifiers) machinelearning::dimensionreduce::nonsupervised::reduce<double> "public abstract class"
%typemap(javabody)           machinelearning::dimensionreduce::nonsupervised::reduce<double> ""
%typemap(javafinalize)       machinelearning::dimensionreduce::nonsupervised::reduce<double> ""
%typemap(javadestruct)       machinelearning::dimensionreduce::nonsupervised::reduce<double> ""
#endif


%nodefaultctor               machinelearning::dimensionreduce::nonsupervised::reduce<double>;
%nodefaultdtor               machinelearning::dimensionreduce::nonsupervised::reduce<double>;


%include "reduce.hpp"
%template(Reduce) machinelearning::dimensionreduce::nonsupervised::reduce<double>;