import java.util.Arrays;

class Updater{
	public static void main(String args[]){
		Parser parse = new Parser();
			
		for(String s : args){
			parse.parseAsCmd(s);	
		}
	}
}

class Parser{
	String[] validCmds = {"addPat", "upEntry"};
	public Parser(){}

	public void parseAsCmd(String cmd){
		String[] cmdAndArgs = cmd.split(":");
		if(Arrays.asList(validCmds).contains(cmdAndArgs[0])){
			String out = "Method: " + cmdAndArgs[0] + "\nArgs: ";
			for(int i = 1; i < cmdAndArgs.length; i++){
				out += cmdAndArgs[i] + ", ";
			}
			out = out.substring(0, out.length() - 2);
			System.out.println(out);
		}
		
	}	
}
