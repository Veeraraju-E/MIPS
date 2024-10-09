.data
    num1: .word 5
    num2: .word 4
    min: .word 0

.text
    lw $t0, num1
    lw $t1, num2
    slt $t2, $t0, $t1
    beq $t2, $zero, set_num2
    add $t3, $t0, $zero
    j end
set_num2:
    add $t3, $t1, $zero
end:
    j end
