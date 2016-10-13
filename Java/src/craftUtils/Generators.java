package craftUtils;

import java.util.ArrayList;

/**
 * 
 * @author CraftSpider
 */
public class Generators {
	
	public static void main(String[] args) {
		Generators gens = new Generators();
		for (int value : gens.genFibonacci(10, 0, 1)) {
			System.out.println(value);
		}
	}
	
	/**
	 * 
	 * @param length
	 * @return ArrayList<Integer>
	 */
	public ArrayList<Integer> genPrimes(int length) {
		ArrayList<Integer> primes = new ArrayList<Integer>();
		int numPrimes = 0;
		int curNum = 2;
		
		while(numPrimes < length) {
			for (int testVal = 2; testVal <= curNum; testVal++) {
				if (curNum % testVal == 0 && curNum != 2) {
					break;
				} else if (testVal >= curNum - 1) {
					primes.add(curNum);
					numPrimes++;
					break;
				}
			}
			curNum++;
		}
		
		return primes;
	}
	
	/**
	 * 
	 * @param length
	 * @param start1
	 * @param start2
	 * @return ArrayList<Integer>
	 */
	public ArrayList<Integer> genFibonacci(int length, int start1, int start2) {
		ArrayList<Integer> fibonacci = new ArrayList<Integer>();
		int numFib = 0;
		int temp;
		
		while (numFib < length) {
			fibonacci.add(start1);
			numFib++;
			temp = start1;
			start1 = start2;
			start2 += temp;
		}
		
		return fibonacci;
	}
}