def cge(g: int, x: int, n: int) -> int:
  '''
  Cyclic Group Exponentiation using "square-and-multiply"

  Parameters:
  - `g`: generator
  - `x`: exponent
  - `n`: order

  Returns:
  - `g^x (mod n)`
  '''
  h = g
  y = 1 # natural element g^0
  while x > 0:
    if x & 1 == 1:
      y = (y * h) % n
    h = (h * h) % n
    x >>= 1
  return y

if __name__ == "__main__":
  print(cge(2, 3, 5))
    