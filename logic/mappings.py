import numpy as np
import logging


def standard(file, settings) -> np.array:

    # Screens cant resolve more than three colors
    xdim = file.shape[0]
    ydim = file.shape[1]
    tdim = file.shape[3]
    zdim = file.shape[4]
    channels = file.shape[2]


    mappedfile = np.zeros((xdim, ydim, 3, tdim, zdim))

    # First Parameter will be the channels according to the file layout that need to be mapped
    rmapping = [channel for channel in settings.rmapping[0] if channel < channels]
    gmapping = [channel for channel in settings.gmapping[0] if channel < channels]
    bmapping = [channel for channel in settings.bmapping[0] if channel < channels]
    map = [rmapping,gmapping,bmapping]

    # Case of More Channels than in Map is automatically handled

    for index, mappedchannels in enumerate(map):
        #Iterate over chosen channels
        if len(mappedchannels) > 1:
            channelsfromfile = np.nanmax(file.take(mappedchannels,axis=2),axis=2) #maxisp of taken channels
        elif len(mappedchannels) == 1:
            channelsfromfile = file[:,:,mappedchannels[0],:,:]
        else:
            channelsfromfile = np.zeros((xdim, ydim, tdim, zdim))

        #channelsfromfile.append() #as we are casting a maxisp projection this is not really important
        #channelsfromfile = np.array(channelsfromfile)

        #maxispofchannelsfromfile = np.nanmax(channelsfromfile, axis=2)
        mappedfile[:, :, index, :, :] = channelsfromfile



    logging.info("Returned colormap shape {0}".format(str(mappedfile.shape)))
    return mappedfile, {"Mapping":"Returned colormap shape {0}".format(str(mappedfile.shape))}

