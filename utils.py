#contains general functions for use in multiple files. makes things nice and organized!

def get_piece_at(pieces, location):
    for piece in pieces:
        if piece._location == location:
            return piece