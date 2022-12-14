#!/usr/bin/python3
import os
import copy
import random
import time

class CheeseParticle:
    def __init__(self,index,visited,connections,location):
        self.index=index
        self.visited=visited
        self.connections=connections
        self.location=location
        self.not_removable=0 
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
        for particle in self.particles:
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
        self.counter=0

    def generate_must_haves(self,cheese,verbose):
        c=0
        for h in range(cheese.height):
            for _ in range(cheese.length):
                self.left_wall.append(c)
                self.right_wall.append(c+width-1)
                c+=cheese.width
            for w in range(cheese.width):
                self.back_wall.append(w+h*cheese.width*cheese.length)
                self.front_wall.append(w+cheese.width*(cheese.length*(h+1)-1))
        for i in range(cheese.length*cheese.width):
            self.floor.append(i)
            self.ceiling.append(i+cheese.length*cheese.width*(cheese.height-1))
        if verbose==1:
            print("Left wall:",self.left_wall)
            print("Right wall:",self.right_wall)
            print("Back wall:",self.back_wall)
            print("Front wall:",self.front_wall)
            print("Floor:",self.floor)
            print("Ceiling:",self.ceiling)
    
    def check_must_haves(self,cheese):
        ok_table=[0]*6
        for particle in cheese.particles:
            for must in self.left_wall:
                if must==particle.index:
                    #print("Must particle found in left wall",must)
                    ok_table[0]=1
                    break
            for must in self.right_wall:
                if must==particle.index:
                    #print("Must particle found in right wall",must)
                    ok_table[1]=1
                    break
            for must in self.back_wall:
                if must==particle.index:
                    #print("Must particle found in back wall",must)
                    ok_table[2]=1
                    break
            for must in self.front_wall:
                if must==particle.index:
                    #print("Must particle found in front wall",must)
                    ok_table[3]=1
                    break
            for must in self.ceiling:
                if must==particle.index:
                    #print("Must particle found in ceiling",must)
                    ok_table[4]=1
                    break
            for must in self.floor:
                if must==particle.index:
                    #print("Must particle found in floor",must)
                    ok_table[5]=1
                    break
            if not 0 in ok_table:
                return True
        return False

    def avoid_eaten(self,cheese,particle,index=-1):
        for connection in particle.connections:
            if connection!=particle.index and connection!=index:
                return connection

    def condition_1(self,particle,c1,sub=0,v=0):
        all_good=True
        if len(particle.connections)-sub<c1:
            if v:
                print("Condition_1 failed for particle",particle,"particle has less than",c1,"connections!")
            all_good=False
        return all_good

    def condition_2(self,particle,cheese,c2,sub=0,v=0,eaten=-1):
        all_good=True
        if len(particle.connections)-sub==1:
            hook=self.avoid_eaten(cheese,particle)
            if len(cheese.particles[hook].connections)-1<c2:
                all_good=False
                if v:
                    print("Condition_2 failed for particle",particle,"particle",cheese.particles[particle.connections[0]],"has less than 5 connections!")
            return all_good
        else:
            if v:
                print("Condition_2 failed for particle",particle,"the number of connections is not equal to 1")
            return False

    def condition_3(self,particle,cheese,c3,sub=0,v=0,eaten=-1):
        all_good=True
        if len(particle.connections)==2:
            hook_1=self.avoid_eaten(cheese,particle)
            hook_2=self.avoid_eaten(cheese,particle,hook_1)
            if len(cheese.particles[hook_1].connections)-1<c3 or len(cheese.particles[hook_2].connections)-1<c3:
                all_good=False
                if v:
                    print("Condition_3 failed for particle",particle,"particle neighbours have less than 4 connections each:",cheese.particles[particle.connections[0]],cheese.particles[particle.connections[1]])
            return all_good
        else:
            if v:
                print("Condition_3 failed for particle",particle,"the number of connections is not equal to 2")
            return False
    
    def is_particle_good(self,cheese,particle,c1,c2,c3,v=0,sub=0):
        if not self.condition_1(particle,c1,sub): 
            if not self.condition_2(particle,cheese,c2,sub,v,particle.index):
                if not self.condition_3(particle,cheese,c3,sub,v,particle.index):
                    return False
        return True

    def check_structure(self,cheese,c1,c2,c3):
        all_good=False
        for particle in cheese.particles:
            if particle.index!=-1:
                all_good=True
                break
        for particle in cheese.particles:
            if particle.index==-1:
                continue
            if not self.is_particle_good(cheese,particle,c1,c2,c3):
                all_good=False
                break
        return all_good    

    def make_hole(self,index,cheese):
        for i in cheese.particles[index].connections:
            cheese.particles[i].connections.remove(index)
        cheese.particles[index]=self.empty
    
    def dfs(self,cheese,current):
        cheese.particles[current].visited=1
        for p in cheese.particles[current].connections:
            if cheese.particles[p].visited==0:
                self.dfs(cheese,p)
    
    def check_if_all_visited(self,cheese):
        for particle in cheese.particles:
            if particle.visited==0:
                return False
        return True

    def reset_visited(self,cheese):
        for particle in cheese.particles:
            particle.visited=0

    def solid_or_not(self,cheese):
        for particle in cheese.particles:
            if particle.index!=-1:
                self.dfs(cheese,0)
                break
        solid=self.check_if_all_visited(cheese)
        return solid

    def bruteforce_holes(self,cheese,c1,c2,c3):
        print("Bruteforcing holes...")
        self.generate_must_haves(cheese,0)
        number_of_particles=cheese.height*cheese.length*cheese.width
        perm='0'
        goal='1'*number_of_particles
        holes=0
        max_holes=0
        wip_cheese=copy.deepcopy(cheese)
        holesome_cheese=copy.deepcopy(cheese)
        c=0
        start=time.time()
        while not perm==goal:
            perm=bin(c).replace('0b','').zfill(number_of_particles)
            print(f"Most holes found {max_holes} | Trying:",perm,end="\r")
            for i in range(len(perm)):
                if perm[i]=='0':
                    self.make_hole(i,wip_cheese) #Stw??rz we wskazanym miejscu dziur??
            if self.check_structure(wip_cheese,c1,c2,c3): #Sprawdzenie wszystkich warunk??w dotycz??cych liczby po????cze??
                if self.check_must_haves(wip_cheese): #Sprawdzenie warunku kul ??ciennych
                    if self.solid_or_not(wip_cheese): #Sprawdzenie czy wygenerowany ser jest sp??jny (dfs)
                        holes=perm.count('0')
                        if holes>max_holes:
                            max_holes=holes
                            holesome_cheese=copy.deepcopy(wip_cheese)
            wip_cheese=copy.deepcopy(cheese)
            c+=1
        end=time.time()
        print("Maximal number of holes is:",max_holes)
        print("This took:",end-start)
        holesome_cheese.generate_cheese_blender_script('optimal.py',0.7) #Wygeneruj skrypt z wizualizacj?? otrzymanego sera

    def build_solution(self,cheese):
        solution=[]
        for particle in cheese.particles:
            if particle.index!=-1:
                solution.append(particle.index)
        return solution


    def grow_hole(self,cheese,start,c1,c2,c3): #backtracking
        neighbours=cheese.particles[start]
        can_eat=1
        for i in neighbours.connections:
            if not self.is_particle_good(cheese,cheese.particles[i],c1,c2,c3,0,1):
                cheese.particles[start].not_removable=1
                can_eat=0
                break
        if can_eat:
            self.make_hole(start,cheese)
        for i in neighbours.connections:
            if cheese.particles[i].not_removable==0:
                self.grow_hole(cheese,i,c1,c2,c3)
            
    def one_by_one(self,cheese,c1,c2,c3): #heuristic
        for particle in cheese.particles:
            can_eat=1
            for i in particle.connections:
                if not self.is_particle_good(cheese,cheese.particles[i],c1,c2,c3,0,1):
                    particle.not_removable=1
                    can_eat=0
                    break
            if can_eat:
                self.make_hole(particle.index,cheese)
    
    def one_by_all(self,cheese,c1,c2,c3):
        number_of_particles=cheese.width*cheese.length*cheese.height
        queue=list(range(number_of_particles))
        wip_cheese=copy.deepcopy(cheese)
        holesome_cheese=copy.deepcopy(cheese)
        holes=0
        max_holes=0
        start=time.time()
        for a in range(number_of_particles):
            print("Going through",a,", max holes found",max_holes,end='\r')
            queue.append(queue.pop(0))
            for i in queue:
                can_eat=1
                for neighbour in wip_cheese.particles[i].connections:
                    if not self.is_particle_good(wip_cheese,wip_cheese.particles[neighbour],c1,c2,c3,0,1):
                        wip_cheese.particles[i].not_removable=1
                        can_eat=0
                        break
                if can_eat:
                    holes+=1
                    self.make_hole(i,wip_cheese)
            if holes>max_holes:
                max_holes=holes
                holesome_cheese=copy.deepcopy(wip_cheese)
            holes=0
            wip_cheese=copy.deepcopy(cheese)
        end=time.time()
        print("This took:",end-start,"s")
        holesome_cheese.generate_cheese_blender_script("small_one_by_all.py",0.7)

if __name__=="__main__":
    width=3     #int(input('Windexth of cheese: '))
    length=3    #int(input('Length of cheese: '))
    height=2    #int(input('Height of cheese: '))
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
    #cheese.dump_cheese()
    #test.generate_must_haves(cheese,0)
    #test.bruteforce_holes(cheese,3,5,2) #cheese, bound for cond_1, 2, 3
    #test.grow_hole(cheese,0,3,5,2)
    test.one_by_all(cheese,3,4,2)
    #cheese.generate_cheese_blender_script("big_cgungus_growing_hole.py",0.7)
    #cheese.dump_cheese()
