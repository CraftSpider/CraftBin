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
		System.out.println(math.roundPlace(123.456, 0));
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
}
