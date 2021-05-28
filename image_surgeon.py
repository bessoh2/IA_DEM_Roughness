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

  
  
  
def tile_slicer(im, shape):
    """Takes image and divides it into multiple tiles with equal specified shape.
    Shape should be a tuple with the desired tile size. Returns as a dicctionary with 
    tile locations as keys of data type tuple. Returns tiled image, preserved shapes for padded tiles,
    and locations for each original tile for stitching."""
    import numpy as np
    #import xarray as xr
    
    if type(shape) != tuple:
        print('The specified shape is not in tuple form.')
        return 
    
    im_shape = np.array(np.shape(im)) # the full shape of the image, tuple
    des_shape = np.array(shape)
    div = im_shape / des_shape
    for i in range(len(div)):
        div[i] = math.ceil(div[i])
    #print(div)
    for i in div: # Ends the function if the tile size is greater than the image
        if i < 1:
            print('The specified tile size is larger than the image.')
            return
    tile_num = int(np.prod(div))
    #print(tile_num, 'Tiles')
    
    shape_iter = list(shape)
    
    tile_dict = {}
    saved_locs = {}
    for i in range(1,int(div[1])+1): # iterates with different tiles locations until the whole image is captured 
        for j in range(1,int(div[0])+1):
            location = tuple([i,j])
            # subset slicing
            # vertical coordinates
            vh = j * shape_iter[0]
            vl = vh - shape_iter[0]
            hh = i * shape_iter[1]
            hl = hh - shape_iter[1]
            # print(f'{vl}:{vh}')
            # print(f'{hl}:{hh}')
            # ensures indexing is within the bounds
            if vh > list(im_shape)[0]: 
                vh = list(im_shape)[0]
            if hh > list(im_shape)[1]:
                hh = list(im_shape)[1]
            
            subset = im[vl:vh, hl:hh]
            saved_locs[location] = [vl, vh, hl, hh]
            tile_dict[location] = subset
            
    return tile_dict, saved_locs, im_shape
  
  
  
def pad_cutter(tiles, preserved_shapes):
    """Takes tiles that have had analysis performed on them and cuts out the padding"""
    for key in preserved_shapes.keys():
        im = tiles[key]
        #print(preserved_shapes[key])
        trim = list(preserved_shapes[key])
        trimd_im = im[0:trim[0],0:trim[1]]
        tiles[key] = trimd_im
        
    return tiles
  
  
  
def tif_stitch(tiles, saved_locs, im_shape):
    """Creates a background mask the size of the original image shape and uses it to stitch the tiles back together.
    """
    import numpy as np
    
    stitched_im = np.zeros(im_shape)
    for key in saved_locs.keys():
        location = saved_locs[key]
        im = tiles[key]
        
        stitched_im[location[0]:location[1], location[2]:location[3]] = im
    
    return stitched_im
  
  
  
  
