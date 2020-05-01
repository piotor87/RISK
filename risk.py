import numpy as np
from collections import Counter

def dice_roll(n):
  '''
  Returns n sorted dice rolls 
  '''
  results = np.random.randint(5,size = n) +1 
  return np.array(sorted(results,reverse=True))



def roll(ad,dd):
  '''
  Simulates risk attack with ad attackers and dd defenders. Returns difference of dice
  '''
  size = min(ad,dd) # maximum number of losses in total
  attack_roll = dice_roll(ad)[:size]
  defense_roll = dice_roll(dd)[:size] + 0.01
  return np.sign(attack_roll - defense_roll)


def attack(a,d):
  '''
  Simulates single attack between a attackers and d defenders
  '''
  assert a>1 and d > 0

  #get number of dice. attack needs to leave one behind
  ad,dd = min(3,a-1),min(3,d)
  result = roll(ad,dd)

  a_loss = np.sum(result==-1)  
  d_loss = np.sum(result==1)
  return [a_loss,d_loss]


def outcome_prob(n= 1000):
  '''
  Tests outcome probs of single attack
  '''
  a_losses = [attack(4,3)[0] for elem in range(n)]
  c = Counter(a_losses)
  for key in c:
    print(key,c[key]/float(n))
      
#outcome_prob(100000)


def full_attack(a,d):
  '''
  Full attack between a attackers and d defenders. Returns the final number of troops for both defense and attack
  '''
  assert a>1 and d > 0
  while a>1 and d > 0 :
    a_loss,d_loss = attack(a,d)
    a -= a_loss
    d -= d_loss
  return a,d 

def simulate_attacks(a,d,n=100):
  
  a,d,n = int(a),int(d),int(n)
  #final troops for attack and defense
  attack,defense = list(map(np.array,zip(*[full_attack(a,d) for elem in range(n)])))

  a_wins,d_wins = attack[attack>1],defense[defense>0]
  w_prob,d_prob = len(a_wins)/float(n),len(d_wins)/float(n)

  if w_prob:
    w_avg,w_std = a_wins.mean(),a_wins.std()
    print(f"Attack: {w_prob} {round(w_avg,2)} {round(w_std,2)}")

  if d_prob:
    d_avg,d_std = d_wins.mean(),d_wins.std()
    print(f"Defense: {d_prob} {round(d_avg,2)} {round(d_std,2)}")


a = input('attack?')
d = input('defense?')
n = input('rounds?')

results = simulate_attacks(a,d,n)
