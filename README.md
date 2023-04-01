This project was made by alexfacehead in Python. It does not implement castling,
en passant, or pawn promotion. These are to-be-implemented, and I welcome any
advice on simplifying modularization. Enjoy the simple crappy chess game.

Features:
- Scoreboard (in red, both sides)
- Undo move button by pressing `u`
- Piece logic for everything but castling and en passant
- Turn-based, can't cheat!

**Install Instructions**

**For Windows**:
1. Have a working Python install.
2. Have a working `pip` install for Windows (skip to step 3 if you already have one)
3. Run `game.exe` in /python_chess/dist/

**For Linux**:
1. Have a working Python install.
2. Have a working `pip` install (skip to step 3 if you already have one)
3. Install `pygame` library using `pip install pygame`
4. Execute `chmod +x run_game.sh` if on Linux
5. Execute `./run_game.sh` and enjoy!