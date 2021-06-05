# IA_DEM_Roughness
Using Image Analysis techniques to identify pixels of a DEM with low surface roughness and slope

## Project Goals
* Learn about the posibilities of image analysis techniques for use with satellite data
* Create a computationally efficient moving window function for use on large images
* Develop a tiling and stitching function to reduce the size of the image being worked on while preserving the original location of each tile
* Identify areas of low slope and low surface roughness for use with ICESat-2 satellite data

# Function Documentation

## Image Slice and Stitch Goals
- Create a function that can slice an image into however many tiles of specified shape to reduce computing power for image analysis
- Create a function that will successfully stitch the tiles back together post-analysis into an image the same size as the original shape

## tile_slicer

**tile_slicer(image, shape)**

  Divides a given image into uniform tiles (except for at the edges) of specified shape. Returns the tiles in a dictionary with the location of each
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
