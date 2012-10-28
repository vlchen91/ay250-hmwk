from MPLFigureEditor import *
from enthought.traits.api import HasTraits, Str, Button
from enthought.traits.ui.api import View, Item, Group, HGroup

import urllib2
import simplejson
import socket
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import image as mpimg
import os
from skimage import img_as_float
from skimage.filter import threshold_otsu, canny, tv_denoise
import scipy.ndimage as ndi



class ImageSearch(HasTraits):
    queryString = Str("Monty Python, humour")
    run_query = Button("Run query")
    image_url = Str
    im = np.zeros((1,1,3))
    orig = im.copy()
    figure = Instance(Figure, ())
    
    otsu_threshold_color = Button("Threshold (color)")
    otsu_threshold_gray = Button("Threshold (gray)")
    gauss = Button("Gaussian Filter (sigma=3)")
    canny_edge = Button("Edges (canny)")
    original= Button("Original")

    def _otsu_threshold_color_fired(self):
        self.im = self.orig

        thresh = threshold_otsu(self.im)
        # np takes care of broadcasting
        binary = self.im > thresh
        self.im = binary
        try:
            self.axes.imshow(self.im)
            self.figure.canvas.draw()
        except:
            pass

    def _otsu_threshold_gray_fired(self):
        self.im = self.orig
        # Convert im from RGB to grayscale (3 channels)
        r,g,b = np.rollaxis(self.im,axis=-1)
        gray = 0.299*r + 0.587*g + 0.114*b

        thresh = threshold_otsu(gray)
        binary = gray > thresh
        new_im = np.dstack((binary,binary,binary))
        self.im = new_im
        try:
            self.axes.imshow(self.im)
            self.figure.canvas.draw()
        except:
            pass

    def _gauss_fired(self):
        self.im = self.orig
        r,g,b = np.rollaxis(self.im,axis=-1)
        gaussed_r = ndi.gaussian_filter(r,sigma=3)
        gaussed_g = ndi.gaussian_filter(g,sigma=3)
        gaussed_b = ndi.gaussian_filter(b,sigma=3)
        self.im = np.dstack((gaussed_r,gaussed_g,gaussed_b))
        try:
            self.axes.imshow(self.im)
            self.figure.canvas.draw()
        except:
            pass

    def _canny_edge_fired(self):
        self.im = self.orig
        r,g,b = np.rollaxis(self.im,axis=-1)
        edge_r = canny(tv_denoise(r, weight=1))
        edge_g = canny(tv_denoise(g, weight=1))
        edge_b = canny(tv_denoise(b, weight=1))
        edges = edge_r + edge_g + edge_b
        self.im = np.dstack((edges,edges,edges))
        self.im[self.im > 0.] = 1.
        try:
            self.axes.imshow(self.im)
            self.figure.canvas.draw()
        except:
            pass        

    def _original_fired(self):
        self.im = self.orig
        try:
            self.axes.imshow(self.im)
            self.figure.canvas.draw()
        except:
            pass        

    def _run_query_fired(self):
        query = urllib2.quote(self.queryString.__str__(),'')
        # works only for mac/unix systems
        ip = socket.gethostbyname(socket.gethostname())
        url1 = 'https://ajax.googleapis.com/ajax/services/search/images?'
        temp = 'v=1.0&q=%s&userip=%s' % (query,ip)
        url1 = (url1 + temp)
        request = urllib2.Request(url1,None,{'Referer':'http://www.asdf.com/'})
        response1 = urllib2.urlopen(request)
        results = simplejson.load(response1)
        url2 = results['responseData']['results'][0]['url']
        
        opener = urllib2.build_opener()
        opener.addheaders = [('User-agent','Mozilla/5.0')]
        response2 = opener.open(url2)
        filename = 'my_image.' + url2.split('.')[-1]
        fout = open(filename,'wb')
        fout.write(response2.read())
        fout.close()

        self.im = mpimg.imread(filename,'rb')
        # matplotlib.image bug
        self.im = np.flipud(self.im)
        # standardize as float32
        self.im = img_as_float(self.im)
        target = None
        if self.im.shape[2] == 4: # RGBA
            target = np.zeros((self.im.shape[0],self.im.shape[1],3))
            r,g,b,a = np.rollaxis(self.im,axis=-1)
            target[...,0] = ((1 - a) * r) + (a * r)
            target[...,1] = ((1 - a) * g) + (a * g)
            target[...,2] = ((1 - a) * b) + (a * b)
        elif self.im.shape[2] == 3: # RGB
            target = self.im
        else: # gray
            target = np.dstack((self.im,self.im,self.im))

        # By this point, im & orig are both (converted) RGB images
        self.im = target
        self.orig = self.im.copy()
        try:
            self.image_url = str(url2)
            self.axes.imshow(self.im)
            self.figure.canvas.draw()
        except:
            pass



    view = View(
    			Group(
    					HGroup(
    							Item('queryString',label='Query string',springy=True),
    							Item('run_query',show_label=False),
    							label='Input',
    							show_border=True),
    					Group(
    							Item('image_url',style='readonly',show_label=False),
    							label='Image URL',
    							show_border=True),
    					Group(
    							Item('figure',editor=MPLFigureEditor(),
    								 show_label=False,
    								 width=600,
    								 height=400,
                                     springy=True),
                                label="Image Display",
                                show_border=True ),
                        HGroup(
                                Item('original',show_label=False),
                                Item('otsu_threshold_color',show_label=False),
                                Item('otsu_threshold_gray',show_label=False),
                                Item('gauss',show_label=False),
                                Item('canny_edge',show_label=False),
                                label="Image Manipulation Options",
                                show_border=True ) ),
				title='Google Image Search',
				resizable=True,
				height=0.80,width=0.60 )
    

    def __init__(self):
		super(ImageSearch,self).__init__()
		ax = self.figure.add_subplot(111)
		self.axes = ax
		self.f = self.figure
		ax.imshow(self.im)

ImageSearch().configure_traits()

