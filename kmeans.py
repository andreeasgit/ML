import sys
import csv
import random
import math
import time
from tkinter import *

def get_point_list(d, csv_file_name):
	point_list = []
	
	with open(csv_file_name, 'rt') as csv_file:
		csv_reader = csv.reader(csv_file, delimiter=' ')
		for row in csv_reader:
			flag = 0
			first_number_string = ""
			second_number_string = ""
			for element in row[0]:
				if str(element) == ',':
					flag = 1
				if str(element) != ',' and flag == 0:
					first_number_string += str(element)
				if str(element) != ',' and flag == 1:
					second_number_string += str(element)
			X = float(first_number_string)
			Y = float(second_number_string)	
			X *= 115
			Y *= 115
			if d == 1:
				point_list.append(X)
			if d == 2:
				tuple = (X,Y)
				point_list.append(tuple)
	return point_list

def get_initial_centroids(d, k, point_list):
	centroids = {}
	color_list = ["black", "navy", "green", "purple","firebrick1","red2","SeaGreen1", "dark green", "RoyalBlue1", "gold"]

	for iterator in range(1,int(k)+1):
		centroid = random.randint(1, len(point_list))-1
		if d == 1:
			centroid_x = point_list[centroid]
			tuple = (centroid_x, color_list[iterator-1])
		if d == 2:
			centroid_x = point_list[centroid][0]
			centroid_y = point_list[centroid][1]
			tuple = (centroid_x, centroid_y, color_list[iterator-1])
		centroids[iterator] = tuple
	return centroids

def get_cluster_list(d, point_list, centroids):
	cluster_list = []

	for point in point_list:
		dist_min = 1000000000.0
		cluster = ()
		for centroid in centroids:
			if d==1:
				dist = abs(centroids[centroid][0]-point)
			if d==2:
				dist = math.sqrt((centroids[centroid][0]-point[0])*(centroids[centroid][0]-point[0]) + (centroids[centroid][1]-point[1])*(centroids[centroid][1]-point[1]))
			if dist < dist_min:
				dist_min = dist
				if d == 1:
					cluster = (centroid, centroids[centroid][0])
				if d == 2:
					cluster = (centroid, centroids[centroid][0], centroids[centroid][1])
		tuple = (cluster, point)
		cluster_list.append(tuple)
		
	cluster_list = sorted(cluster_list, key=lambda x: x[0][0])
	return cluster_list

def get_new_centroids(d, cluster_list, old_centroids):
	new_centroids = {}
	
	for centroid in old_centroids:
		cluster = [item for item in cluster_list if item[0][0] == centroid]
		new_centroid_x = 0.0
		new_centroid_y = 0.0
		for element in cluster:
			if d == 1:
				new_centroid_x +=element[1]
			if d == 2:
				new_centroid_x +=element[1][0]
				new_centroid_y +=element[1][1]
		if d == 1:
			if len(cluster) != 0:
				new_centroid_x /= len(cluster)
			else: 
				new_centroid_x = old_centroids[centroid][0]
			tuple = (new_centroid_x, old_centroids[centroid][1])
		if d == 2:
			if len(cluster) != 0:
				new_centroid_x /= len(cluster)
				new_centroid_y /= len(cluster)
			else: 
				new_centroid_x = old_centroids[centroid][0]
				new_centroid_x = old_centroids[centroid][1]		
			tuple = (new_centroid_x, new_centroid_y, old_centroids[centroid][2])
			
		new_centroids[centroid] = tuple
		
	return new_centroids

def get_J(d, cluster_list, centroids):
	J = 0
	
	for centroid in centroids:
		cluster = [item for item in cluster_list if item[0][0] == centroid]
		for element in cluster:
			if d == 1:
				J += (element[1]-centroids[centroid][0])*(element[1]-centroids[centroid][0])
			if d == 2:
				J += (element[1][0]-element[1][1])*(element[0][1]-element[0][2])+(element[1][0]-element[1][1])*(element[0][1]-element[0][2])
	return J
		
