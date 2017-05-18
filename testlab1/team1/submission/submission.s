main:
        li      $a0, -0x1234    # load the number to be converted into $a0
        la      $a1, buffer     # load the address of buffer for
                                #   ASCII decimal into $a1
        jal     hex2dec         # call the subroutine

# print out the result of the conversion using
# the system call print_int

        move    $a0, $v0        # initialize a0 to buffer
        li      $v0, 4          # tell syscall to do the print_string function
        syscall                 # make the call

# print a newline character
        la      $a0, str_newline# load a0 with the address of the char
        li      $v0, 4          # invoke system call no. 4
        syscall                 # make the actual call

# Return to OS

        li      $v0, 10         # return to the OS by call sys call no. 10
        syscall                 # make the actual call

next:
	li      $t1, 10         # for dividing by 10
        la      $t2, 11($a1)    # set $t2 to end of buffer
while_loop:
        beqz    $a0, done_while

        div     $a0, $t1        # divide $a0 by 10
        mflo    $a0             # put quotient back into $a0
	mfhi    $t3             # put remainder ( < 10 ) into $t3
        add     $t3, $t3, 0x30  # convert to ascii decimal
        subu    $t2, $t2, 1     # decrement buffer pointer
        sb      $t3, ($t2)      # store it in the next available location
