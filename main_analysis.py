"""
Part of this code is adapted from works licensed under Creative Commons:

- Lines 35–43: Adapted from a Stack Overflow Japan post by user "neco", available at
  https://ja.stackoverflow.com/questions/23275/  
  Licensed under CC BY-SA 3.0 (https://creativecommons.org/licenses/by-sa/3.0/)

- Lines 46–83: Copied from code by "Akehi", originally published at  
  https://akehi.github.io/containts/20161119_angle/anglelib.html  
  Licensed under CC BY 3.0, as specified in:  
  https://github.com/Akehi/Akehi.github.io/blob/master/LICENSE.txt  
  (https://creativecommons.org/licenses/by/3.0/)

This code as a whole is distributed under the Creative Commons Attribution-ShareAlike 3.0 (CC BY-SA 3.0) license.

Author: Azusa Kage (@kageazusa)
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import glob
import os
import copy

input_path = "../input/*.csv"
files = glob.glob(input_path)
files_sorted = sorted(files) #sort by file names

output_path = "../output"

threshold = 0.95 #filter by Likelihood

#calculate angle between two vectors
def angle(x, y):

    dot_xy = np.dot(x, y)
    norm_x = np.linalg.norm(x)
    norm_y = np.linalg.norm(y)
    cos = dot_xy / (norm_x*norm_y)
    rad = np.arccos(cos)

    return rad

#calculation of angles
vec = lambda x: x[:,np.newaxis]
pi = np.pi
cos = np.cos
sin = np.sin
atan2 = np.arctan2
d2r = np.deg2rad

def th2q(th):
    return vec(np.array([cos(th),sin(th)]))

def q2R(q):
    q2=vec(np.r_[-q[1],q[0]])
    qR=np.c_[q,q2]
    return qR
    
def qpls(q1,q2):
    q3=q2R(q2)@q1
    return q3

def qconj(q):
    q2=np.r_[q[0],-q[1]]
    return q2

def qdev(qtgt,qcur):
    return qpls(qtgt,qconj(qcur))

def q2th(q):
    return atan2(q[1],q[0])

def dev(thtgt,thcur,radian=True):
    f=1 if radian is True else d2r(1)    
    dq=qdev(th2q(f*thtgt),th2q(f*thcur))
    return q2th(dq)/f

def pls(th1,th2,radian=True):
    f=1 if radian is True else d2r(1)
    qp=qpls(th2q(f*th1),th2q(f*th2))
    return q2th(qp)/f


#Batch processing of data
for fi in files_sorted:
	#Data loading
	data = pd.read_csv(fi)

	#Filling NaN values if tip likelihood is below threshold
	df = copy.deepcopy(data)
	df.loc[df['tip_likelihood'] < threshold, ['tip_x', 'tip_y', 'base_x', 'base_y', 'posterior_x', 'posterior_y']] = np.nan

	#Filtering with tip_likelihood
	data = data[data["tip_likelihood"] >= threshold].reset_index(drop=True)

	#Trimming file names for saving
	#if live 0:41, if demembranated 0:39
	file_name = os.path.basename(fi)[0:39]

	#Save
	nan_name = "nan_" + file_name + ".csv"
	df.to_csv(os.path.join(output_path, nan_name), index=False)

    # Body rotation
    # Convert to vectors (posterior → base) and (base → tip)
    # There might be a smarter way to write this

	# Create an empty list for storing data
	vectors_bt = []
	vectors_bp = []

	for i in range(len(data)):
	    # Data extraction
	    vbt = np.array([[data["base_x"].iloc[i], data["base_y"].iloc[i]], [data["tip_x"].iloc[i], data["tip_y"].iloc[i]]])
	    vbp = np.array([[data["base_x"].iloc[i], data["base_y"].iloc[i]], [data["posterior_x"].iloc[i], data["posterior_y"].iloc[i]]])
	    vectors_bt.append(vbt)
	    vectors_bp.append(vbp)

    # Calculate the body angle
	angles_list = []

	for i in range(len(data)):
	    #base and posterior
	    vbp = vectors_bp[i][1].reshape(-1)  - vectors_bp[i][0].reshape(-1) 
	    a = np.arctan2(vbp[1], vbp[0])
	    angles_list.append(a)

	# Save the file
	body = pd.concat([data["time"], pd.Series(angles_list)], axis=1)
	body.columns = ["time", "angle"]
	file_body = "body_" + file_name + ".csv"
	body.to_csv(os.path.join(output_path, file_body), index=False)


	# Draw a graph
	plt.rcParams['font.family']='Arial'

	fig, ax =plt.subplots(figsize = [16,6])
	ax.set_xlabel("Time [sec]", size=24)
	ax.set_ylabel("Angle [rad]", size=24)
	ax.set_xlim([-1, 81])
	ax.set_xticks([0, 10, 20, 30, 40, 50, 60, 70, 80, 90], [0, 10, 20, 30, 40, 50, 60, 70, 80, 90], fontsize=18)
	ax.set_ylim([-np.pi*1.05, np.pi*1.05])
	ax.set_yticks([-np.pi, -np.pi/2, 0 , np.pi/2, np.pi],['-π', '-π/2', '0', 'π/2', 'π'], fontsize=18)

	# Horizontal axis
	t = data["time"]
	ax.plot(t, angles_list, alpha = 0.7)
	png_body = "body_" + file_name + ".png"
	plt.savefig(os.path.join(output_path, png_body), dpi=200)

	# Calculate the flagellar angle
    # Compute the angle between the vector from base to posterior and the vector from base to tip
	angle1 = []

	for i in range(len(data)):
	    vbt1 = vectors_bt[i][1] - vectors_bt[i][0]
	    vbt1 = vbt1.reshape(-1)
	    vbp1 = vectors_bp[i][1]-vectors_bp[i][0]
	    vbp1 = vbp1.reshape(-1)
	    ang1 = angle(vbt1, vbp1)
	    angle1.append(ang1)

	# Save the file
	fla = pd.concat([data["time"], pd.Series(angle1)], axis=1)
	fla.columns = ["time", "angle"]
	file_fla = "fla_" + file_name + ".csv"
	fla.to_csv(os.path.join(output_path, file_fla), index=False)


	# Draw a graph
	fig, ax =plt.subplots(figsize = [16,6])

	# Horizontal axis
	t = data["time"]
	ax.set_xlabel("Time [sec]", size=24)
	ax.set_ylabel("Angle [rad]", size=24)

	ax.plot(t, angle1, alpha=0.7)
	ax.set_xlim([-1, 64])
	ax.set_xticks([0, 10, 20, 30, 40, 50, 60, 70, 80, 90], [0, 10, 20, 30, 40, 50, 60, 70, 80, 90], fontsize=18)
	ax.set_ylim([-0.05, np.pi*1.05])
	ax.set_yticks([0 , np.pi/2, np.pi],['0', 'π/2', 'π'], fontsize=18)

	png_fla = "fla_" + file_name + ".png"
	plt.savefig(os.path.join(output_path, png_fla), dpi=200)


    # Cumulative body angle
    # Start with the differences
	deltas = []

	for i in range(len(angles_list) - 1):
	    delta = dev(angles_list[i+1], angles_list[i], radian=True)
	    deltas.append(delta[0])

	deltas = pd.Series(deltas)

	cumul_angles = pd.concat([pd.Series(angles_list[0]), deltas], axis=0).reset_index(drop=True)
	cumul_angles2 = cumul_angles.cumsum()

	# Save the file
	cumul_df = pd.concat([t, cumul_angles2], axis=1)
	cumul_df.columns = ["time", "angle"]
	file_cumul = "cumul_" + file_name + ".csv"
	cumul_df.to_csv(os.path.join(output_path, file_cumul), index=False)

	# Draw a graph
	fig, ax =plt.subplots(figsize = [16,6])

	# Horizontal axis
	t = data["time"]
	ax.set_xlabel("Time [sec]", size=24)
	ax.set_ylabel("Cumulative angle [rad]", size=24)
	ax.plot(t, cumul_angles2, alpha=0.7)

	cumul_png = "cumul_" + file_name + ".png"
	plt.savefig(os.path.join(output_path, cumul_png), dpi=200)

	# Approximation line
	a, b = np.polyfit(t[0:2000], cumul_angles2[0:2000], 1)

	# Summarize the results
	results = pd.DataFrame([a, b]).T
	results.columns = ["slope", "slice"]
	
	file_summary = "summary_" + file_name + ".csv"
	results.to_csv(os.path.join(output_path, file_summary), index=False)