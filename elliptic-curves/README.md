# Chapter 5: Elliptic Curves

Also see this <https://curves.xargs.org/> for great animations, especially about Chord & Tangent rule. Furthermore, I have drawn the example TinyJubJub curves in WolframAlpha:

- [Short Weierstrass](https://www.wolframalpha.com/input?i2d=true&i=Power%5By%2C2%5D%3DPower%5Bx%2C3%5D%2B+8x+%2B8+for+x%5C%2844%29y+in+GF%5C%2840%2913%5C%2841%29)
- [Montgomery](https://www.wolframalpha.com/input?i2d=true&i=7Power%5By%2C2%5D%3DPower%5Bx%2C3%5D%2B6Power%5Bx%2C2%5D%2Bx+for+x%5C%2844%29+y+in+GF%5C%2840%2913%5C%2841%29)
- [Twisted Edwards](https://www.wolframalpha.com/input?i2d=true&i=3Power%5Bx%2C2+%5D%2B+Power%5By%2C2%5D+%3D+1+%2B+8+Power%5Bx%2C2%5D+Power%5By%2C2%5D+for+x%5C%2844%29+y+in+GF%5C%2840%2913%5C%2841%29)

Some commonly used curves in this section:

- [alt_bn128](https://github.com/scipr-lab/libff/blob/master/libff/algebra/curves/alt_bn128/alt_bn128.sage) (also known as [BN254](https://neuromancer.sk/std/bn/bn254))
- [secp256k1](https://neuromancer.sk/std/secg/secp256k1)
- [bls12-381](https://neuromancer.sk/std/bls/BLS12-381)

## Exercise 58

> Compute the set of all points $(x, y) \in E_{1, 1}(\mathbb{F}_5)$ from example 70.

Using Sage, we can check for pairs of field elements that satisfy the curve equation. The set of all points is shown below, with the point at infinity included.



```python
from sage.all import GF

F5 = GF(5)
points = ["O"]  # point at infinity
for x in F5:
    for y in F5:
        if y**2 == x**3 + x + 1:
            points.append((x, y))  # type: ignore
print(points)
print(len(points), "points")
```

    ['O', (0, 1), (0, 4), (2, 1), (2, 4), (3, 1), (3, 4), (4, 2), (4, 3)]
    9 points


## Exercise 60

> Look up the definition of curve BLS12-381, implement it in Sage, and compute the number of all curve points.



```python
from sage.all import EllipticCurve

# https://neuromancer.sk/std/bls/BLS12-381
p = 0x1A0111EA397FE69A4B1BA7B6434BACD764774B84F38512BF6730D2A0F6B0F6241EABFFFEB153FFFFB9FEFFFFFFFFAAAB
E = EllipticCurve(GF(p), [0, 4])

base_order, scalar_order = E.base_field().order(), E.order()
print("Base Field Order: ({1} bits)\n{0}".format(base_order, base_order.nbits()))
print("Scalar Field Order: ({1} bits)\n{0}".format(scalar_order, scalar_order.nbits()))
```

    Base Field Order: (381 bits)
    4002409555221667393417789825735904156556882819939007885332058136124031650490837864442687629129015664037894272559787
    Scalar Field Order: (381 bits)
    4002409555221667393417789825735904156556882819939007885332058136124031650490837864442687629129030796414117214202539


The number of all curve points is given by the scalar field order, which is 4002409555221667393417789825735904156556882819939007885332058136124031650490837864442687629129030796414117214202539.

## Exercise 61

> Let $\mathbb{F}$ be a finite field, let $(a, b)$ and $(a', b')$ be two pairs of parameters, and let $c \in \mathbb{F}^*$ be an invertible field element such that $a' = a \cdot c^4$ and $b' = b \cdot c^6$ hold. Show that the function $I$ from equation (5.3) maps curve points onto curve points.

Let us write $x' := c^2 \cdot x$ and $y' := c^3 \cdot y$ as well as $a'$ and $b'$ in the curve equation:

$$
(c^3 \cdot y)^2 = (c^2 \cdot x)^3 + (c^4 \cdot a)(c^2 \cdot x) + (c^6 \cdot b)
$$

$$
c^6 \cdot y^2 = c^6 \cdot x^3 + c^6 \cdot a \cdot x + c^6 \cdot b
$$

Notice how we have $c^6$ on both sides, and we are told that $c$ has a multiplicative inverse, and therefore we can compute $c^{-6} = (c^{-1})^6$ and multiply both sides with it to obtain:

$$
y^2 = x^3 + a \cdot x + b
$$

which is our original curve equation, thus showing that the points are mapped onto curve points.

## Exercise 62 ✨

> Consider $TJJ_{13}$ example 71 and the curve $E_{7, 5}(\mathbb{F}_{13})$ defined as follows:
>
> $$
> E_{5, 7}(\mathbb{F}_{13})
> =    \{(x, y) \in \mathbb{F}_{13} \times \mathbb{F}_{13}
> \mid y^2 = x^3 + 7x + 5\}
> $$
>
> Show that $TJJ_{13}$ and $E_{7, 5}(\mathbb{F}_{13})$ are isomorphic. Compute the set of all points from $E_{7, 5}(\mathbb{F}_{13})$, construct $I$ and map all points of $TJJ_{13}$ onto $E_{7, 5}(\mathbb{F}_{13})$

Let's remember the TinyJubJub curve over field of prime order 13:

$$
TJJ_{13} = \{(x, y) \in \mathbb{F}_{13} \times \mathbb{F}_{13} \mid y^2 = x^3 + 8x + 8\}
$$

If we can find a $c \in \mathbb{F}_{13}^*$ such that $7 = 8 \times c^4$ (for $a$) and $5 = 8 \times c^6$ (for $b$); then, as shown in exercise 61, we would have an isomorphism and a mapping from TinyJubJub to the other curve.

The inverse of 8 in this field is 5, so lets multiply both sides with it in both equations to obtain $9 = c^4$ and $12 = c^6$. From this, we get $12 = 9 \times c^2$ and find $c^2 = 10$. Turns out that $6 \times 6 \equiv 10 \pmod{13}$ so $c = 6$ is a square root, as well as $c = 13 - 6 = 7$ (which is the negative root).

Equation (5.3) gives us the following isomorphism:

$$
I : TJJ_{13}(\mathbb{F}_{13}) \to E_{7, 5}(\mathbb{F}_{13})  : \begin{cases}
(x, y) \\
\mathcal{O}
\end{cases}

\mapsto

\begin{cases}
(10\cdot x, 8\cdot y) \\
\mathcal{O}
\end{cases}
$$

Let's use Sage to confirm this:



```python
from sage.all import EllipticCurve

F13 = GF(13)
TJJ = EllipticCurve(F13, [8, 8])
E75 = EllipticCurve(F13, [7, 5])


def I(xy):
    return (xy[0] * F13(10), xy[1] * F13(8))


TJJ_pts = [p.xy() for p in TJJ.points() if p != TJJ(0)]
E75_pts = [p.xy() for p in E75.points() if p != E75(0)]
I_TJJ_E75pts = [I(pt) for pt in TJJ_pts]
assert sorted(I_TJJ_E75pts) == sorted(E75_pts)
```

## Exercise 63

> Consider the commutative group defined by the affine group law and TinyJubJub with base field $\mathbb{F}_{13}$.
>
> 1. Compute the inverse of $(10, 10), \mathcal{O}, (4, 0), (1, 2)$
> 2. Solve the equation $x \oplus (9, 4) = (5, 2)$ for some point $x$ on the curve.

The inverse of $(x, y)$ is given by $(x, -y)$ unless the point is the point at infinity. So:

- $-(10, 10) = (10, 3)$
- $-\mathcal{O} = \mathcal{O}$
- $-(4, 0) = (4, 0)$
- $-(1, 2) = (1, 11)$

Let us solve the equation, which can be shown as:

$$
x = (5, 2) \oplus (9, 9)
$$

We will use the Chord rule to do this addition as the points are different. Letting $x = (x', y')$ for these equations:

$$
x' = \left(\frac{9-2}{9-5}\right)^2 - 5 - 9 = 5 \times 5 - 1 \equiv 11 \pmod{13}
$$

$$
y' = \left(\frac{9-2}{9-5}\right)(5 - 11) - 2 = 5 \times 7 - 2 = 33 \equiv 7 \pmod{13}
$$

Our result is $x = (11, 7)$. We can confirm with Sage:



```python
from sage.all import EllipticCurve, GF

E = EllipticCurve(GF(13), [8, 8])
(E(5, 2) - E(9, 4)).xy()
```




    (11, 7)



## Exercise 64

> Consider example 79 and compute the set $\{[1](0, 1), [2](0, 1), \ldots, [8](0, 1), [9](0, 1)\}$ using the tangent rule only.

The curve in example 79 is $E_{1,1}(\mathbb{F}_5)$ which has scalar order 9. Using tangent rule only means to use **doubling** only:

$$
\begin{align*}
    [1](0, 1) + [1](0, 1) = [2](0, 1) \\
    [2](0, 1) + [2](0, 1) = [4](0, 1) \\
    [4](0, 1) + [4](0, 1) = [8](0, 1) \\
    [8](0, 1) + [8](0, 1) = [7](0, 1) \\
    [7](0, 1) + [7](0, 1) = [5](0, 1) \\
    [5](0, 1) + [5](0, 1) = [1](0, 1)
\end{align*}
$$

We got points at order 1, 2, 4, 5, 7, 8 but we are missing the ones at 3, 6. We can't find $[3](0, 1)$ or $[6](0, 1)$ without the Chord rule here, and this is not a surprise. As explained in example 79, our group has order 9 which factorizes as $9 = 3 \times 3$. So, we expect to have 3 subgroups:

- A subgroup of order 9 (the group itself).
- A subgroup of order 3.
- A subgroup of order 1 (trivial group).

As you may notice, the points $[3](0, 1)$ and $[6](0, 1)$ are actually the elements within the subgroup of order 3. In other words, they belong to the logarithmic order:

$$
[3](0, 1) \to [6](0, 1) \to \mathcal{O}
$$

When we do the doubling, these points give eachother:

$$
\begin{align*}
    [3](0, 1) + [3](0, 1) = [6](0, 1) \\
    [6](0, 1) + [6](0, 1) = [3](0, 1)
\end{align*}
$$

## Exercise 65

> Consider example 80 and compute the scalar multiplications $[10](5, 11)$ as well as $[10](9, 4)$ and $[4](9, 4)$ with pen and paper using the algorithm from exercise 38 (Efficient Scalar Multiplication).

We can compute these as:

- $[10](5, 11) = [2 \times (2 \times 1 + 1)](5, 11)$
- $[10](9, 4) = [2 \times (2 \times 1 + 1)](9, 4)$
- $[4](9, 4) = [2 \times (2 \times 1)](9, 4)$

The question wants us to do this in pen-and-paper, but I will instead write the intermediate results in Sage below for us to verify results if we are to write them on paper:



```python
from sage.all import GF, EllipticCurve

F13 = GF(13)
TJJ = EllipticCurve(F13, [8, 8])


def esm(P, k) -> int:
    """
    Efficient Scalar Multiplication using "double-and-add"
    for some curve point P and scalar k
    """
    print(P)
    ans = P - P  # 0
    base = P
    while k > 0:
        if k & 1 == 1:
            ans += base
            print(ans)
        base += base
        k >>= 1
    print("")
    return ans


assert esm(TJJ(5, 11), 10) == TJJ(0)  # result from example 80
assert esm(TJJ(9, 4), 10) == TJJ(4, 0)  # result from example 80
assert esm(TJJ(9, 4), 4) == TJJ(7, 11)
```

    (5 : 11 : 1)
    (7 : 11 : 1)
    (0 : 1 : 0)
    
    (9 : 4 : 1)
    (5 : 11 : 1)
    (4 : 0 : 1)
    
    (9 : 4 : 1)
    (7 : 11 : 1)
    


## Exercise 66

> Consider example 81 and compute the set shown in equation (5.23) by inserting all points from the projective plane $\mathbb{F}_5\mathbb{P}^2$ into the defining projective Short Weierstrass equation.

The equation that we have to satisfy over projective points is the following:

$$
\forall (x, y, z) \in [X : Y : Z] : y^2z = x^3 + 1\cdot xz^2 + 1 \cdot z^3
$$

Using Sage, we can try the equation with $z=1$, since we know there are not solutions for $z=0$ other than point at infinity:



```python
from sage.all import GF, EllipticCurve

F5 = GF(5)
E = EllipticCurve(F5, [1, 1])


def eqn(x, y, z):
    return y**2 * z == x**3 + x * z**2 + z**3


affine_points = [p.xy() for p in E.points() if p != E(0)]
proj_points = [(p[0], p[1], 1) for p in affine_points if eqn(p[0], p[1], F5(1))]
print(proj_points)
```

    [(0, 1, 1), (0, 4, 1), (2, 1, 1), (2, 4, 1), (3, 1, 1), (3, 4, 1), (4, 2, 1), (4, 3, 1)]


Alternatively, we can use `ProjectiveSpace` within Sage (thanks to [@skaunov](https://github.com/skaunov) for letting me know about `ProjectiveSpace` in issue [#1](https://github.com/erhant/moonmath/issues/1)):



```python
from sage.all import GF, ProjectiveSpace

F5 = GF(5)
F5P2 = ProjectiveSpace(F5, 2)
points = [(x, y, z) for (x, y, z) in F5P2 if (y**2) * z == x**3 + x * (z**2) + z**3]
print(points)
```

    [(0, 1, 1), (0, 4, 1), (2, 1, 1), (2, 4, 1), (3, 1, 1), (3, 4, 1), (4, 2, 1), (4, 3, 1), (0, 1, 0)]


## Exercise 67 ✨

> Compute the projective representation of the TinyJubJub curve with base field $\mathbb{F}_{13}$. Then, print the logarithmic order of its large prime-order subgroup with respect to the generator $[ 7 : 11 : 1 ]$.

Let's begin by finding the co-factor:



```python
from sage.all import GF, EllipticCurve, factor

TJJ = EllipticCurve(GF(13), [8, 8])
order = TJJ.order()
factorization = factor(order)
lpf = max(factorization)[0]  # largest-prime factor
cf = order // lpf  # co-factor
```

Now let's do co-factor clearing:



```python
Esub = set([p * cf for p in TJJ.points()])
assert len(Esub) == lpf  # order should be equal to lpf
```

Let's also make sure our generator for the exercise is in this subgroup:



```python
g = TJJ(7, 11)  # [7 : 11 : 1]
assert g in Esub  # make sure it is in the subgroup
```

We can then add the generator to itself many times to find the logarithmic order:



```python
log_order = [g]
for _ in range(1, lpf):
    log_order.append(log_order[-1] + g)
print(log_order)
print(len(log_order), "elements")
```

    [(7 : 11 : 1), (8 : 5 : 1), (8 : 8 : 1), (7 : 2 : 1), (0 : 1 : 0)]
    5 elements


As expected from the large prime-order subgroup of $TJJ_{13}$ which has order 5, we see 5 elements.

## Exercise 68

> Consider example 81 again. Compute the following expressions for projective points $E_{1, 1}(\mathbb{F}_5\mathbb{P}^2)$ using algorithm 7.
>
> - $[0 : 1 : 0] \oplus [4 : 3 : 1]$
> - $[0 : 3 : 0] \oplus [3 : 1 : 2]$
> - $-[0 : 4 : 1] \oplus [3 : 4 : 1]$
> - $[4 : 3 : 1] \oplus [4 : 2 : 1]$
>
> and then solve the equation $[X : Y : Z] \oplus [0 : 1 : 1] = [2 : 4 : 1]$ for some point from the projective Short Weierstrass curve $E_{1, 1}(\mathbb{F}_5\mathbb{P}^2)$

Let's explain each expression one by one:

- The first expression here is actually addition with a point-at-infinity, so $[0 : 1 : 0] \oplus [4 : 3 : 1] = [4 : 3 : 1]$ is straightforward.

- At $[0 : 3 : 0] \oplus [3 : 1 : 2]$ we can look at the point on the left hand-side a bit more carefully. Notice that $\{3k \mid k \in \mathbb{F}_5^\ast\} = \{3, 1, 4, 2\}$, so this projective point is the same as $[0 : 1 : 0]$ that is the point at infinity. We can simply say that $[0 : 3 : 0] \oplus [3 : 1 : 2] = [3 : 1 : 2]$ in that case. We can find the answer for $Z=1$ as well, simply multiply the coordinates with 3 to get $[9 : 3 : 6] = [4 : 3 : 1]$.

- $-[0 : 4 : 1] \oplus [3 : 4 : 1]$ can be written as $[0 : 1 : 1] \oplus [3 : 4 : 1]$ due to how additive inverse works in projective points. Then, let's look at first few variables in the Algorithm 7:

$$
\begin{align*}
U_1 &\gets Y_2 \cdot Z_1 &= 4 \cdot 1 = 4 \\
U_2 &\gets Y_1 \cdot Z_2 &= 1 \cdot 1 = 1 \\
V_1 &\gets X_2 \cdot Z_1 &= 3 \cdot 1 = 3 \\
V_2 &\gets X_1 \cdot Z_2 &= 0 \cdot 1 = 0
\end{align*}
$$

We have $V_1 \ne V_2$ so we apply the `else` branch at the bottom:

$$
\begin{align*}
U  &= U_1 − U_2 &= 4 - 1 = 3 \\
V  &= V_1 − V_2 &= 3 - 0 = 3 \\
W  &= Z_1 \cdot Z_2 &= 1 \cdot 1 = 1 \\
A  &= U^2 \cdot W − V^3 − 2 \cdot V^2 \cdot V_2 &= 3^2 \cdot 1 - 3^3 - 2 \cdot 3^2 \cdot 0 = 4 - 2 = 2 \\
X' &= V \cdot A &= 3 \cdot 2 = 1 \\
Y' &= U \cdot (V^2 \cdot V_2 − A) − V^3 \cdot U_2 &= 3 \cdot (3^2 \cdot 0 - 2) - 3^3 \cdot 1 = - (3 \cdot 2) - 3^3 = 4 - 2 = 2 \\
Z' &= V^3 \cdot W &= 3^3 \cdot 1 = 2
\end{align*}
$$

We find the answer as $[X' : Y' : Z'] \gets [1 : 2 : 2]$. We can have $Z=1$ by multiplying the values by 3, $[1 \times 3 : 2 \times 3 : 2 \times 3] = [3 : 1 : 1]$.

- $[4 : 3 : 1] \oplus [4 : 2 : 1]$ is actually an operation of a point with its inverse, notice that $-[4 : 3 : 1] = [4 : -3 : 1] = [4 : 2 : 1]$, so the result of this operation is $[0 : 1 : 0]$ i.e. point-at-infinity.

Let's verify our results with Sage:



```python
from sage.all import GF, EllipticCurve

E = EllipticCurve(GF(5), [1, 1])

assert E(0, 1, 0) + E(4, 3, 1) == E(4, 3, 1)
assert E(0, 3, 0) + E(3, 1, 2) == E(4, 3, 1)
assert -E(0, 4, 1) + E(3, 4, 1) == E(3, 1, 1)
assert E(4, 3, 1) + E(4, 2, 1) == E(0, 1, 0)
```

## Exercise 69

> Compare the affine addition law for Short Weierstrass curves with the projective addition rule. Which branch in the projective branch corresponds to which case in the affine law?

The first two if-else's handle the addition with neutral element (point at infinity) case. Then, we have a major branching after $V_1 = V_2$ check, which is true if $X_1 = X_2$. If $X$ coordinates match for two points, they are either the same point or on the opposite sides of the curve:

- $U_1 \ne U_2$ is true if these points are on the opposite sides, and we know this means $Y_1 = -Y_2$ and their addition results in $\mathcal{O}$
- $U_1 = U_2$ means this is the same point, and we apply the Tangent rule. However, there is one case where the tangent rule results in point at infinity, and that is when $Y = 0$ which is checked by $Y_1 = 0$ in the algorithm.

Naturally, the remaining branch (where $V_1 \ne V_2$) handles the Chord rule where we add two different points with different $X$ coordinates.

## Exercise 70

> Consider example 82 and compute the set in (5.30) by inserting every pair of field elements $(x, y) \in \mathbb{F}_{13} \times \mathbb{F}_{13}$ into the defining Montgomery equation.

We use Sage to compute the set:



```python
from sage.all import GF, Set

F13 = GF(13)
B = F13(7)
A = F13(6)
points = []
for x in F13:
    for y in F13:
        if B * (y**2) == (x**3) + A * (x**2) + x:
            points.append((x, y))
print(points)
```

    [(0, 0), (1, 4), (1, 9), (2, 4), (2, 9), (3, 5), (3, 8), (4, 4), (4, 9), (5, 1), (5, 12), (7, 1), (7, 12), (8, 1), (8, 12), (9, 2), (9, 11), (10, 3), (10, 10)]


## Exercise 71

> Consider $E_1(\mathbb{F})$ from example 70 and show that this curve is not a Montgomery curve.

The curve in example 70 is defined as the set of all pairs $(x, y)$ in $\mathbb{F}_5$ that satisfy $y^2 = x^3 + x + 1$. One of the conditions for a Short Weierstrass curve to be a Montgomery curve is for it to have a scalar order divisible by 4. If we check that:



```python
from sage.all import GF, EllipticCurve

F5 = GF(5)
a, b = 0, 1
E1_F5 = EllipticCurve(F5, [a, b])
if E1_F5.order() % 4 != 0:
    print("Not a Montgomery curve!")
```

    Not a Montgomery curve!


As we can see, the order of the scalar field is not divisible by 4, therefore $E_1(\mathbb{F}_5)$ is not a Montgomery curve.

## Exercise 72

> Show that `secp256k1` is not a Montgomery curve.

One of the conditions to be a Montogomery curve is that order of the scalar field should be divisible by 4.



```python
from sage.all import GF, EllipticCurve

# order of the base field
p = 115792089237316195423570985008687907853269984665640564039457584007908834671663
E = EllipticCurve(GF(p), [0, 7])

if E.order() % 4 != 0:
    print("Not a Montgomery curve!")
```

    Not a Montgomery curve!


As we can see, the order of the scalar field is not divisible by 4, therefore `secp256k1` is not a Montgomery curve.

## Exercise 73 ✨

> Consider the commutative group defined by the Montgomery group law and TinyJubJub with base field $\mathbb{F}_{13}$ in Montgomery form.
>
> - Compute the inverse of $(1, 9), \mathcal{O}, (7, 12), (4, 9)$.
> - Solve the equation $x \oplus (3, 8) = (10, 3)$ for some point in the Montgomery curve.
>
> Finally, choose some point in the curve and test to see if it is a generator. If not, keep trying until you find one. Print out that generator point's logarithmic order.

See the code [here](./montgomery.sage).

## Exercise 74

> Show that `alt_bn128` is not a Montgomery curve.

One of the conditions to be a Montogomery curve is that order of the scalar field should be divisible by 4.



```python
from sage.all import EllipticCurve, GF

# order of the base field
p = 21888242871839275222246405745257275088696311157297823662689037894645226208583
E = EllipticCurve(GF(p), [0, 3])
assert E.order() % 4 != 0
```

As we can see, the order is not divisible by 4, therefore `alt_bn128` is not a Montgomery curve.

## Exercise 75 ✨

> Consider the commutative group defined by the Twisted Edwards group law and TinyJubJub with base field $\mathbb{F}_{13}$ in Twisted Edwards form.
>
> - Compute the inverse of $(1, 11), (0, 1), (3, 0), (5, 8)$.
> - Solve the equation $x \oplus (5, 8) = (1, 11)$ for some point in the Montgomery curve.
>
> Finally, choose some point in the curve and test to see if it is a generator. If not, keep trying until you find one. Print out that generator point's logarithmic order.

We first implement a class for Twisted Edwards:



```python
from sage.all import GF, Set, FiniteFields


class TwistedEdwardsCurve:
    a = 0
    d = 0
    F: FiniteFields  # base field
    points: set  # points in curve

    def __init__(self, a, d, prime) -> None:
        F = GF(prime)
        self.a = F(a)
        self.d = F(d)
        self.F = F

        # find all points, O(n^2)
        affine_points = []
        for x in F:
            for y in F:
                if self.in_curve((x, y)):
                    affine_points.append((x, y))
        self.points = Set(affine_points)

    def __str__(self) -> str:
        return "{0} * x^2 + y^2 = 1 + {1} * x^2 * y^2".format(self.a, self.d)

    def add(self, P, Q):
        """Add points P and Q in the Twisted Edwards curve."""
        x1, x2, y1, y2 = P[0], Q[0], P[1], Q[1]

        x3 = (x1 * y2 + y1 * x2) / (1 + self.d * x1 * x2 * y1 * y2)
        y3 = (y1 * y2 - self.a * x1 * x2) / (1 - self.d * x1 * x2 * y1 * y2)
        return (x3, y3)

    def in_curve(self, P) -> bool:
        """Returns true if the given point is in curve."""
        return self.a * (P[0] ** 2) + (P[1] ** 2) == self.F(1) + self.d * (
            P[0] ** 2
        ) * (P[1] ** 2)

    def inverse(self, P):
        """Inverts a point."""
        return (self.F.order() - P[0], P[1])

    def point(self, x, y):
        """Return the a point in curve."""
        return (self.F(x), self.F(y))
```

With that, we can solve our exercise:



```python
# TinyJubJub parameters
prime = 13
a = 3
d = 8
TETJJ = TwistedEdwardsCurve(a, d, prime)
print("\nCurve:")
print(TETJJ)

print("\nPart 1: Inverting points:")
pointsToInvert = list(
    map(lambda xy: TETJJ.point(xy[0], xy[1]), [(1, 11), (0, 1), (3, 0), (5, 8)])
)
inverses = list(map(lambda p: TETJJ.inverse(p), pointsToInvert))
for p, ip in zip(pointsToInvert, inverses):
    assert TETJJ.in_curve(ip)
    print("{0} --> {1}".format(p, ip))

print("\nPart 2: Solving x + (5, 8) = (1, 11)")
A, B = TETJJ.point(5, 8), TETJJ.point(1, 11)
assert TETJJ.in_curve(A)
assert TETJJ.in_curve(B)
X = TETJJ.add(B, TETJJ.inverse(A))  # X = B + (-A)
assert TETJJ.in_curve(X)
print("X:", X)

print("\nPart 3: Searching for a generator")
for point in points:
    runner = point
    i = 1
    while i < (len(points) - 1):
        if runner == (0, 1):
            # print("{} is not a generator".format(point))
            i = 1
            break
        runner = TETJJ.add(
            TETJJ.point(runner[0], runner[1]), TETJJ.point(point[0], point[1])
        )
        i += 1
    if i == len(points) - 1:
        assert TETJJ.add(runner, point) == (0, 1)
        print("{} is a generator".format(point))
        break
```

    
    Curve:
    3 * x^2 + y^2 = 1 + 8 * x^2 * y^2
    
    Part 1: Inverting points:
    (1, 11) --> (12, 11)
    (0, 1) --> (0, 1)
    (3, 0) --> (10, 0)
    (5, 8) --> (8, 8)
    
    Part 2: Solving x + (5, 8) = (1, 11)
    X: (11, 7)
    
    Part 3: Searching for a generator
    (11, 7) is a generator


## Exercise 76

> Consider the short Weierstrass curve $y^2 = x^3 + x + 1$ over extension field $\mathbb{F}_{5^2}$. Compute $(4t + 3, 2t + 1) \oplus (3t + 3, 2)$, and double-check the result in sage. Then, solve the equation $x \oplus (3t + 3, 3) = (3, 4)$ for some $x$ in the curve. Also, compute $[5](2t + 1, 4t + 4)$.

Here is the solution in Sage:



```python
from sage.all import GF, EllipticCurve

F5 = GF(5)  # field
F5t = F5["t"]  # polynomial ring
P_MOD_2 = F5t([2, 0, 1])  # irreducible polynomial t^2 + 2

# extension field
F5_2 = GF(5**2, name="t", modulus=P_MOD_2)

# curve over extension field
E1F5_2 = EllipticCurve(F5_2, [1, 1])

print(
    "(4t+3, 2t+1) + (3t + 3, 2) =",
    (E1F5_2([3, 4], [1, 2]) + E1F5_2([3, 3], [2])).xy(),
)
print("\nx + (3t + 3, 3) = (3, 4)\nx =", (E1F5_2([3], [4]) - E1F5_2([3, 3], [2])).xy())
print("\n[5](2t + 1, 4t + 4) =", (5 * E1F5_2([1, 2], [4, 4])).xy())
```

    (4t+3, 2t+1) + (3t + 3, 2) = (0, 1)
    
    x + (3t + 3, 3) = (3, 4)
    x = (2*t + 2, t)
    
    [5](2t + 1, 4t + 4) = (2*t + 1, t + 1)


## Exercise 77

> Consider TinyJubJub. Show that $t^4 + 2 \in \mathbb{F}_{13}[t]$ is irreducible.
>
> Then, write a sage program to implement the finite field extension $\mathbb{F}_{13^4}$. Implement the curve extension in the extension field, and compute the number of curve points (i.e. order).

Here is the solution in Sage:



```python
from sage.all import GF, EllipticCurve

F13 = GF(13)  # field
F13t = F13["t"]  # polynomial ring
P_MOD_4 = F13t([2, 0, 0, 0, 1])  # irreducible polynomial
assert P_MOD_4.is_irreducible()

# extension field
F13_4 = GF(13**4, name="t", modulus=P_MOD_4)

# TinyJubJub over the extension field
TJJ_F13_4 = EllipticCurve(F13_4, [8, 8])
print("Order of E(F_13^4):", TJJ_F13_4.order())
```

    Order of E(F_13^4): 28800


## Exercise 78 ✨

> Consider `alt_bn128` curve. We know from example 89 that this curve has embedding degree 12.
>
> - Use Sage to find an irreducible polynomial in $\mathbb{F}_p[t]$
> - Then compute the field extension $\mathbb{F}_{p^{12}}$ to implement the curve extension of `alt_bn128`. Compute the number of curve points.

Here is the solution in Sage:



```python
# curve parameters for alt_bn128
p = 21888242871839275222246405745257275088696311157297823662689037894645226208583
a, b = 0, 3

FP = GF(p)  # field
FPt = FP["t"]  # polynomial ring

k = 12  # embedding degree
P_MOD_K = FPt.irreducible_element(k)  # an irreducible polynomial of degree k
print("Irreducible polynomial:\n", P_MOD_K)

# extension field
FP_K = GF(p**k, name="t", modulus=P_MOD_K)

# curve over extension field
E = EllipticCurve(FP_K, [a, b])

print("Order of alt_bn128 extension:\n", E.order())
```

    Irreducible polynomial:
     t^12 + 7*t^11 + 15*t^10 + t^9 + 21888242871839275222246405745257275088696311157297823662689037894645226208558*t^8 + 24*t^7 + 152*t^6 + 208*t^5 + 184*t^4 + 144*t^3 + 78*t^2 + 51*t + 71
    Order of alt_bn128 extension:
     12092909088188237225393433017559174875623137613219078327682045681675023350320878590139619158941453632724570634378148379186020109423506557278061404249513976103803771139954000579995199902828634263992330574392218791796266323480026479977659504287064359209036331389750395884727865805793574046154686347934603866375769645860851559671200189106819576945533990794197558448169154800495832790107673176422796675256499746815795625450299074794144048526198146639914021389804535306000613349331018514938275266778482547622423749922359770464262581875420752922397459498567293510559440917138825365277367270645144062796625014026162633826493618231042343006032299664580979412778040535526273331171632325988684368468515086899424261777185250498803406666234578372177228678748158811450716246172407259106389136866877568849564706281406613378690107119143771354767479053194532950000787048176486489212307035732283106982641546328096285628300491976754624


## Exercise 79 ✨

> Consider the full 5-torsion group $TJJ_{13}[5]$ from example 92.
>
> - Write down the set of all elements from this group, and identify the subset of all elements from $TJJ_{13}(\mathbb{F}_{13})[5]$ as well as $TJJ_{13}(\mathbb{F}_{13^2})[5]$.
> - Then compute the 5-torsion group $TJJ_{13}(\mathbb{F}_{13^8})[5]$.

First, let's compute the full 5-torsion group $TJJ_{13}[5]$ as shown in the example. For a full $r$-torsion group, we need the curve defined over the extension field over a polynomial with degree equal to $k(r)$. We know from a previous example that $k(5) = 4$ so we will use a degree 4 polynomial.



```python
from sage.all import GF, EllipticCurve, Set

F13 = GF(13)  # field
F13t = F13["t"]  # polynomial ring

# degree 4 irreducible polynomial
P_MOD_4 = F13t([2, 0, 0, 0, 1])
assert P_MOD_4.is_irreducible()

# extension field
F13_4 = GF(13**4, name="t", modulus=P_MOD_4)

# curve over the extension
TJJF13_4 = EllipticCurve(F13_4, [8, 8])

# full 5-torsion group, that is the
# set of points P such that [5]P == INF
TJJF13_4_5 = Set(TJJF13_4(0).division_points(5))
print("Number of elements:", TJJF13_4_5.cardinality())  # 25
```

    Number of elements: 25


From the definition of $r$-torsion groups, we know that the following holds:

$$
TJJ_{13}(\mathbb{F}_{13})[5] = TJJ_{13}(\mathbb{F}_{13^2})[5] \subset TJJ_{13}(\mathbb{F}_{13^4})[5] = TJJ_{13}(\mathbb{F}_{13^8})[5]
$$

Remember that this is because 4 is the embedding degree. So, with our code so far we have already computed the 5-torsion group $TJJ_{13}(\mathbb{F}_{13^8})[5]$. We can compute the other one over the curve itself, without the field extension.



```python
# curve over the field
TJJ = EllipticCurve(F13, [8, 8])

# 5-torsion group
TJJ_5 = Set(TJJ(0).division_points(5))
print("Number of elements:", TJJ_5.cardinality())  # 5
print(TJJ_5)
```

    Number of elements: 5
    {(7 : 11 : 1), (0 : 1 : 0), (8 : 8 : 1), (7 : 2 : 1), (8 : 5 : 1)}


## Exercise 80

> Consider `secp256k1` curve and it's full $r$-torsion group. Write down a single element from the curve's full torsion group that is not the point at infinity.

In example 93, we learn the following:

> ..., without any optimizations, representing such an element would need $k \cdot 256$ bits, which is too much to be representable in the observable universe. It follows that it is not only infeasible to compute the full $r$-torsion group of $\text{secp256k1}$, but moreover to even write down single elements of that group in general.

So, the question boils down to some optimization. Futher in the exercise 96 at the end of next section, it mentions the following:

> ... according to example 93 we can not store average curve points from the extension curve $\text{secp256k1}(F_{p^k})$ on any computer, ...

We are looking for a point other than the point at infinity, and with the knowledge we have so far that seems to be impossible.

However, we could maybe find a value from the curve itself instead of an extension field, which would be in the full $r$-torsion group due to the subset rule. Also note that $r$ here is equal to the scalar order, because the scalar order of `secp256k1` is a prime meaning that the order itself is the largest prime factor.



```python
from sage.all import GF, EllipticCurve, is_prime

p = 115792089237316195423570985008687907853269984665640564039457584007908834671663
E = EllipticCurve(GF(p), [0, 7])
INF = E(0)
# embedding degree
k = 19298681539552699237261830834781317975472927379845817397100860523586360249056

# order of scalar field
q = E.order()
assert is_prime(q)

# largest prime factor is the order itself
r = q.factor()[0][0]
assert q == r

# try for some random points
for _ in range(200):
    assert E.random_point() * r == INF
```

Indeed any point within the original curve is a member of the torsion group $E(\mathbb{F}_p)[r]$ and we know that this is a subset of the full-torsion group!

## Exercise 81 🔴

> Consider `alt_bn128` curve and and it's full $r$-torsion group. Write a Sage program that computes a generator from the curve's full torsion group.

First of all, we should notice that $r$ is equal to the order of the scalar field of `alt_bn128` since that order is a prime and it is the largest prime factor on its own. We also know from example 89 that this curve has an embedding degree of 12. So, we must compute the curve over the extension field with a degree 12 polynomial. Let's do that in Sage:



```python
# curve parameters for alt_bn128
p = 21888242871839275222246405745257275088696311157297823662689037894645226208583
a, b = 0, 3

FP = GF(p)  # field
FPt = FP["t"]  # polynomial ring

# curve over the base field
E = EllipticCurve(FP, [a, b])

# an irreducible polynomial of degree k
k = 12  # embedding degree
P_MOD_K = FPt.irreducible_element(k)
assert P_MOD_K.is_irreducible()

# extension field
FP_K = GF(p**k, name="t", modulus=P_MOD_K)

# curve over extension field
E_K = EllipticCurve(FP_K, [a, b])

# largest prime factor is the order itself
r = q.factor()[0][0]
assert q == r

# try for some random points
INF = E_K(0)
for _ in range(200):
    assert E_K.random_point() * r == INF
```

## Exercise 82

> Consider the small prime factor 2 of the TinyJubJub curve. Compute the full 2-torsion group of $TJJ_{13}$ and then compute the groups $\mathbb{G}_1[2]$ and $\mathbb{G}_2[2]$.

First, let's find the embedding degree $k(2)$ for this curve.



```python
from sage.all import GF, EllipticCurve, Set

# order of the base field for TJJ
p = 13
F13 = GF(p)
TJJ = EllipticCurve(F13, [8, 8])

# order of the curve's scalar field
n = TJJ.order()
# small prime factor
r = 2
assert n % r == 0

# find embedding degree
k = 1
while k < r:
    if (p**k - 1) % r == 0:
        break
    k += 1
print("Embedding degree:", k)
```

    Embedding degree: 1


We find the embedding degree to be 1. In fact, you can immediately say that the embedding degree is 1, because notice that following operation in the congruence:

$$
13^k - 1 \bmod{2}
$$

We are looking for the smallest $k$ that results in 0 for the above operation, and it is obvious that $13-1$ is an even number and thus $k=1$. We also know this result from example 87 by the way.

Yet another argument is that an embedding degree $1 \leq k < r$ is guaranteed for the prime order due to FLT, and we can only have $k=1$ for $r=2$ anyways.

To compute the **full** 2-torsion group, we need to find the 2-torsion group of the curve over field extension with order $p^{k(2)}$. We have just shown that $k(2) = 1$, so it turns out that our original curve serves the purpose to find the full torsion group! We can simply choose points $P$ such that $[2]P = \mathcal{O}$ using Sage:



```python
# full r-torsion group, using the original curve
TJJ_1_tor = Set(TJJ(0).division_points(r))
print("{}-torsion group:".format(r))
print(TJJ_1_tor)
```

    2-torsion group:
    {(4 : 0 : 1), (0 : 1 : 0)}


We would expect $r^2$ elements (i.e. 4) in the full-torsion group, which is NOT the case here! After lengthy discussions with [@bufferhe4d](https://github.com/bufferhe4d) and his further discussions with more people, we have come to conclusion that the $r^2$ requirement is not strict when $k=1$. In some cases, we can have $r$ elements.

Let's compute the pairing groups now:


```python
INF = TJJ(0)  # point at infinity


def fro_pi(P):
    if P != INF:
        (x, y) = P.xy()
        return TJJ(x**p, y**p)
    else:
        return P


G1 = [P for P in TJJ_1_tor if fro_pi(P) == P]
print("G1:", G1)
# {(4 : 0 : 1), (0 : 1 : 0)}

G2 = [P for P in TJJ_1_tor if fro_pi(P) == p * P]
print("G2:", G1)
```


    ---------------------------------------------------------------------------

    NameError                                 Traceback (most recent call last)

    Cell In[9], line 1
    ----> 1 INF = TJJ(0)  # point at infinity
          4 def fro_pi(P):
          5     if P != INF:


    NameError: name 'TJJ' is not defined


Regarding the remark above about finding $r$ elements instead of $r^2$, there is also another thing to mention. If you find the 2-torsion group of TJJ over $\mathbb{F}_{p^4}$ you do actually get $r^2$ elements. 4 is the first time this happens, where the torsion group has 2 elements up until this point and has 4 elements beyond this point.

This would be in-line with (5.44) in the book; however, 4 is not the embedding degree for $r=2$ in this case.

Regardless of this fact, the pairing groups for the torsion group at $k=4$ is equal to the pairing groups computed for $k=1$ in this exercise!

> See this [code](./pairings.sage) here for a better presentation of this exercise. I have opened an issue about this exercise and the things discussed in particular: [see here](https://github.com/LeastAuthority/moonmath-manual/issues/84).

## Exercise 83 🔴

> Consider `alt_bn128` curve and and it's curve extension. Write a Sage program that computes a generator for each of the torsion group $\mathbb{G}_1[p]$ and $\mathbb{G}_2[p]$.

TODO


## Exercise 84 🔴

> Consider the `alt_bn128` curve from example 73, and the generators $g_1$ and $g_2$ of $\mathbb{G}_1[p]$ and $\mathbb{G}_2[p]$ from exercise 83. Write a Sage program that computes the Weil pairing $e(g_1, g_2)$

First, let's see how the pairing is computed, as shown in example 87:



```python
from sage.all import GF, EllipticCurve

# field of TJJ
F13 = GF(13)
F13t = F13["t"]

# extension field over t^4 + 2
P_MOD_4 = F13t([2, 0, 0, 0, 1])  # t^4 + 2
F13_4 = GF(13**4, name="t", modulus=P_MOD_4)

# curve over extension field
TJJF13_4 = EllipticCurve(F13_4, [8, 8])
P = TJJF13_4([7, 2])
print("      P:", P.xy())

Q = TJJF13_4([F13t([7, 0, 9]), F13t([0, 2, 0, 12])])  # 9t^2 + 7  # 12t^3 + 2t
print("      Q:", Q.xy())

ans = P.weil_pairing(Q, 5)
print("e(P, Q):", ans)
```

          P: (7, 2)
          Q: (9*t^2 + 7, 12*t^3 + 2*t)
    e(P, Q): 7*t^3 + 7*t^2 + 6*t + 3


Now, lets do the same thing but for the group that is given in our exercise:

TODO: do the exercise here


## Exercise 85

> Use our definition of the `try-hash` algorithm to implement a hash function $H_{TJJ[5]} : \{0, 1\}^\ast \to TJJ(\mathbb{F}_{13})[5]$ that maps binary strings of arbitrary length onto the 5-torsion group of $TJJ(\mathbb{F}_{13})[5]$

I didn't like the example implementation much, so I will implement the more generic function (the one defined in Algorithm 9) below, and use it for this exercise.



```python
from sage.all import ZZ, GF
from hashlib import sha256


def try_and_increment(s, E):
    """Hash `s` into a curve point on `E`."""
    c = -1

    # order of base field & curve params
    p = E.base_field().order()
    a, b = E.a4(), E.a6()

    # number of bits of p
    k = len(p.bits())
    while True:
        c += 1
        # compute sha256 of `s || bits(c)`
        sc: str = s + bin(c)[2:]
        digest: str = sha256(sc.encode("utf-8")).hexdigest()

        # cast the digest into integer & get (k+1)-bit representation
        bits = ZZ(digest, 16).digits(base=2, padto=k + 1)

        # map to a number (x-coord) using k bits
        x = 0
        for i, bit in enumerate(bits[:k]):
            x += bit * (2**i)
        if x >= p:
            # if x is too large, try again
            continue

        # find y^2 via the curve equation
        x = E.base_field()(x)
        yy = x**3 + a * x + b
        if not yy.is_square():
            # if yy is not a square root, try again
            continue
        y = yy.sqrt()

        if bits[k] == 0:
            # if auxiliary bit is 0, use the positive root
            return E(x, y)
        else:
            # if auxiliary bit is 1, use the negative root
            return E(x, -y)


# example
TJJ = EllipticCurve(GF(13), [8, 8])
print(try_and_increment("lorem ipsum", E))
```

    (8 : 8 : 1)


The function above can map any string into a curve point. In the exercise, we not only need to hash to a curve point but then also map this point onto the 5-torsion group of TJJ. Remember that TJJ had 20 points, and $20 = 5 \times 4$ so we can do co-factor clearing by multiplying the point with 4.



```python
def hash_to_tjj_13_5(s: str):
    TJJ = EllipticCurve(GF(13), [8, 8])
    P = try_and_increment(s, TJJ)
    return 4 * P


P = hash_to_tjj_13_5("lorem ipsum")
print(P.xy())

# [5]P == INF if P is in 5-torsion group
assert P * 5 == 0
```

    (8, 5)


## Exercise 86

> Implement a cryptographic hash function $H_{\text{secp256k1}} : \{0, 1\}^* \to \text{secp256k1}$ that maps binary strings of arbitrary length onto the elliptic curve `secp256k1`.

We will make use of the `try_and_increment` function implemented in the previous exercise.



```python
from sage.all import GF, EllipticCurve


def hash_to_secp256k1(s: str):
    # parameters for secp256k1
    p = 115792089237316195423570985008687907853269984665640564039457584007908834671663
    a, b = 0, 7

    Fp = GF(p)
    E = EllipticCurve(Fp, [a, b])

    P = try_and_increment(s, E)
    return P


P = hash_to_secp256k1("lorem ipsum")
print(P.xy())
```

    (98592660300306139108217934677605000680670471692090637702610446742601439054516, 10944968578626111729072870382098433009590240719021050603286881666265231643137)


## Exercise 87

> Consider `alt_bn128` curve. Write a Sage program that computes the trace of Frobenius for `alt_bn128`. Does the curve contain more or less elements than its base field $\mathbb{F}_p$?

Using Sage:



```python
from sage.all import GF, EllipticCurve

# curve parameters
p = 21888242871839275222246405745257275088696311157297823662689037894645226208583
a, b = 0, 3
Fp = GF(p)
E = EllipticCurve(Fp, [a, b])

# order of the scalar field
q = E.order()

# trace of Frobenius
t = p + 1 - q
print("Trace of Frobenius:", t)

if q < p:
    print("curve contains less elements than Fp")
else:
    print("curve contains more elements than Fp")
```

    Trace of Frobenius: 147946756881789318990833708069417712967
    curve contains less elements than Fp


We see that the curve `alt_bn128` contains less elements than its base field.

## Exercise 88

> Consider `alt_bn128` curve. Write a Sage program that computes the $j$-invariant for `alt_bn128`.

The $j$-invariant is computed as follows (as shown in section 5.6.2):

$$
j(E(\mathbb{F}_q)) = 1728 \cdot \frac{4 \cdot a^3}{4 \cdot a^3 + 27 \cdot b^2} \bmod{q}
$$

Here, $a, b$ are the curve parameters and $q$ is the order of the base field $\mathbb{F}_q$. Let's write that in Sage:


```python
from sage.all import GF, EllipticCurve

# curve parameters
p = 21888242871839275222246405745257275088696311157297823662689037894645226208583
a, b = 0, 3

def j_invariant(a, b, q):
    return (1728 * (4 * (a ** 3)) / (4 * (a ** 3) + 27 * (b ** 2))) % q

# note that we use p to denote order of base field, instead of q here
j_inv = j_invariant(a, b, p)
print("J invariant:", int(j_inv))

# also check with Sage
assert j_inv == EllipticCurve(GF(p), [a, b]).j_invariant()
```

    J invariant: 0



## Exercise 89 🔴

> Show that the Hilbert class polynomials for the CM-discriminants $D = -3$ and $D = -4$ are given by $H_{-3, q}(x) = x$ and $H_{-4, q}(x) = x - (1728 \bmod{q})$

TODO

## Exercise 90 🔴

> Use the complex multiplication method to construct an elliptic curve of order 7 over the prime field $\mathbb{F}_{13}$

TODO

## Exercise 91 🔴

> Use the complex multiplication method to compute all isomorphism classes of all elliptic curves of order 7 over the prime field $\mathbb{F}_{13}$

TODO

## Exercise 92 🔴

> Consider the prime modulus $p$ of curve `alt_bn128` from example 73, and its trace $t$ from exercise 92. Use the complex multiplication method to synthesize an elliptic curve over $F_p$ that is isomorphic to `alt_bn128` and compute an explicit isomorphism between these two curves.

TODO

## Exercise 93

> Consider the point $P = (9, 2)$. Show that $P$ is a point on the `BLS6_6` curve and compute the scalar product $[3]P$

BLS6\_6 has the curve equation $y^2 = x^3 + 6$ for values defined over $\mathbb{F}_{43}$. We can check if the equation holds for the given point:

$$
\begin{align*}
2^2 &= 9^3 + 6 \\
4 &= 41 + 6 \\
4 &= 4
\end{align*}
$$

Indeed the point is on curve. Now, remember that the order of scalar field for BLS6\_6 is 39, which factorizes as $13 \cdot 3$. We are given the addition table of the subgroup of order 13 (page 128), and the point $(9, 2)$ does not appear there. This just means that $(9, 2)$ does not belong to the subgroup of order 13, so it may have order 3 or 39.

We could compute the result using the Tangent and Chord rules (i.e. double it, and add itself) but I will use Sage instead. Note that the book also provides the result of this computation in section 5.6.4.2.


```python
from sage.all import GF, EllipticCurve

BLS6_6 = EllipticCurve(GF(43), [0, 6])
print(BLS6_6(9, 2).xy())
```

    (9, 2)



## Exercise 94

> Compute the following expressions:
>
> - $-(26, 34)$
> - $(26, 9) \oplus (13, 28)$
> - $(35, 15) \oplus \mathcal{O}$
> - $(27, 9) \oplus (33, 9)$

We can use the addition table of BLS6\_6 (page 128) to solve this quite easily. We can also keep in mind that BLS6\_6 is defined over the base field $\mathbb{F}_{43}$.

- $-(26, 34)$ corresponds to the number that when added to $(26, 34)$ results in $\mathcal{O}$. We see that $(26, 9)$ is the point we are looking for. We could also remember that $-(x, y) = (x, -y)$ in Short Weierstrass curves, so $-(26, 34) = (26, -34) = (26, 9)$ works too.

- $(26, 9) \oplus (13, 28)$ results in $(27, 9)$, as seen in the table.

- $(35, 15) \oplus \mathcal{O}$ results in $(35, 15)$ since the point-at-infinity is neutral. We can confirm this by looking at the first row or the first column in the table.

- $(27, 9) \oplus (33, 9)$ results in $(26, 34)$, as seen in the table.

## Exercise 95 🔴

> Consider the extended `BLS6_6` curve as defined in 5.67 and the two curve points $g_1 = (13, 15)$ and $g_2 = (7v^2, 16v^3)$. Compute the Weil pairing $e(g_1, g_2)$ using definition 5.49 and Miller's algorithm.

TODO

