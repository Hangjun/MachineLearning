/** 
 @cond
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
 @endcond
 **/


#include <cstdlib>
#include <machinelearning.h>
#include <boost/numeric/ublas/vector.hpp>
#include <boost/program_options/parsers.hpp>
#include <boost/program_options/variables_map.hpp>
#include <boost/program_options/options_description.hpp>

namespace po        = boost::program_options;
namespace ublas     = boost::numeric::ublas;
namespace tools     = machinelearning::tools;
namespace ga        = machinelearning::geneticalgorithm;


/** main program for using the genetic algorithm to solve
 * the binary packing problem (Knapsack problem)
 * @param argc number of arguments
 * @param argv arguments
 **/
int main(int argc, char* argv[]) {
    
    std::size_t l_populationsize;
    std::size_t l_elitesize;
    std::size_t l_iteration;
    double l_packsize;
    double l_mutation;
    
    
    // create CML options with description
    po::options_description l_description("allowed options");
    l_description.add_options()
        ("help", "produce help message")
        ("packs", po::value< std::vector<double> >()->multitoken(), "weights / costs of the different packs")
        ("maxpacksize", po::value<double>(&l_packsize), "maximum pack size")
        ("population", po::value<std::size_t>(&l_populationsize)->default_value(50), "population size / number of individuals")
        ("elite", po::value<std::size_t>(&l_elitesize)->default_value(10), "elite size / number of individuals that are elite")
        ("iteration", po::value<std::size_t>(&l_iteration)->default_value(10), "number of iterations")
        ("mutation", po::value<double>(&l_mutation)->default_value(0.35), "mutation probability")
    ;
    
    po::variables_map l_map;
    po::positional_options_description l_input;
    po::store(po::command_line_parser(argc, argv).options(l_description).positional(l_input).run(), l_map);
    po::notify(l_map);
    
    if (l_map.count("help")) {
        std::cout << l_description << std::endl;
        return EXIT_SUCCESS;
    }
    
    if ( (!l_map.count("packs")) || (!l_map.count("maxpacksize")) )  {
        std::cout << "[--packs] and [--maxpacksize] must be set" << std::endl;
        return EXIT_FAILURE;
    }
    
    if (l_map["packs"].as< std::vector<double> >().size() < 2) {
        std::cout << "[--packs] must be greater or equal two" << std::endl;
        return EXIT_FAILURE;
    }
    
    
    //http://www.learncpp.com/cpp-tutorial/121-pointers-and-references-to-the-base-class-of-derived-objects/
    // genetic algorithm
    ublas::vector<double> l_packs = tools::vector::copy(l_map["packs"].as< std::vector<double> >());
    
    ga::binaryindividual<std::size_t> l_individual( l_packs.size() );
    ga::population<double,std::size_t> l_population(l_individual, l_populationsize, l_elitesize);
    
    
    return EXIT_SUCCESS;
    
}
