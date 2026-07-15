from constants import *
import numpy as np
class Game:

    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.grid = np.zeros((rows, cols), dtype=int)
        self.players = []

    def add_player(self,player):
        self.players.append(player)
        player.id = len(self.players)
        r=player.start_pos[0]
        c=player.start_pos[1]
        for i in range(r-2,r+3):
            for j in range(c-2,c+3):
                if i>=0 and i<ROWS and j>=0 and j<COLS:
                    self.grid[i][j]=+player.id
        player.outside = False
        player.blocked = False
    
    def flood_fill(self, player):
        visited = np.zeros((self.rows, self.cols), dtype=bool)

        q = []
        head = 0

        for c in range(self.cols):
            if self.grid[0][c] != player.id and self.grid[0][c] != -player.id:
                visited[0][c] = True
                q.append((0, c))

            if self.grid[self.rows-1][c] != player.id and self.grid[self.rows-1][c] != -player.id:
                visited[self.rows-1][c] = True
                q.append((self.rows-1, c))

        for r in range(self.rows):
            if self.grid[r][0] != player.id and self.grid[r][0] != -player.id:
                visited[r][0] = True
                q.append((r, 0))

            if self.grid[r][self.cols-1] != player.id and self.grid[r][self.cols-1] != -player.id:
                visited[r][self.cols-1] = True
                q.append((r, self.cols-1))

        directions = [(1,0), (-1,0), (0,1), (0,-1)]

        while head < len(q):
            r, c = q[head]
            head += 1

            for dr, dc in directions:
                nr = r + dr
                nc = c + dc

                if nr < 0 or nr >= self.rows or nc < 0 or nc >= self.cols:
                    continue

                if visited[nr][nc]:
                    continue

                if self.grid[nr][nc] == player.id or self.grid[nr][nc] == -player.id:
                    continue

                visited[nr][nc] = True
                q.append((nr, nc))

        for r in range(self.rows):
            for c in range(self.cols):
                if not visited[r][c]:
                    self.grid[r][c] = player.id

        player.trail = []
        player.outside = False
        
    def update(self):
        next_positions={}
        for player in self.players:
            next_pos=(player.dir[1]+player.pos[0],player.dir[0]+player.pos[1])
            next_positions[player]=next_pos
        for (k,v) in next_positions.items():
            if k.alive:
                for other in next_positions.keys():
                    if other!=k and other.alive:
                        if self.grid[next_positions[other]]==-k.id or self.grid[v]==-k.id:
                            k.alive=False
                        if self.grid[v]==-other.id:
                            other.alive=False
                if self.grid[v]>0 and self.grid[v]!=+k.id:
                    k.blocked=True
                elif self.grid[v]==0 or self.grid[v]==+k.id:
                    k.blocked=False
                if v[0]<0 or v[0]>=self.rows or v[1]<0 or v[1]>=self.cols:
                    k.blocked=True
        for player in self.players:
            if player.alive and not player.blocked :
                old_outside=player.outside
                old_pos=player.pos
                player.pos=next_positions[player]
                if self.grid[player.pos]!=+player.id:
                    player.outside=True
                else:
                    player.outside=False
                if player.outside:
                    self.grid[player.pos]=-player.id
                    if self.grid[old_pos]!=+player.id:
                        player.trail.append(old_pos)
                if old_outside and not player.outside:
                    self.flood_fill(player)
            elif not player.alive :
                for trail_pos in player.trail:
                    self.grid[trail_pos]=0
                self.grid[player.pos]=0
                player.trail=[]
                
        # compute all next positions
        # head-on — same target cell kills both
        # move the players who survived
    
        
    def reset(self):
        self.grid = np.zeros((self.rows,self.cols),dtype=int)
        for player in self.players:
            player.reset()
            r=player.start_pos[0]
            c=player.start_pos[1]
            for i in range(r-2,r+3):
                for j in range(c-2,c+3):
                    if i>=0 and i<ROWS and j>=0 and j<COLS:
                        self.grid[i][j]=+player.id
            player.outside = False
            player.blocked = False

            
        