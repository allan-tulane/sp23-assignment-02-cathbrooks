"""
CMPS 2200  Assignment 2.
See assignment-02.pdf for details.
"""
import time


class BinaryNumber:
    """ done """
    def __init__(self, n):
        self.decimal_val = n               
        self.binary_vec = list('{0:b}'.format(n)) 
        
    def __repr__(self):
        return('decimal=%d binary=%s' % (self.decimal_val, ''.join(self.binary_vec)))
    

## Implement multiplication functions here. Note that you will have to
## ensure that x, y are appropriately sized binary vectors for a
## divide and conquer approach.
def binary2int(binary_vec): 
    if len(binary_vec) == 0:
        return BinaryNumber(0)
    return BinaryNumber(int(''.join(binary_vec), 2))

def split_number(vec):
    return (binary2int(vec[:len(vec)//2]),
            binary2int(vec[len(vec)//2:]))

def bit_shift(number, n):
    # append n 0s to this number's binary string
    return binary2int(number.binary_vec + ['0'] * n)
    
def pad(x,y):
    # pad with leading 0 if x/y have different number of bits
    # e.g., [1,0] vs [1]
    if len(x) < len(y):
        x = ['0'] * (len(y)-len(x)) + x
    elif len(y) < len(x):
        y = ['0'] * (len(x)-len(y)) + y
    # pad with leading 0 if not even number of bits
    if len(x) % 2 != 0:
        x = ['0'] + x
        y = ['0'] + y
    return x,y



def subquadratic_multiply(x, y):
    xvec = x.binary_vec
    yvec = y.binary_vec
    xvec, yvec = pad(xvec, yvec)
    
    #base case
    #if y and y are both 1 or 0 return their product
    if x.decimal_val <= 1 and y.decimal_val <= 1:
      return BinaryNumber(x.decimal_val*y.decimal_val)

    #split the vectors
    x_left, x_right = split_number(xvec)
    y_left, y_right = split_number(yvec)

    #2^n(x_left*y_left)
    left_product = bit_shift(subquadratic_multiply(x_left, y_left), len(xvec))

    #x_right * y_right
    right_product = subquadratic_multiply(x_right, y_right)

    #2^n/2((x_left + x_right)*(y_left + y_right) - (x_left * y_left) - (x_right * y_right)
    x_sum = BinaryNumber(x_left.decimal_val + x_right.decimal_val)
    y_sum = BinaryNumber(y_left.decimal_val + y_right.decimal_val)
    sum_product = subquadratic_multiply(x_sum, y_sum)
    middle_product = bit_shift(BinaryNumber(sum_product.decimal_val - left_product.decimal_val - right_product.decimal_val), len(xvec)//2)

    #final sum
    return BinaryNumber(left_product.decimal_val + middle_product.decimal_val + right_product.decimal_val)


## Feel free to add your own tests here.
def test_multiply():
    assert subquadratic_multiply(BinaryNumber(2), BinaryNumber(2)) == 2*2
    assert subquadratic_multiply(BinaryNumber(4), BinaryNumber(2)) == 4*2
    assert subquadratic_multiply(BinaryNumber(3), BinaryNumber(4)) == 3*4

def time_multiply(x, y, f):
    start = time.time()
    # multiply two numbers x, y using function f
    f(x,y)
  
    return (time.time() - start)*1000

def compare_run_times():
  n2 = time_multiply(BinaryNumber(2), BinaryNumber(2), subquadratic_multiply)
  print("n = 2: " + str(n2))
  print()
  
  n3 = time_multiply(BinaryNumber(2), BinaryNumber(4), subquadratic_multiply)
  print("n = 3: " + str(n3))
  print()
  
  n4 = time_multiply(BinaryNumber(2), BinaryNumber(6), subquadratic_multiply)
  print("n = 4: " + str(n4))
  print()
  
  n5 = time_multiply(BinaryNumber(2), BinaryNumber(8), subquadratic_multiply)
  print("n = 5: " + str(n5))
  print()
  
  n6 = (time_multiply(BinaryNumber(2), BinaryNumber(10), subquadratic_multiply)
  print("n = 6: " + str(n6))
  print()
  
compare_run_times()

