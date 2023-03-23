from Space import *
from Constants import *

from importlib.machinery import all_suffixes
from msilib.schema import Error
from matplotlib.pyplot import close
from numpy import empty
import math
import time

def DFS(g:Graph, sc:pygame.Surface):
    print('Implement DFS algorithm')

    open_set = [g.start.value]
    closed_set = []
    father = [-1]*g.get_len()
    
    while len(open_set) > 0:
        current_node_value = open_set.pop()
        
        closed_set.append(current_node_value)
        
        current_node = g.grid_cells[current_node_value]
        if g.is_goal(current_node):
            path = []
            while current_node_value != -1:
                path.append(current_node_value)
                current_node_value = father[current_node_value]
            path = path[::-1]
            node_temp = current_node_value
            T = True
            for node in reversed(path):
                g.grid_cells[node].set_color(grey)
                if T == False:
                    pygame.draw.line(sc, green, (g.grid_cells[node_temp].x, g.grid_cells[node_temp].y),(g.grid_cells[node].x, g.grid_cells[node].y), 2)
                else: 
                    T = False
                g.draw(sc)
                time.sleep(0.05)
                node_temp = node
                
            return 

        #
        current_node.set_color(yellow)
        current_node.draw(sc)
        pygame.display.flip()
        time.sleep(0.1)
      
        neighbors = g.get_neighbors(current_node)

        for neighbor in neighbors:
            if neighbor.value not in closed_set:
                open_set.append(neighbor.value)
                father[neighbor.value] = current_node_value
                neighbor.set_color(red)
                neighbor.draw(sc)
                pygame.display.flip()
                time.sleep(0.05)

        current_node.set_color(blue)
        g.draw(sc)
        pygame.display.flip()
        time.sleep(0.05)
    
    #TODO: Implement DFS algorithm using open_set, closed_set, and father
    #raise NotImplementedError('Not implemented')

def BFS(g:Graph, sc:pygame.Surface):
    print('Implement BFS algorithm')

    open_set = [g.start.value]
    closed_set = []
    father = [-1]*g.get_len()
    
    while len(open_set) > 0:
        
        current = open_set.pop(0)
        g.grid_cells[current].set_color(yellow)
        g.grid_cells[current].draw(sc)
        pygame.display.flip()
        time.sleep(0.05)
        
        if g.is_goal(g.grid_cells[current]):
            path = []
            while current != -1:
                path.append(current)
                current = father[current]
            path = path[::-1]
            node_temp = father[current]
            T = True
            for node in reversed(path):
                g.grid_cells[node].set_color(grey)
                if T ==False:
                    pygame.draw.line(sc, green, (g.grid_cells[node_temp].x, g.grid_cells[node_temp].y),(g.grid_cells[node].x, g.grid_cells[node].y), 2)
                else: 
                    T = False
                g.draw(sc)
                time.sleep(0.05)
                node_temp = node
            
            break

        closed_set.append(current)

        neighbors = g.get_neighbors(g.grid_cells[current])
        for n in neighbors:
            if n.value not in closed_set and n.value not in open_set:
                open_set.append(n.value)
                father[n.value] = current
                n.set_color(red)
                n.draw(sc)
                pygame.display.flip()
                time.sleep(0.05)

        g.grid_cells[current].set_color(blue)
        g.grid_cells[current].draw(sc)
        pygame.display.flip()
        time.sleep(0.05)

    
    #TODO: Implement BFS algorithm using open_set, closed_set, and father
    #raise NotImplementedError('Not implemented')

