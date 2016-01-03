'''
Created on 30.11.2015

@author: Kai
'''
import log
def calculate_probability(lam1, distributions):
    '''calculate the probability with 2 exponential distributions.
    for example: calculate_probability(10,[10,20])
    '''
    # calculate with 2 exponential distributions
    if len(distributions) != 2:
        log.show_error("it can just calculate with 2 exponential distributions")
    if lam1 not in distributions:
        log.show_error("lam1 is not in the tup")
    lam2 = 0
    # get the first number, if it equals lam1, set the second number to lam2
    # if it not equals lam1, set it to lam2
    temp = distributions[0]
    if temp == lam1:
        lam2 = distributions[1]
    else:
        lam2 = temp

    pro = float(lam2) / (lam1 + lam2)  
    pro = round(pro, 3)

    return pro  

if __name__ == "__main__":
    # test
    print calculate_probability(5, [5, 10])
    print calculate_probability(5, [5, 5])
    print calculate_probability(5, [5, 8])
