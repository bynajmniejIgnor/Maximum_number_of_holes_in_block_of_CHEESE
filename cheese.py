#!/usr/bin/python3
import os
import copy

class CheeseParticle:
	def __init__(self,index,visited,connections,location):
		self.index=index
		self.visited=visited
		self.connections=connections
		self.location=location
	
	def __str__(self):
		return f"id:{self.index} connections:{self.connections} location:{self.location}"

class Cheese:
	def __init__(self,particles,width,lenght,height):
		self.particles=particles
		self.width=width
		self.length=length
		self.height=height
		
	def make_cheese_slice(self):
		c=0
		for i in range(length-1): #Connections from top to bottom
			for j in range(width):
				particles[i*width+j].connections.append((i+1)*width+j)
		
		for i in range(width*length-1): #Connections from left to right
			if c==width-1:
				c=0
				continue
			particles[i].connections.append(i+1)
			c+=1	
		
	def stack_cheese_slices(self):
		area=width*length
		for h in range(height):
			for i in range(area):
				for c in particles[i+area*(h-1)].connections:
					particles[i+area*h].connections.append(c+area)
					
	def solidify_cheese(self):
		area=width*length
		for h in range(height-1):
			for i in range(area):
				particles[i+area*h].connections.append(i+area*(h+1))

	def bond_the_CHEESE(self):
		for particle in particles:
			for i in particle.connections:
				if particle.index not in particles[i].connections:
					particles[i].connections.append(particle.index)
	
	def fromager(self):
		print("Generating the block of cheese...",end=' ')
		self.make_cheese_slice()
		self.stack_cheese_slices()
		self.solidify_cheese()
		self.bond_the_CHEESE()
		print("DONE!\n")
	
	def launch_blender(self,file_name):
		choice=input("Launch blender with generated file? (y/n): ")
		if choice=='n':
			return
		path='/usr/bin/blender'
		if os.path.exists(path)==False:
			print("Blender not found, check your PATH variable or install blender")
		else:
			command=f'{path} -P {file_name}'
			os.system(command)
	
	def generate_cheese_blender_script(self,file_name,scale):
		print("Generating",file_name, "...",end=' ')
		file=open(file_name,'w')
		file.write("import bpy\n")
		file.write("bpy.ops.object.select_all(action='SELECT')\n")
		file.write("bpy.ops.object.delete(use_global=False, confirm=False)\n")
		for particle in particles:
			if particle.index==-1:
				continue
			file.write(f"bpy.ops.mesh.primitive_uv_sphere_add(enter_editmode=False, align='WORLD', location=({particle.location[0]},{particle.location[1]},{particle.location[2]}), scale=({scale},{scale},{scale}))\n")
		print("DONE!\n")
		file.close()
		self.launch_blender(file_name)

	def dump_cheese(self):
		c=0
		l=0
		for particle in self.particles:
			print(particle,end='        ')
			c+=1
			l+=1
			if c==width:
				print()
				c=0
			if l==width*length:
				print()
				l=0

