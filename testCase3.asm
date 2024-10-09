.data
    val1: .word 5
    val2: .word 8
    result_or: .word 0
    result_sub: .word 0

.text
    lw $t0, val1
    lw $t1, val2

    sub $t2, $t0, $t1
    beq $t2, $zero, equal

    or $t3, $t0, $t1
    j end

equal:
    addi $t3, $zero, 0

end:
    j end
