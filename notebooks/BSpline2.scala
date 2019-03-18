
//:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
/** @author  Michael Cotterell
 *  @version 1.4
 *  @date    Fri Nov 18 21:45:58 EDT 2017
 *  @see     LICENSE (MIT style license file).
 */

import scalation.linalgebra.{MatrixD, VectorD}
import scalation.math.double_exp
import scalation.stat.Statistic
import scalation.util.{timed, Error}

//:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
/** The `BSpline2` class provides B-Spline basis functions for various orders 'm',
 *  where the order is one more than the degree.  A spline function is a piecewise
 *  polynomial function where the pieces are stitched together at knots with the
 *  goal of maintaining continuity and differentability.  B-Spline basis functions
 *  form a popular form of basis functions used in Functional Data Analysis.
 * 
 *  @see [[http://web.mit.edu/hyperbook/Patrikalakis-Maekawa-Cho/node15.html `PMC2009`]]
 *  @see [[http://en.wikipedia.org/wiki/B-spline "B-spline" on Wikipedia]]
 * 
 *  @param T  the time-points of the original knots in the time dimension
 *  @param k  the maximum order, allowing splines orders from 1 to k
 */
class BSpline2 (T: VectorD, k: Int = 4, isCardinal: Boolean = false) extends Error {

    protected val head = T(0)            // first knot
    protected val tail = T(T.dim - 1)    // last knot

    /** Evaluates each of the `T.dim-m`-many order `m+1` B-spline basis
     *  functions at `t` for `1 <= (m+1) <= k` non-recursively, using an 
     *  efficient dynamic programming approach. 
     *  @param t  point to evaluate
     *  @author Michael Cotterell
     *  @see Carl de Boor (1978). A Practical Guide to Splines. Springer-Verlag. ISBN 3-540-90356-9.
     */    
    def eval (k: Int = this.k) (t: Double): Array[VectorD] = {
        // NOTE: k shadows this.k
        val N = Array.ofDim [VectorD] (k) // array of basis function coefficients
        for (m <- 0 until k) {
            val nc = T.dim - m - 1        // number of knots/control points
            val nf = nc                   // number of basis functions of order K
            N(m)   = new VectorD (nf)     // evaluations for order K
            if      (t =~ head) N(m)(   0) = 1.0
            else if (t =~ tail) N(m)(nc-1) = 1.0
            else if (m == 0) {
                for (i <- 0 until nf-1) {
                    N(m)(i) = if ((T(i) < t || T(i) =~ t) && (t < T(i+1))) 1.0 else 0.0
                } // for
            } else if (m > 0) {
                for (i <- 0 until nf) {
                    val bs1 = N(m-1)(i)  
                    val bs2 = N(m-1)(i+1)
                    // using "== 0" instead of "=~ 0" should be safe                    
                    val bf1 = if (bs1 == 0) 0 else (t - T(i)) * bs1 / (T(i+m) - T(i))
                    val bf2 = if (bs2 == 0) 0 else (T(i+m+1) - t) * bs2 / (T(i+m+1) - T(i+1))
                    N(m)(i) = bf1 + bf2
                } // for
            } // if
        } // for  
        N
    } // eval

