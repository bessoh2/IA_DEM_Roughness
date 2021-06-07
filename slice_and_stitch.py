"""
Function Documentation:

tile_slicer(image, shape)

  Short Summary:

    Slices an image into tiles of specified shape.
    
  Extended Summary:
  
    Divides a given image into uniform tiles (except for at the edges) of specified shape. 
    Returns the tiles in a dictionary with the location of each
    of the tiles as keys and the tiles as values.
  
  Parameters:
                  
                  image : array_like
                    Input image.
                    
                  shape : tuple of ints
                    Desired tile size as a two dimensional shape.
                    
  Returns:
  
               tile_dict : dictionary (keys : tuple of ints; values : array_like)
                  The keys are the original tile locations with the origin as the top left corner, and the values are the tiles.
                  
               saved_locs : dictionary (keys: tuple of ints; values : list of ints)
                  The keys are the original tile locations with the origin as the top left corner, and the values are the locations used to subset the tiles.
                  
               im_shape : tuple of ints
                  The shape of the original image.
                  
  Examples:
  
     >>> im = [a 5000x5000 image stored as an array]
     >>> tile_dict, saved_locs, im_shape = tile_slicer(im, (500,500))
     >>> print(tile_dict)
     {(1, 1): <xarray.DataArray (y: 500, x: 500)>
     array([[2211.215 , 2212.88  , 2213.9575, ..., 2928.8174, 2930.355 , 2931.82  ],
       [2212.0874, 2213.885 , 2214.6226, ..., 2929.85  , 2931.65  , 2932.6226],
       [2212.7224, 2214.465 , 2215.1924, ..., 2930.425 , 2931.965 , 2933.4575],
       ...,
       [2526.4375, 2527.02  , 2526.825 , ..., 2780.78  , 2780.68  , 2780.795 ],
       [2526.25  , 2526.345 , 2526.0024, ..., 2780.7576, 2780.725 , 2780.845 ],
       [2525.36  , 2525.6875, 2525.78  , ..., 2780.6375, 2780.8875, 2780.9824]],
      dtype=float32)...
     >>> print(saved_locs)
      {(1, 1): [0, 500, 0, 500], (1, 2): [500, 1000, 0, 500]...
     >>> print(im_shape)
      [5000 5000]
     
                  
tif_stitch

tif_stitch(tiles, saved_locs, im_shape)
  
  Takes the outputs from tile_slicer and stitches the image back together.
  
  Parameters:
  
                  tiles : dictionary (keys : tuple of ints; values : array_like)
                  The keys are the original tile locations with the origin as the top left corner, and the values are the tiles.
                  
                  saved_locs : dictionary (keys: tuple of ints; values : list of ints)
                  The keys are the original tile locations with the origin as the top left corner, and the values are the locations used to subset the tiles.
                  
                  im_shape : tuple of ints
                  The shape of the original image.
                  
  Returns:
  
                  stitched_im : array_like
                    The stitched image.
                    
  Examples:
  
    >>> im = tif_stitch(tile_dict, saved_locs, im_shape)
    >>> np.shape(im)
    (5000, 5000)
    
"""


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
