.data
    valA: .word 5
    valB: .word 5
    result: .word 0

.text
    lw $t0, valA
    lw $t1, valB
    beq $t0, $t1, equal
    addi $t2, $zero, 0
    j end
equal:
    addi $t2, $zero, 1
end:
