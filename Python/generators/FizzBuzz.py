# for i in range(1,101):print(""if i%5else"Fizz",""if i%7else"Buzz",i if i%5and i%7else"",sep="")
i=0;exec('print(i%5//4*"Fizz"+i%7//6*"Buzz"or-~i);i+=1;'*100)
# y=int(input());i=0;exec('print(i%5//4*"Fizz"+i%7//6*"Buzz"or-~i);i+=1;'*y)