The sequence `2,4,1,3,7,5,0,3,1,4,4,7,5,5,3,0` leads to

```
b = a % 8
b = b ^ 3
c = a // 2^b
a >> 3
b ^= a
b ^= c
out(b % 8)
if a != 0: jump 0
```

## End

We know that a should be in between [1,7] in the penultimate step.

## Start
