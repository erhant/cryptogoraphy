def esm(g: int, x: int, n: int) -> int:
  '''
  Efficient Scalar Multiplication using "double-and-add"

  Parameters:
  - `g`: number
  - `x`: number
  - `n`: order

  Returns:
  - `g * x (mod n)`
  '''
  h = g
  y = 0
  while x > 0:
    if x & 1 == 1:
      y = (y + h) % n
    h = (h << 1) % n
    x >>= 1
  return y

if __name__ == "__main__":
  print(esm(2, 8, 5))
   