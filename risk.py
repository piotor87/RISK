import numpy as np
import random
from collections import defaultdict as dd

def dice_roll(n):
  '''
  Returns n dice rolls in order
  '''
  results = []
  for j in range(n):
    results.append(random.randint(1,6))
 
  return np.array(sorted(results,reverse = True))


def roll(ad,dd):
  '''
  Simulates risk attack with ad attackers and dd defenders
  '''
  size = min(ad,dd)
  attack_roll = dice_roll(ad)[:size]
  defense_roll = dice_roll(dd)[:size] +0.1

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

  awins,dwins = [],[]
  for i in range(n):
    s = full_attack(a,d)
    awins.append(s[0])
    dwins.append(s[1])

  awins = np.array(awins)
  dwins = np.array(dwins) 
  awins = awins[awins>0]
  aprob = len(awins)/n
  avg_a = awins.mean()
  
  dwins = dwins[dwins>0]
  dprob = len(dwins)/n
  avg_d = dwins.mean()
  print(aprob,dprob)
  print(avg_a,avg_d)
  
  


results = simulate_attacks(140,100)

