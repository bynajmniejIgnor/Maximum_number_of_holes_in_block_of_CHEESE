#!/usr/bin/python3
import os

class CheeseParticle:
	def __init__(self,index,visited,connections,location):
		self.index=index
		self.visited=visited
		self.connections=connections
		self.location=location
		#print("Made cheese ball of index",index)
	
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
		for h in range(height):
			for i in range(length): 
				for j in range(width):
					particles[i+j+h].location=[i,j,h]
					file.write(f"bpy.ops.mesh.primitive_uv_sphere_add(enter_editmode=False, align='WORLD', location=({particles[i+j+h].location[0]},{particles[i+j+h].location[1]},{particles[i+j+h].location[2]}), scale=({scale},{scale},{scale}))\n")
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

#bpy.context.space_data.shading.type = 'MATERIAL'
#bpy.data.materials["Material.001"].node_tree.nodes["Principled BSDF"].inputs[0].default_value = (0.8, 0.588643, 0.16654, 1)
#bpy.ops.object.select_all(action='SELECT')
#bpy.ops.object.make_links_data(type='MATERIAL')

if __name__=="__main__":
	width=7#int(input('Windexth of cheese: '))
	length=5#int(input('Length of cheese: '))
	height=6#int(input('Height of cheese: '))
	particles=[]
	for i in range(width*length*height):
		particles.append(CheeseParticle(i,0,[],[]))
	
	cheese=Cheese(particles,width,length,height)
	cheese.fromager()
	cheese.generate_cheese_blender_script("blender_full_cheese.py",0.7)
