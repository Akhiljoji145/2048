import json, random, tkinter as tk
from pathlib import Path

N=4
BG="#faf8ef"; DARK="#776e65"; BOARD="#bbada0"; EMPTY="#cdc1b4"
PALETTE={0:(EMPTY,DARK),2:("#eee4da",DARK),4:("#ede0c8",DARK),8:("#f2b179","white"),16:("#f59563","white"),32:("#f67c5f","white"),64:("#f65e3b","white"),128:("#edcf72","white"),256:("#edcc61","white"),512:("#edc850","white"),1024:("#edc53f","white"),2048:("#edc22e","white")}
BEST=Path.home()/".2048_desktop_best.json"

class Game:
 def __init__(self,root):
  self.root=root; root.title("2048 — Desktop"); root.configure(bg=BG); root.resizable(False,False)
  root.bind("<KeyPress>",self.key)
  self.score=0; self.best=self.load_best(); self.prev=None; self.keep=False; self.won=False; self.over=False
  outer=tk.Frame(root,bg=BG,padx=18,pady=16); outer.pack()
  top=tk.Frame(outer,bg=BG); top.pack(fill="x")
  tk.Label(top,text="2048",font=("Arial",36,"bold"),bg=BG,fg=DARK).pack(side="left")
  boxes=tk.Frame(top,bg=BG); boxes.pack(side="right")
  self.score_lbl=self.score_box(boxes,"SCORE"); self.best_lbl=self.score_box(boxes,"BEST")
  bar=tk.Frame(outer,bg=BG); bar.pack(fill="x",pady=(12,14))
  tk.Label(bar,text="Join the numbers and reach 2048.",bg=BG,fg=DARK,font=("Arial",10)).pack(side="left")
  self.btn(bar,"New Game",self.new_game).pack(side="right")
  self.btn(bar,"Undo",self.undo).pack(side="right",padx=7)
  self.grid=tk.Frame(outer,bg=BOARD,padx=8,pady=8); self.grid.pack()
  self.cells=[]
  for r in range(N):
   row=[]
   for c in range(N):
    w=tk.Label(self.grid,text="",width=4,height=2,font=("Arial",25,"bold"),bg=EMPTY,fg=DARK)
    w.grid(row=r,column=c,padx=5,pady=5,ipadx=7,ipady=8); row.append(w)
   self.cells.append(row)
  self.status=tk.Label(outer,text="Use the arrow keys to move tiles. U = Undo · R = Restart",bg=BG,fg=DARK,font=("Arial",10))
  self.status.pack(pady=(12,0)); self.new_game(); root.after(150,root.focus_force)
 def btn(self,parent,label,cmd):
  return tk.Button(parent,text=label,command=cmd,font=("Arial",10,"bold"),bg="#8f7a66",fg="white",activebackground="#776452",activeforeground="white",relief="flat",padx=12,pady=7,cursor="hand2")
 def score_box(self,parent,title):
  b=tk.Frame(parent,bg=BOARD,padx=12,pady=5); b.pack(side="left",padx=3)
  tk.Label(b,text=title,bg=BOARD,fg="#eee4da",font=("Arial",8,"bold")).pack()
  x=tk.Label(b,text="0",bg=BOARD,fg="white",font=("Arial",15,"bold")); x.pack(); return x
 def load_best(self):
  try:return int(json.loads(BEST.read_text()).get("best",0))
  except:return 0
 def save_best(self):
  try:BEST.write_text(json.dumps({"best":self.best}))
  except:pass
 def new_game(self):
  self.board=[[0]*N for _ in range(N)]; self.score=0; self.prev=None; self.keep=False; self.won=False; self.over=False
  self.add_tile(); self.add_tile(); self.status.config(text="Use the arrow keys to move tiles. U = Undo · R = Restart"); self.render()
 def add_tile(self):
  empty=[(r,c) for r in range(N) for c in range(N) if not self.board[r][c]]
  if empty:
   r,c=random.choice(empty); self.board[r][c]=4 if random.random()<.1 else 2
 def key(self,e):
  d={"Left":"left","Right":"right","Up":"up","Down":"down"}.get(e.keysym)
  if d:self.move(d); return "break"
  if e.keysym.lower()=="u":self.undo(); return "break"
  if e.keysym.lower()=="r":self.new_game(); return "break"
 def collapse(self,line):
  a=[x for x in line if x]; out=[]; gain=0; i=0
  while i<len(a):
   if i+1<len(a) and a[i]==a[i+1]:
    v=a[i]*2; out.append(v); gain+=v; i+=2
   else:out.append(a[i]); i+=1
  return out+[0]*(N-len(out)),gain
 def move(self,d):
  if self.over or (self.won and not self.keep):return
  old=[x[:] for x in self.board]; new=[[0]*N for _ in range(N)]; gain_total=0
  for i in range(N):
   line=old[i][:] if d in ("left","right") else [old[r][i] for r in range(N)]
   if d in ("right","down"):line.reverse()
   result,gain=self.collapse(line); gain_total+=gain
   if d in ("right","down"):result.reverse()
   if d in ("left","right"):new[i]=result
   else:
    for r in range(N):new[r][i]=result[r]
  if new==old:return
  self.prev=(old,self.score,self.won,self.keep,self.over)
  self.board=new; self.score+=gain_total
  if self.score>self.best:self.best=self.score; self.save_best()
  self.add_tile()
  if not self.won and any(2048 in row for row in self.board):
   self.won=True; self.status.config(text="You reached 2048! Choose Continue or New Game.")
   self.render(); self.win_dialog(); return
  if not self.can_move():self.over=True; self.status.config(text="Game over — choose New Game to play again.")
  self.render()
 def can_move(self):
  for r in range(N):
   for c in range(N):
    if not self.board[r][c]:return True
    if c+1<N and self.board[r][c]==self.board[r][c+1]:return True
    if r+1<N and self.board[r][c]==self.board[r+1][c]:return True
  return False
 def undo(self):
  if not self.prev:self.status.config(text="No move available to undo."); return
  self.board,self.score,self.won,self.keep,self.over=self.prev; self.prev=None; self.status.config(text="Last move undone."); self.render()
 def render(self):
  for r in range(N):
   for c in range(N):
    v=self.board[r][c]; bg,fg=PALETTE.get(v,("#3c3a32","white"))
    self.cells[r][c].config(text=str(v) if v else "",bg=bg,fg=fg,font=("Arial",25 if v<1024 else 19,"bold"))
  self.score_lbl.config(text=str(self.score)); self.best_lbl.config(text=str(self.best))
 def win_dialog(self):
  win=tk.Toplevel(self.root); win.title("2048 reached"); win.configure(bg=BG); win.resizable(False,False); win.transient(self.root); win.grab_set()
  tk.Label(win,text="You reached 2048!",font=("Arial",18,"bold"),bg=BG,fg=DARK,padx=24,pady=18).pack()
  row=tk.Frame(win,bg=BG); row.pack(pady=(0,18))
  def cont():
   self.keep=True; self.status.config(text="Keep going! Use the arrow keys."); win.destroy(); self.root.focus_force()
  self.btn(row,"Continue",cont).pack(side="left",padx=5)
  self.btn(row,"New Game",lambda:(win.destroy(),self.new_game())).pack(side="left",padx=5)

if __name__=="__main__":
 root=tk.Tk(); Game(root); root.mainloop()