def K_means (d, point_list, initial_centroids):

	print ("Initial centroids positions")
	if d == 1:
		before_positions = [(initial_centroids[item]) for item in initial_centroids]
		for element in before_positions:
			print(element[0]/115)
	if d == 2:
		before_positions = [(initial_centroids[item][0], initial_centroids[item][1]) for item in initial_centroids]
		for element in before_positions:
			print(element[0]/115, element[1]/115)
	print("\n")
	
	J_list = []
	
	cluster_list = get_cluster_list(d, point_list, initial_centroids)
	J = get_J(d, cluster_list, initial_centroids)
	J_list.append(J)
	#paint(d, cluster_list, initial_centroids)
	
	
	new_centroids = get_new_centroids(d, cluster_list,initial_centroids)
	cluster_list = get_cluster_list(d, point_list, new_centroids)
	J = get_J(d, cluster_list, new_centroids)
		
	if d == 1:
		after_positions =  [(new_centroids[item]) for item in new_centroids]
	if d == 2:
		after_positions = [(new_centroids[item][0], new_centroids[item][1]) for item in new_centroids]
	
	print ("Centroids positions after 1 iteration")
	if d == 1:
		for element in after_positions:
			print(element[0]/115)
	if d == 2:
		for element in after_positions:
			print(element[0]/115, element[1]/115)
	print("\n")
	
	t =1
	while set(before_positions)!=set(after_positions):
		before_positions = after_positions
		new_centroids = get_new_centroids(d, cluster_list,new_centroids)
		cluster_list = get_cluster_list(d, point_list, new_centroids)
		J = get_J(d, cluster_list, new_centroids)
		J_list.append(J)
		
		if d == 1:
			after_positions =  [(new_centroids[item]) for item in new_centroids]
		if d == 2:
			after_positions = [(new_centroids[item][0], new_centroids[item][1]) for item in new_centroids]
		t+=1
		print ("Centroids positions after", t, "iteration")
		
		if d == 1:
			for element in after_positions:
				print(element[0]/115)
		if d == 2:
			for element in after_positions:
				print(element[0]/115, element[1]/115)
		print("\n")
	
	
	return (cluster_list, new_centroids, J_list)
	
	
def draw_point(window, X, Y, color_name):
    x1, y1 = (X - 5), (Y - 5)
    x2, y2 = (X + 5), (Y + 5)
    window.create_oval(x1, y1, x2, y2, fill=color_name)

def paint(d, cluster_list, centroids):	
	master = Tk()
	master.title("K Means Clusters")
	w = Canvas(master, width=1000, height=700)
	w.create_line(0, 350, 999, 350, dash=(2,2))  
	w.create_line(500, 0, 500, 999, dash=(2,2)) 
	
	for element in cluster_list:
		for centroid in centroids:
			if int(element[0][0]) == centroid:
				if d == 1:
					draw_point(w, element[1]+500,350-0, centroids[centroid][1])
				if d == 2:
					draw_point(w, element[1][0]+500,350-element[1][1], centroids[centroid][2])
				
	w.pack(expand=YES, fill=BOTH)
	mainloop()

def main():
	d = int(sys.argv[1])
	#k = sys.argv[2]
	csv_file_name = sys.argv[2]

	point_list = get_point_list (d, csv_file_name)
	
	#J_min = 100000000000000.0
	best_k = -1
	J_list = []
	
	for k in [2, 3, 4, 5, 6, 7, 8, 9, 10]:
		initial_centroids = get_initial_centroids(d, k, point_list)	
	
		#cluster_list = get_cluster_list(d, point_list, initial_centroids)
		#paint(d, cluster_list, initial_centroids)
	
		result = K_means(d, point_list, initial_centroids)

		cluster_list = result[0]
		new_centroids = result[1]
		J = result[2]
		J_list.append((J,k))
	
	for element in J_list:
		print ("\nJ values for k=",element[1],":")
		for item in element[0]:
			print(item)
	
	max_difference = 0.0
	for element in J_list:
		for iterator in range(1, len(element[0])):
			difference = element[0][iterator-1] - element[0][iterator]
			if difference != 0.0 and difference > max_difference:
				max_difference = difference
				best_k = element[1]
	
	initial_centroids = get_initial_centroids(d, best_k, point_list)	
	result = K_means(d, point_list, initial_centroids)
	print("Best k found:", best_k)
	
	cluster_list = result[0]
	new_centroids = result[1]
	paint(d, cluster_list, new_centroids)

main()

