// Program to test iCRUD interface

import java.util.Scanner;

class MainClass
{
	public static void main(String[] args)
	{
		try
		{
			Scanner scanner = new Scanner(System.in);
			String className = "";
			if (args.length == 0)
			{
				System.out.print("Enter class name: ");
				className = scanner.next();
			}
			else
			{
				className = args[0];
			}
			iCRUD objCRUD = (iCRUD) Class.forName(className).newInstance();
			objCRUD.printMenu();
		}
		catch (Exception objException)
		{
			System.out.println("Invalid class name");
		}
	}
}