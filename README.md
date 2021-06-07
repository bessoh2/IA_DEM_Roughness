# IA_DEM_Roughness
Using Image Analysis techniques to identify pixels of a DEM with low surface roughness and slope

## Project Goals
* Learn about the posibilities of image analysis techniques for use with satellite data
* Create a computationally efficient moving window function for use on large images
* Develop a tiling and stitching function to reduce the size of the image being worked on while preserving the original location of each tile
* Identify areas of low slope and low surface roughness for use with ICESat-2 satellite data

## General Workflow
1. Run the FirstLookGM notebook to find the standard deviation that is most common at Grand Mesa, a location where ICESat-2 has been known to perform with high accuracy. You will need a DEM of Grand Mesa, which can be downloaded from https://nsidc.org/data/ASO_3M_SD/versions/1
2. Run the Terrain_Roughness_Slope notebook. This will require a DEM of the study area (in our original case, this is Tuolumne Meadows, available here: https://nsidc.org/data/ASO_3M_SD/versions/1 ) as well as a .csv with ICESat-2 points with a geometries column (which can be output during preprocessing by loading the downloaded and processed data into a geodataframe and then outputting as a .csv: raw data can be downloaded from: https://nsidc.org/data/atl08 ). In this study, we ran code on a subset image from the Tuolumne DEM, with an image size of 5000x5000 pixels. 
3. If the file size is extremely large, first use the slice_and_stitch.py function to tile the original DEM into tiles, then run the standard deviation function (and any other desired analysis) on each tile before stitching those tiles back together.
4. For more information on our specific project, please see our poster at https://github.com/bessoh2/IA_DEM_Roughness/blob/main/Final_Project_ICESat.pdf:

# Function Documentation

## tile_slicer

**tile_slicer(image, shape)**

  **Short Summary:**

    Slices an image into tiles of specified shape.
    
  **Extended Summary:**
  
    Divides a given image into uniform tiles (except for at the edges) of specified shape. 
    Returns the tiles in a dictionary with the location of each
    of the tiles as keys and the tiles as values.
  
  **Parameters:** 
                  
                  image : array_like
                    Input image.
                    
                  shape : tuple of ints
                    Desired tile size as a two dimensional shape.
                    
  **Returns:**  
  
               tile_dict : dictionary (keys : tuple of ints; values : array_like)
                  The keys are the original tile locations with the origin as the top left corner, and the values are the tiles.
                  
               saved_locs : dictionary (keys: tuple of ints; values : list of ints)
                  The keys are the original tile locations with the origin as the top left corner, and the values are the locations used to subset the tiles.
                  
               im_shape : tuple of ints
                  The shape of the original image.
                  
  **Examples:**
  
     >>> im = [a 5000x5000 image stored as an array]
     >>> tiles, locs, shape = tile_slicer(im, (500,500))
     >>> print(tiles)
     {(1, 1): <xarray.DataArray (y: 500, x: 500)>
     array([[2211.215 , 2212.88  , 2213.9575, ..., 2928.8174, 2930.355 , 2931.82  ],
       [2212.0874, 2213.885 , 2214.6226, ..., 2929.85  , 2931.65  , 2932.6226],
       [2212.7224, 2214.465 , 2215.1924, ..., 2930.425 , 2931.965 , 2933.4575],
       ...,
       [2526.4375, 2527.02  , 2526.825 , ..., 2780.78  , 2780.68  , 2780.795 ],
       [2526.25  , 2526.345 , 2526.0024, ..., 2780.7576, 2780.725 , 2780.845 ],
       [2525.36  , 2525.6875, 2525.78  , ..., 2780.6375, 2780.8875, 2780.9824]],
      dtype=float32)...
      >>> print(locs)
      {(1, 1): [0, 500, 0, 500], (1, 2): [500, 1000, 0, 500]...
      >>> print(shape)
      [5000 5000]
     
                  
## tif_stitch

**tif_stitch(tiles, saved_locs, im_shape)**
  
  Takes the outputs from tile_slicer and stitches the image back together.
  
  **Parameters:**
  
                  tiles : dictionary (keys : tuple of ints; values : array_like)
                  The keys are the original tile locations with the origin as the top left corner, and the values are the tiles.
                  
                  saved_locs : dictionary (keys: tuple of ints; values : list of ints)
                  The keys are the original tile locations with the origin as the top left corner, and the values are the locations used to subset the tiles.
                  
                  im_shape : tuple of ints
                  The shape of the original image.
                  
  **Returns:**
  
                  stitched_im : array_like
                    The stitched image.
                    
  **Examples:**
  
    >>> im = [an image stored as an array]
    >>> 
    
