def tile_slicer(im, shape):
    """Takes image and divides it into multiple tiles with equal specified shape.
    Shape should be a tuple with the desired tile size. Returns as a dicctionary with 
    tile locations as keys of data type tuple."""
    import numpy as np
    
    if type(shape) != tuple:
        print('The specified shape is not in tuple form.')
        return 
    
    im_shape = np.array(np.shape(im)) # the full shape of the image, tuple
    des_shape = np.array(shape)
    div = im_shape / des_shape
    for i in range(len(div)):
        div[i] = math.ceil(div[i])
    print(div)
    for i in div: # Ends the function if the tile size is greater than the image
        if i < 1:
            print('The specified tile size is larger than the image.')
            return
    tile_num = int(np.prod(div))
    #print(tile_num, 'Tiles')
    
    shape_iter = list(shape)
    
    tile_dict = {}
    for i in range(1,int(div[1])+1): # iterates with different tiles locations until the whole image is captured 
        for j in range(1,int(div[0])+1):
            location = tuple([i,j])
            # subset slicing
            # vertical coordinates
            vh = j * shape_iter[0]
            vl = vh - shape_iter[0]
            hh = i * shape_iter[1]
            hl = hh - shape_iter[1]
            #print(f'{vl}:{vh}')
            #print(f'{hl}:{hh}')
            subset = im[vl:vh, hl:hh]
            tile_dict[location] = subset
            
    return tile_dict
