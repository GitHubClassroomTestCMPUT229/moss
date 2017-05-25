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
main:
        li      $a0, -0x1234    # load the number to be converted into $a0
        la      $a1, buffer     # load the address of buffer for
                                #   ASCII decimal into $a1
        jal     hex2dec         # call the subroutine
f:
        li      $a0, -0x1234    # load the number to be converted into $a0
        la      $a1, buffer     # load the address of buffer for
                                #   ASCII decimal into $a1
        jal     hex2dec         # call the subroutine
main:
        li      $a0, -0x1234    # load the number to be converted into $a0
        la      $a1, buffer     # load the address of buffer for
                                #   ASCII decimal into $a1
        jal     hex2dec         # call the subroutine