    /** Evaluates each of the `T.dim-1`-many order `k` B-spline basis functions 
     *  at `t` non-recursively, using an efficient dynamic programming approach.
     * 
     *  ==Example==
     *  {{{
     *  val k = 4                     // order k (degree k-1)
     *  val t = VectorD (1, 2, 3, 4)  // original time points
     *  val T = BSpline2.clamp (k, t) // let knots be a clamped version of T
     *  val N = BSpline2 (T, k)       // BSpline2 instance
     *  val z = N.evalFast (t)        // vector of evaluations
     *  println (s"order $k basis functions at $t = $z")
     *  }}}
     * 
     *  ==Implementation Details==
     *  Let `N(k)(i)` denote the `i`-th order `k` basis function evaluated at
     *  `t`. Then each `N(k)(i)` depends on the evaluation of `N(k-1)(i)` and 
     *  `N(k-1)(i+1)`. Here is an example, given a set of order `k=4` B-spline
     *  basis functions and knot vector `T` of length `n`:
     *  {{{
     *  N(1)(0), N(1)(1), N(1)(2), N(1)(3), ..., N(1)(n-1)
     *        |/       |/       |/            |/
     *  N(2)(0), N(2)(1), N(2)(2), ..., N(2)(n-2)
     *        |/       |/            |/
     *  N(3)(0), N(3)(1), ..., N(3)(n-3)
     *        |/            |/
     *  N(4)(0), ..., N(4)(n-4)
     *  }}}
     *  This algorithm applies the procedure described above using O(n)
     *  storage and O(k*n) floating point operations. 
     * 
     *  ==TODO==
     *  Further speedup should be achievable when the knot vector `T` is 
     *  uniform, since that would result in "cardinal" B-spline basis 
     *  functions. In that case, we can compute `N(k)(i)` using O(n)
     *  storage and O(n) floating point operations.
     * 
     *  @param t  point to evaluate
     *  @author Michael Cotterell
     *  @see Carl de Boor (1978). A Practical Guide to Splines. Springer-Verlag. ISBN 3-540-90356-9.
     */
    def evalFast (k:Int = this.k) (t: Double): VectorD = {
        // NOTE: k shadows this.k
        val N = Array.ofDim [Double] (T.dim-1) // all evaluatons; overwrite as needed
        for (m <- 0 until k) {                 // build for each order 1 <= (m+1) <= k
            val nf = T.dim - m - 1             // number of basis funftions for order (m+1)
            if      (t =~ head) N(   0) = 1.0  // trivial case: near first knot
            else if (t =~ tail) N(nf-1) = 1.0  // trivial case: near last knot
            else if (m == 0) {                 // evaluate order 1
                for (i <- 0 until nf-1) {
                    N(i) = if ((T(i) < t || T(i) =~ t) && (t < T(i+1))) 1.0 else 0.0
                } // for
            } else if (m > 0) {                // evaluate orders (m+1) <= k
                for (i <- 0 until nf) {
                    val bs1 = N(i)             
                    val bs2 = N(i+1)
                    // using "== 0" instead of "=~ 0" should be safe
                    val bf1 = if (bs1 == 0) 0 else (t - T(i)) * bs1 / (T(i+m) - T(i))
                    val bf2 = if (bs2 == 0) 0 else (T(i+m+1) - t) * bs2 / (T(i+m+1) - T(i+1))
                    N(i) = bf1 + bf2
                } // for
            } // if
        } //  for  
        new VectorD (T.dim - k, N) // do not allocate new storage         
    } // evalFast

    def apply (m: Int = k) (i: Int) (t: Double): Double =
    {
        val bs = eval(m)(t).last
        bs (i)
    } // apply

    def apply (m: Int, t: Double): VectorD =
    {
        val bs = eval(m)(t).last
        bs 
    } // apply

    def apply (m: Int, vt: VectorD): MatrixD =
    {
        MatrixD(for (j <- vt.indices) yield apply(m, vt(j)), false)
    } // apply

    def applyFast (vt: VectorD): MatrixD =
    {
        MatrixD(for (j <- vt.indices) yield evalFast(k)(vt(j)), false)
    } // applyFast

    def derivative (m: Int = k) (n: Int, i: Int) (t: Double): Double =
    {
        val dbs = derivative (m, n, t)
        dbs (i)
    } // derivative

    // TODO - implement non-recursively
    def derivative (m: Int, n: Int, t: Double): VectorD =
    {
        val N = eval(m)(t) // slow
        if (n == 0) N (m-1)
        else {
            val dN  = new VectorD (N(m-1).dim)
            val dbs = derivative (m-1, n-1, t)
            for (i <- 1 until dN.dim-1) {
                val dbs1 = dbs (i)
                val dbs2 = dbs (i+1)
                val l    = if (dbs1 =~ 0) 0 else (k - 1) * dbs1 / (T(i+k-1) - T(i))
                val r    = if (dbs2 =~ 0) 0 else (k - 1) * dbs2 / (T(i+k) - T(i+1))
                dN(i) = l - r
            } // for
            dN
        } // if
    } // derivative

