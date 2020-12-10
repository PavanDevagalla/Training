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
				System.out.print("Enter database name: ");
				className = scanner.next();
			}
			else
			{
				className = args[0];
			}
			Framework objFramework = new Framework(className);
			objFramework.printMenu();
		}
		catch (Exception objException)
		{
			System.out.println(objException.getMessage());
		}
	}
}