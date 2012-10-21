import matplotlib as mpl
from matplotlib import pyplot as plt
from matplotlib.patches import Rectangle
import numpy as np

# Before we start, set the Artist parameter defaults
# Check this website out for reference: 
##      http://matplotlib.org/users/customizing.html

# Try mpl.rc(group, **kwargs) 
# instead of mpl.rcParams['property'] = value

# Create mainframe
f,axs = plt.subplots(4,4)

###### Modify Artist parameters ######

def label_border_axes_only():
    '''Only the bottom & right axes have labeled axes.
       This prevents cluttering.'''
    for i in range(4):
        for j in range(4):
            if i != 3:
                axs[i,j].set_xticks([])
            else:
                axs[i,j].xaxis.tick_bottom()
            if j != 3:
                axs[i,j].set_yticks([])
            else:
                axs[i,j].yaxis.tick_right()

label_border_axes_only()

def add_text(ax, theText):
	"""Add 'Sepal Length', 'Sepal Width', 'Petal Length',
	'Petal Width' labels to the diagnal axes on the
	upper-left corner."""
	ax.text(0.05,0.9,theText,horizontalalignment='left',
		verticalalignment='center',transform=ax.transAxes)
    # transform=ax.transAxes means (0,0) is BL corner
    # (1,1) is TR corner, etc etc

add_text(axs[0,0],'Sepal Length')
add_text(axs[1,1],'Sepal Width')
add_text(axs[2,2],'Petal Length')
add_text(axs[3,3],'Petal Width')

""" DOESN'T WORK
def turn_on_grid():
	'''Turn on grid for all axes'''
	for i in range(4):
		for j in range(4):
			axs[i,j].grid(True)

turn_on_grid()
"""

###### Load & plot the data ######

dt = [  ('slen',float),
        ('swid',float),
        ('plen',float),
        ('pwid',float),
        ('species',(str,25))  ]
tab = np.loadtxt('anderson_iris_data_parsed.txt',dt)

# Set up plots for slen vs slen, slen vs swid, ... , pwid vs pwid
# 'cats' stands for 'categories'
cats = ['slen','swid','plen','pwid']
species2color = {   'Isetosa':'r',
                    'Iversicolor':'g',
                    'Ivirginica':'b'   }

for i in range(4):
    for j in range(4):
        axs[i,j].scatter(  tab[cats[i]],tab[cats[j]],
                            c='0.75'  ) # Gray for now

###### Event Handling ######


pressed = False
orig_colors = [0.75,0.75,0.75,1]
num = len(tab['slen'])

def on_press(event):
    '''# reset colors back to original
    for i in range(4):
        for j in range(4):
            scat = axs[i,j].collections[0]
            scat.set_color(orig_colors) '''
    for row in axs:
        for ax in row:
            # remove all rectangles on all axes
            if ax.patches != []:
                ax.patches[0].remove()
            # re-add dummy rectangle to ensure all axes have rect instances
            ax.add_patch(Rectangle((0,0),0,0,alpha=0.2))
    # when mouse button is pressed, set pressed to True and 
    # select the rectangle inside the axes that contains the mouse-event.
    curr_ax = event.inaxes
    # if mouse clicked outside an axes, return
    if not curr_ax: return
    curr_rect = curr_ax.patches[0]
    curr_rect.set_xy((event.xdata,event.ydata))
    global pressed
    pressed = True
    curr_ax.figure.canvas.draw()
    
def on_motion(event):
    global pressed
    if pressed:
        curr_ax = event.inaxes
        curr_rect = curr_ax.patches[0]
        (x0, y0) = curr_rect.xy
        x1 = event.xdata
        y1 = event.ydata
        curr_rect.set_width(x1 - x0)
        curr_rect.set_height(y1 - y0)
        curr_ax.figure.canvas.draw()

def on_release(event):
    global pressed
    pressed = False
    curr_ax = event.inaxes
    curr_rect = curr_ax.patches[0]
    # Select the points contained in rectangle
    m, n = 0, 0
    for i in range(4):
        for j in range(4):
            if axs[i,j] == curr_ax:
                m, n = i, j
    (x0, y0) = curr_rect.xy
    x1 = x0 + curr_rect.get_width()
    y1 = y0 + curr_rect.get_height()
    left_bound = min(x0,x1)
    right_bound = max(x0,x1)
    bottom_bound = min(y0,y1)
    top_bound = max(y0,y1)
    xs, ys = tab[cats[m]], tab[cats[n]]
    inside_xbools_a = left_bound <= xs 
    inside_xbools_b = xs <= right_bound
    inside_xbools = inside_xbools_a & inside_xbools_b
    inside_ybools_a = bottom_bound <= ys
    inside_ybools_b = ys <= top_bound
    inside_ybools = inside_ybools_a & inside_ybools_b
    inside_xybools = inside_xbools & inside_ybools
    # Change the other axes' points that are associated to the points
    # inside the current axes' rectangle.
    for i in range(4):
        for j in range(4):
            scat = axs[i,j].collections[0]
            newcolors = np.tile(orig_colors, (num, 1))
            for p in range(num):
                if inside_xybools[p]:
                    newcolors[p] = [0, 0.75, 0.75, 1]
            
            scat.set_color(newcolors)
            
    curr_ax.figure.canvas.draw()

f.canvas.mpl_connect('button_press_event', on_press)
f.canvas.mpl_connect('motion_notify_event', on_motion)
f.canvas.mpl_connect('button_release_event', on_release)



###### Run the code ######
def main():
	plt.show()

if __name__ == '__main__':
	main()