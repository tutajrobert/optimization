def style(matplotlib):
	#matplotlib.use('PDF')
	matplotlib.rc('font', **{'family': 'serif', 'serif': ['Computer Modern']}) 
	matplotlib.rcParams['text.usetex']=True
	matplotlib.rcParams['text.latex.unicode']=True
	matplotlib.rc('text', usetex=True)
	#matplotlib.rc('font',**{'family':'sans-serif','sans-serif':['Helvetica']})
