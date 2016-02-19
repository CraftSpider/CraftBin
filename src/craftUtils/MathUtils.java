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
		System.out.println("Start: " + input);
		input = input * Math.pow(10, -place);
		System.out.println("Pow up: " + input);
		input = Math.round(input);
		System.out.println("Rounded: " + input);
		input = input * Math.pow(10, place);
		System.out.println("Pow down: " + input);
		return input;
	}
	
}
