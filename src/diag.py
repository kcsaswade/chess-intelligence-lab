from chesslab.engine.perft import divide
from chesslab.io.fen import parse_fen

KIWIPETE_FEN = "r3k2r/p1ppqpb1/bn2pnp1/2pP4/1p2P3/2N2N2/PPQBBPPP/R3K2R w KQkq - 0 1"

position = parse_fen(KIWIPETE_FEN)
parts = divide(position, 1)

print("count =", len(parts))
for move, count in parts:
    print(move, count)