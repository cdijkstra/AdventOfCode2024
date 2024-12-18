Each button consists of a system of equations, where A and B are the amount of times button A and B are pressed respectively

```
a_x * A + b_x * B = p_x
a_y * A + b_y * B = p_y
```

We can then do multiplications by `b_x` and `b_y` to ensure the same coefficients occur in front of `B`

```
a_x * b_y * A + b_x * b_y * B = p_x * b_y
a_y * b_x * A + b_x * b_y * B = p_y * b_x
```

Now perform a substraction

```
(a_x * b_y - a_y * b_x) * A = p_x * b_y - p_y * b_x
```

So we obtain

```
A = p_x * b_y - p_y * b_x / (a_x * b_y - a_y * b_x)
```

And then we can solve for variable `B`

```
B = (p_x - a_x * A) / b_x
```