    def derivative (m: Int, n: Int, vt: VectorD): MatrixD =
    {
        MatrixD (for (j <- vt.indices) yield derivative(m, n, vt(j)), false)
    } // derivative

    def derivative (n: Int, vt: VectorD): MatrixD = derivative (k, n, vt)

    /** Evaluates the `n`-th derivative of each basis function at `t`.
     *  
     *  ==Implementation==
     *  Let `dN(n)(k)(i)` denote the `n`-th derivative of the `i`-th B-spline
     *  basis function of order `k` (degree `k-1`). Here is an example, given a 
     *  set of order `k=4` B-spline basis functions and knot vector `T` of 
     *  length `n`:
     *  {{{
     *      N(2)(0),     N(2)(1),     N(2)(2), ...,     N(2)(n-2) // order 2 at t
     *  dN(0)(2)(0), dN(0)(2)(1), dN(0)(2)(2), ..., dN(0)(2)(n-2) // use N for this row 
     *            |/           |/                  /
     *  dN(1)(3)(0), dN(1)(3)(1), ..., dN(1)(3)(n-3)
     *            |/                  /
     *  dN(2)(4)(0), ..., dN(2)(4)(n-4)
     *  }}}
     */
    def derivativeFast (k: Int = this.k) (n: Int, t: Double): VectorD =
    {
        val dN = evalFast (k-n)(t) // base case
        for (d <- 1 to n) {
            val m  = k - n + d     // effective order (m+1)
            val nf = T.dim - m     // number of basis funftions for order m
            // NOTE: I've not seen anyone else handle the first and last knot this way...
            if      (t =~ head) dN(   0) = 0 // if (d % 2 == 0) Double.MinValue else Double.MaxValue // trivial case: near first knot
            else if (t =~ tail) dN(nf-1) = 0 // if (d % 2 == 0) Double.MaxValue else Double.MinValue // trivial case: near last knot
            else {
                for (i <- 0 until nf) {
                    val d1 = dN (i)
                    val d2 = dN (i+1)
                    val l  = if (d1 == 0) 0 else (m - 1) * d1 / (T(i+m-1) - T(i))
                    val r  = if (d2 == 0) 0 else (m - 1) * d2 / (T(i+m) - T(i+1))
                    dN(i) = l - r
                } // for
            } // if 
        } // for
        new VectorD (T.dim - k, dN().array)
    } // derivativeFast

    //:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::    
    /** Returns the number of basis functions of order `k` given the knot
     *  vector `T` for this `BSpline2` instance.
     *  @param m  order (degree = m-1) (default = k)
     */
    def count (m: Int = k): Int = T.dim - m

} // BSpline2 class

//:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
/** Companion object for `BSpline2` class.
 */
object BSpline2Util {

    /** Returns a "clamped" version of the input vector, augmented to ensure
     *  that each end has `k`-many repeated points. If `isInclusive` is true,
     *  then the first and last values of the vector are repeated; otherwise,
     *  the values `t(0)-EPSILON` and `t(t.dim-1)+EPSILON` are repreated for
     *  the beginning and end, respectively. 
     *  @param k            intended B-spline order (degree = k - 1)
     *  @param t            non-decreasing vector of time points
     *  @param isInclusive  repeat end points (default = true)
     */
    def clamp (k: Int, t: VectorD, isInclusive: Boolean = true): VectorD =
    {
        val e    = scalation.math.ExtremeD.EPSILON
        val head = t(0)
        val tail = t(t.dim-1)
        if (isInclusive) VectorD.fill (k-1)(head) ++ t ++ VectorD.fill (k-1)(tail)
        else             VectorD.fill (k)(head-e) ++ t ++ VectorD.fill (k)(tail+e)
    } // clamp

} // BSpline2Util object
