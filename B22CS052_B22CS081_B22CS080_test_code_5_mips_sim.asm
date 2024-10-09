.data
    val1: .word 5

.text
    lw $t0, val1
    addi $t0, $t0, 1
    add $t1, $zero, $zero
    add $t2, $zero, $zero
loop:
    slt $t3, $t2, $t0
    beq $t3, $zero, exit
    add $t1, $t1, $t2
    addi $t2, $t2, 1
    j loop

exit:



