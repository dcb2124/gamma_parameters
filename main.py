import scipy.integrate as integrate
from scipy.stats import gamma
import numpy

def gamma_parameters(mean, stdev):

  #variance = stdev^2 = alpha * beta^2, mean = alpha*beta
  variance = stdev ** 2

  beta = variance/mean

  alpha = mean/beta

  print("(alpha, beta) = ")
  return (alpha, beta)

def lower_half(alpha, beta, lim):

  return integrate.quad(lambda x: gamma.pdf(x, alpha, scale = beta), 0, lim)[0]

def estimate_median(alpha, beta):

  #see https://en.wikipedia.org/wiki/Gamma_distribution#Median_calculation 
  # if alpha < 0.17, the second if returns negative, so we use a better approximation 
  if alpha < 0.17 and beta == 1:

    return numpy.exp(0.5772156649) * 2 ** (-1/alpha)

  elif beta == 1:
    a = 8/405
    b = 184/25515
    c = 2248/344525
    d = -19006408/15345358875

    return alpha - 1/3 + a*alpha**-1 + b*alpha**-2 + c*alpha**-3 + d*alpha**-4
  
  #otherwise just brute force it
  else:
    err = numpy.sqrt(alpha * beta**2)

    start = alpha * beta - err

    last = lower_half(alpha, beta, start)

    i = 0

    while last < .5:
      i+=1
      last = lower_half(alpha, beta, start + i)
      if last >= 0.5:
        break

    #return whichever one is closer to 50%
    bottom = lower_half(alpha, beta, start+i-1)
    top = lower_half(alpha, beta, start+i)
    if abs(bottom-0.5) < abs(top-0.5):
      return start+i-1
    else:
      return start+i


  

  
  




  









