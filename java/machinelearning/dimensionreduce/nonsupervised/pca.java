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

package machinelearning.dimensionreduce.nonsupervised;



/** create the principal component analysis (PCA)
 * $LastChangedDate$
 * @see http://download.oracle.com/javase/1.4.2/docs/api/java/lang/System.html#mapLibraryName%28java.lang.String%29
 **/
public class pca<T> extends machinelearning.object implements reduce<T> {
    
    /** private member, that stores the pointer of the native object **/
    private final long cpp_ptr;
    
    
    /** constructor
     * @param p_dim number of target dimensions
     **/
    public pca( int p_dim ) { cpp_ptr = cpp_ctor(p_dim); }
    
    /** finalizer, that calls the disposer with exception handling **/
    protected void finalize() { try { this.dispose(); } catch(Exception e) {} }
    
    
    /** run the mapping structure
     * @param p_data input data / matrix
     * @return project data
     **/
    public native T[][] map( T[][] p_data );
    
    /** returns the project dimension
     * @return number of dimensions
     **/
    public native int getDimension();
    
    /** returns the projection vectors
     * @return array with project vectors
     **/
    public native T[][] getProject();
    
    /** dispose for clearing memory **/
    public native void dispose();
    
    
    /** native ctor method with the return of the pointer
     * @param p_dim dimension
     * @return pointer address
     **/
    private native long cpp_ctor( int p_dim );
    
}