def UCS(g:Graph, sc:pygame.Surface):
    print('Implement UCS algorithm')

    open_set = {}
    open_set[g.start.value] = 0
    closed_set:list[int] = []
    father = [-1]*g.get_len()
    cost = [100_000]*g.get_len()
    cost[g.start.value] = 0
    
    while len(open_set) > 0:
        current_node = min(open_set, key = lambda k: open_set[k])
        current_cost = open_set[current_node]
        del open_set[current_node]
        closed_set.append(current_node)
        
        g.grid_cells[current_node].set_color(yellow)
        g.grid_cells[current_node].draw(sc)
        pygame.display.flip()
        time.sleep(0.05)

        if g.is_goal(g.grid_cells[current_node]):
            path = []
            while current_node != -1:
                path.append(current_node)
                current_node = father[current_node]
            path = path[::-1]
            node_temp = father[current_node]
            T = True
            for node in reversed(path):
                g.grid_cells[node].set_color(grey)
                if T == False:
                    pygame.draw.line(sc, green, (g.grid_cells[node_temp].x, g.grid_cells[node_temp].y),(g.grid_cells[node].x, g.grid_cells[node].y), 2)
                else:
                    T = False
                g.draw(sc)
                time.sleep(0.05)
                node_temp = node
                
            return

        x1 = g.grid_cells[current_node].x
        y1 = g.grid_cells[current_node].y
        
        for neighbor in g.get_neighbors(g.grid_cells[current_node]):
            if neighbor.value in closed_set:
                continue

            x2 = neighbor.x
            y2 = neighbor.y
            
            tentative_cost = cost[current_node] + math.sqrt((x1 - x2)**2 + (y1 - y2)**2)
            if tentative_cost < cost[neighbor.value]:
                father[neighbor.value] = current_node
                cost[neighbor.value] = tentative_cost
                open_set[neighbor.value] = tentative_cost

                if neighbor.value != g.start.value and neighbor.value != g.goal.value:
                    neighbor.set_color(red)
                    g.draw(sc)
                    time.sleep(0.05)
        
        g.grid_cells[current_node].set_color(blue)
        g.grid_cells[current_node].draw(sc)
        pygame.display.flip()
        time.sleep(0.05)
            
def heuristic(node1:Node, node2:Node):
    return ((node1.x - node2.x) ** 2 + (node1.y - node2.y) ** 2) ** 0.5

def AStar(g:Graph, sc:pygame.Surface):
    print('Implement A* algorithm')

    open_set = {}
    open_set[g.start.value] = 0
    closed_set:list[int] = []
    father = [-1]*g.get_len()
    cost = [100_000]*g.get_len()
    cost[g.start.value] = 0 
    
    while open_set:
        current_node_value = min(open_set, key=open_set.get)
        current_node = g.grid_cells[current_node_value]
        del open_set[current_node_value]
        closed_set.append(current_node_value)
        
        current_node.set_color(yellow)
        current_node.draw(sc)
        pygame.display.flip()
        time.sleep(0.05)
        
        if g.is_goal(current_node):
            path = []
            while current_node_value != -1:
                path.append(current_node_value)
                current_node_value = father[current_node_value]
            path = path[::-1]
            node_temp = father[current_node_value]
            T = True
            for node in reversed(path):
                g.grid_cells[node].set_color(grey)
                if T == False:
                    pygame.draw.line(sc, green, (g.grid_cells[node_temp].x, g.grid_cells[node_temp].y),(g.grid_cells[node].x, g.grid_cells[node].y), 2)
                else:
                    T = False
                g.draw(sc)
                time.sleep(0.05)
                node_temp = node
                
            return
        
        for neighbor in g.get_neighbors(current_node):
            if neighbor.value in closed_set:
                continue
    
            tentative_f_score = cost[current_node.value] + heuristic(neighbor, g.goal)
            
            if neighbor.value not in open_set or tentative_f_score < cost[neighbor.value]:
                father[neighbor.value] = current_node.value
                cost[neighbor.value] = cost[current_node.value]
                open_set[neighbor.value] = tentative_f_score
                neighbor.set_color(red)
                g.draw(sc)
            
        current_node.set_color(blue)
        current_node.draw(sc)
        pygame.display.flip()
        time.sleep(0.05)
            
    #     #TODO: Implement A* algorithm using open_set, closed_set, and father
    #     #raise NotImplementedError('Not implemented')
        