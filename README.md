# Ternary Engine

# Representation

The program uses balanced ternary. This is a base 3 numbering system with the digits (trits) -1, 0, and 1.

Trits are represented by nzp meaning negative, zero, and positive. This avoids the sign problem of -0+ when using addition or subtraction.
```
5+5=10
pnn+pnn=pzp
+--++--=+0+
```

## Internal representation

The program uses the same representation internally. It would be more efficient to represent each trit as an integer. Adding and multiplication would be much faster, but this does not translate well to FPGA. Instead, I have implemented the diadic and monadic operands as LUTs (look up tables). These can be readily implemented on FPGA.

Once a cpu has been implemented here, translating to FPGA should be straight forward. This program provides the tools to design an ALU or CPU in balanced ternary.

# Ternary Gates

The files monadic.py and diadic.py provide access unary operators and binary (two input) operators. Each file has a apply_operator function. These work on individual trits rather than whole trytes. 

The ternary equivalents of AND and OR are MIN and MAX. AND and Min return the lowest operand and OR and MAX return the highest operand.

## Gates provided

Monadic:
- constNeg: always returns n
- constZero: always returns z
- constPos: always returns p
- identity: returns the input unchanged
- clampDown: return n on n, otherwise z
- clampUp: return p on p, otherwise z
- isNeg, false: returns p on n, otherwise n
- isZero, unknown: returns p on z, otherwise n
- isPos, true: returns p if input is p, otherwise n
- notNeg: returns n on n, otherwise p
- notZero, known: returns n on z, otherwise p
- notPos: returns n on p, otherwise p
- inc: returns input + 1 with p rolling over to n
- dec: returns input - 1 with n rolling over to p
- negate: returns p on n, n on p, z on z

Diadic:
- min: roughly equivalent to AND, returns the lowest of two values
- max: roughly equivalent to OR, returns the highest of two values
- antimin: negated min
- antimax: negated max
- sum: returns the sum or two trits without a carry - see consensus
- 

Registers