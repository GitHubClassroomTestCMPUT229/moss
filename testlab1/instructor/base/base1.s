main:
        li      $a0, -0x1234    # load the number to be converted into $a0
        la      $a1, buffer     # load the address of buffer for
                                #   ASCII decimal into $a1
        jal     hex2dec         # call the subroutine
