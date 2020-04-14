import numpy as np
from collections import defaultdict as dd

def dice_roll(n,add = 0):
  '''
  Returns n sorted dice rolls 
  '''
  results = np.random.randint(5,size = n) +1 + add
  results = np.array(sorted(results,reverse=True))

  return results




def roll(ad,dd):
  '''
  Simulates risk attack with ad attackers and dd defenders
  '''
  size = min(ad,dd)
  # returns size best rolls for each side
  attack_roll = dice_roll(ad)[:size]
  defense_roll = dice_roll(dd,0.01)[:size]

  return np.sign(attack_roll - defense_roll)


def attack(a,d):
  '''
  Simulates single attack between a attackers and d defenders
  '''
  assert a>0 and d > 0

  #get number of dice
  ad = min(3,a)
  dd = min(3,d)

  result = roll(ad,dd)
  a_loss = np.sum(result==-1)  
  d_loss = np.sum(result==1)
  return [a_loss,d_loss]


def outcome_prob(n= 1000):
  '''
  Tests outcome probs of single attack
  '''
  a = dd(int)
  for i in range(n):
    s = attack(3,3)
    s = '_'.join(list(map(str,s)))
    a[s] += 1
  for key in a:
    val = a[key]
    a[key] = round(val/float(n),2)
  return a


def full_attack(a,d):
  '''
  Full attack between a attackers and d defenders
  '''
  assert a>0 and d > 0
  while a>0 and d > 0 :
    a_loss,d_loss = attack(a,d)
    a -= a_loss
    d -= d_loss

  return a,d 

def simulate_attacks(a,d,n=1000):
  a,d = int(a),int(d)
  awins,dwins = [],[]
  for i in range(n):
    s = full_attack(a,d)
    awins.append(s[0])
    dwins.append(s[1])

  for wins in [awins,dwins]:
    res = analysis(wins)
    print(res)
  

def analysis(wins):
  n = len(wins)
  wins = np.array(wins)
  wins = wins[wins>0]
  prob = len(wins)/float(n)
  avg = wins.mean()
  std = wins.std()
  return prob,avg,std

a = input('attack?')
d = input('defense?')
results = simulate_attacks(a,d)