class Holemaker:	
	def __init__(self):
		self.left_wall=[]
		self.right_wall=[]
		self.front_wall=[]
		self.back_wall=[]
		self.floor=[]
		self.ceiling=[]
		self.empty=CheeseParticle(-1,0,[],[])
	def generate_must_haves(self,cheese):
		c=0
		for h in range(cheese.height):
			for l in range(cheese.length):
				self.left_wall.append(c)
				self.right_wall.append(c+width-1)
				c+=cheese.width
			for w in range(cheese.width):
				self.back_wall.append(w+h*cheese.width*cheese.length)
				self.front_wall.append(w+cheese.width*(cheese.length*(h+1)-1))
		for i in range(cheese.length*cheese.width):
			self.floor.append(i)
			self.ceiling.append(i+cheese.length*cheese.width*(cheese.height-1))
		print("Left wall:",self.left_wall)
		print("Right wall:",self.right_wall)
		print("Back wall:",self.back_wall)
		print("Front wall:",self.front_wall)
		print("Floor:",self.floor)
		print("Ceiling:",self.ceiling)

	def condition_1(self,particle):
		all_good=True
		if len(particle.connections)<3:
			#print("Condition_1 failed for particle",particle,"particle has less than 3 connections!")
			all_good=False
		return all_good

	def condition_2(self,particle,cheese):
		all_good=True
		if len(particle.connections)==1:
			hook=particle.connections[0]
			if len(cheese.particles[hook].connections)-1<5:
				all_good=False
				#print("Condition_2 failed for particle",particle,"particle",cheese.particles[particle.connections[0]],"has less than 5 connections!")
			return all_good
		else:
			#print("Condition_2 failed for particle",particle,"the number of connections is not equal to 1")
			return False

	def condition_3(self,particle,cheese):
		all_good=True
		if len(particle.connections)==2:
			hook_1=particle.connections[0]
			hook_2=particle.connections[1]
			if len(cheese.particles[hook_1].connections)-1<4 or len(cheese.particles[hook_2].connections)-1<4:
				all_good=False
				#print("Condition_3 failed for particle",particle,"particle neighbours have less than 4 connections each:",cheese.particles[particle.connections[0]],cheese.particles[particle.connections[1]])
			return all_good
		else:
			#print("Condition_3 failed for particle",particle,"the number of connections is not equal to 2")
			return False

	def check_structure(self,cheese):
		all_good=False
		for particle in cheese.particles:
			if not particle.index==-1:
				all_good=True
				break
		for particle in cheese.particles:
			if particle.index==-1:
				continue
			if not self.condition_1(particle): 
				if not self.condition_2(particle,cheese):
					if not self.condition_3(particle, cheese):
						all_good=False
						break
					else:
						print("Redemption at condition_3! Particles neighbours have at least 4 other connections each:\n",cheese.particles[particle.connections[0]],"\n",cheese.particles[particle.connections[1]])
				else:
					print("Redemption at condition_2! Particles neighbour has at least 5 different connections:",cheese.particles[particle.connections[0]])
		return all_good	

	def make_hole(self,index,cheese):
		for i in cheese.particles[index].connections:
			cheese.particles[i].connections.remove(index)
		cheese.particles[index]=self.empty
			
	def bruteforce_holes(self,cheese):
		print("Bruteforcing holes...")
		number_of_particles=cheese.height*cheese.length*cheese.width
		perm='0'
		goal='1'*number_of_particles
		holes=0
		max_holes=0
		wip_cheese=copy.deepcopy(cheese)
		holesome_cheese=copy.deepcopy(cheese)
		c=0
		while not perm==goal:
			perm=bin(c).replace('0b','').zfill(number_of_particles)
			print("Trying:",perm)
			for i in range(len(perm)):
				if perm[i]=='0':
					self.make_hole(i,wip_cheese)
			if self.check_structure(wip_cheese):
				print("Solution found")
				holes=perm.count('0')
				if holes>max_holes:
					print(holes)
					max_holes=holes
					holesome_cheese=copy.deepcopy(wip_cheese)
				break
			wip_cheese=copy.deepcopy(cheese)
			c+=1
		holesome_cheese.generate_cheese_blender_script('blender_cheese_o_holes.py',0.7)

#bpy.context.space_data.shading.type = 'MATERIAL'
#bpy.data.materials["Material.001"].node_tree.nodes["Principled BSDF"].inputs[0].default_value = (0.8, 0.588643, 0.16654, 1)
#bpy.ops.object.select_all(action='SELECT')
#bpy.ops.object.make_links_data(type='MATERIAL')

if __name__=="__main__":
	width=3#int(input('Windexth of cheese: '))
	length=3#int(input('Length of cheese: '))
	height=2#int(input('Height of cheese: '))
	particles=[]
	w=0
	l=0
	h=0
	for i in range(width*length*height):
		particles.append(CheeseParticle(i,0,[],[w,l,h]))
		w+=1
		if w==width:
			l+=1
			w=0
		if l==length:
			h+=1
			l=0
	
	cheese=Cheese(particles,width,length,height)
	cheese.fromager()
	#cheese.dump_cheese()
	test=Holemaker()
	cheese.dump_cheese()
	test.bruteforce_holes(cheese)
