package craftUtils;

import java.lang.Math;

/**
 * 
 * @author CraftSpider
 *
 */
public class MathUtils {
	
	public static void main(String[] args) {
		MathUtils math = new MathUtils();
		System.out.println(math.nthRoot(5, 0));
		System.out.println();
	}
	
	/**
	 * 
	 * @param input
	 * @param place
	 * @return double
	 */
	public double roundPlace(double input, int place) {
		input = input * Math.pow(10, -place);
		input = Math.floor(input+.5);
		input = input * Math.pow(10, place);
		return input;
	}
	
	/*public double divFraction() {
		
	}*/
	
	public double sumValues(double[] values) {
		double total = 0;
		
		for (double value : values) {
			total += value;
		}
		
		return total;
	}
	
	public double nthRoot(double input, int root) {
		double oldEstimate = 0;
		
		for(int n = 1; n <= input; n++) {
			if (n*n <= input) {
				oldEstimate = n;
			}
		}
		
		double estimate = input/oldEstimate;
		estimate = (estimate+oldEstimate)/2;
		
		for(int i=0;i<5;i++) {
			oldEstimate = estimate;
			estimate = input/oldEstimate;
			estimate = (estimate+oldEstimate)/2;
		}
		
		return estimate;
	}
	
	public double euclideanNorm(double[] vector, int p) {
		return (Double) null;
	}
}
