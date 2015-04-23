'''
Created on Apr 23, 2015

@author: Hannes Jensen
'''

import numpy as np
from scipy import fftpack
from power_spectrum import _get_dims, _get_k

def gaussian_random_field(dims, box_dims, power_spectrum, random_seed=None):
    '''
    Generate a Gaussian random field with the specified
    power spectrum.
    
    Parameters:
        * dims (tuple): the dimensions of the field in number
            of cells. Can be 2D or 3D.
        * box_dims (float or tuple): the dimensions of the field
            in cMpc.
        * power_spectrum (callable, one parameter): the desired 
            spherically-averaged power spectrum of the output.
            Given as a function of k
        * random_seed (int): the seed for the random number generation
            
    Returns:
        The Gaussian random field as a numpy array
    '''
    #Verify input
    assert len(dims) == 2 or len(dims) == 3
    
    #Generate FT map
    if random_seed != None:
        np.random.seed(random_seed)
    map_ft_real = np.random.normal(loc=0., scale=1., size=dims)
    map_ft_imag = np.random.normal(loc=0., scale=1., size=dims)
    map_ft = map_ft_real + 1j*map_ft_imag
    
    #Get k modes
    box_dims = _get_dims(box_dims, map_ft_real.shape)
    assert len(box_dims) == len(dims)
    k_comp, k = _get_k(map_ft_real, box_dims)
    k[np.abs(k) < 1.e-6] = 1.e-6
    
    #Scale factor
    boxvol = np.product(map(float,box_dims))
    pixelsize = boxvol/(np.product(map_ft_real.shape))
    scale_factor = pixelsize**2/boxvol
    
    #Scale to power spectrum
    map_ft *= np.sqrt(power_spectrum(k)/scale_factor)
    
    #Inverse FT
    map_ift = fftpack.ifftn(fftpack.fftshift(map_ft))
    
    #Return real part
    map_real = np.real(map_ift)
    return map_real
