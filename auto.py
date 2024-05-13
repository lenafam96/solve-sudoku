def auto(board, pya, sys=None):
    if sys == None or sys.platform == 'win32':
        pya.hotkey('alt', 'tab')
        # time.sleep(0.0001)
        for i in range(9):
            if i%2 == 0:
                for j in range(9):
                    pya.hotkey(str(board[i][j]))
                    # time.sleep(0.0001)
                    pya.hotkey('right')
                    # time.sleep(0.0001)
            else:
                for j in range(8, -1, -1):
                    pya.hotkey(str(board[i][j]))
                    # time.sleep(0.0001)
                    pya.hotkey('left')
                    # time.sleep(0.0001)
            pya.hotkey('down')
            # time.sleep(0.0001)
        pya.hotkey('alt', 'tab')
    elif sys.platform == 'darwin':
        pya.keyDown('command')
        pya.press('tab')
        pya.keyUp('command')

        # time.sleep(0.0001)
        for i in range(9):
            if i%2 == 0:
                for j in range(9):
                    pya.hotkey(str(board[i][j]))
                    # time.sleep(0.0001)
                    pya.hotkey('right')
                    # time.sleep(0.0001)
            else:
                for j in range(8, -1, -1):
                    pya.hotkey(str(board[i][j]))
                    # time.sleep(0.0001)
                    pya.hotkey('left')
                    # time.sleep(0.0001)
            pya.hotkey('down')
            # time.sleep(0.0001)
        pya.keyDown('command')
        pya.press('tab')
        pya.keyUp('command')
