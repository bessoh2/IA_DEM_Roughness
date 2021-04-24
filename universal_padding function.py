def universal_padding(tile, shape, top, bottom, left, right):
    """Takes a subset from an image and pads specified edges with NaN values 
    to fit a standard array size. Requires True/False inputs for each edge, 
    as well as a desired array shape. The edges should only be adjacent, never opposite."""
    import numpy as np
    
    vert = np.array([0,0])
    horiz = np.array([0,0])
    
    tile_size = np.shape(tile) # Finds the shape of the tile
    t_array = np.array(tile_size) # Converts the shape from a tuple into an array
    
    pad_width = np.array(shape) - t_array # Should be a positive value
    
    if pad_width.all() < 0:
        print('The given tile is larger than the specified shape')
        return
    
    if bottom==True:
        vert[1] += pad_width[0]
    elif top==True:
        vert[0] += pad_width[0]
    
    if right==True:
        horiz[1] += pad_width[1]
    elif left==True:
        horiz[0] += pad_width[1]
            
    vert = tuple(vert)
    horiz = tuple(horiz)
    padded_tile = np.pad(tile, (vert, horiz), 'constant', constant_values=np.nan)
    
    return padded_tile
