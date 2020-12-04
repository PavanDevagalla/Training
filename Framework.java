// Program to do CRUD operations based on user choice.

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.util.Scanner;
import java.sql.ResultSetMetaData;

class MainClass
{
	public static void main(String[] args)
	{
		try
		{
			Framework objFramework = new Framework();
			objFramework.printMenu();
		}
		catch (SQLException objException)
		{
			System.out.println(objException.getMessage());
		}
	}
}

class Framework
{
	Connection connection;
	Statement statement;
	ResultSet resultSet;
	Scanner scanner = new Scanner(System.in);
	String query;
	String[] fieldNames;
	String[] updatableFieldPositons;
	String[] promptMessages;
	String[] menu;
	int rowsAffected;

	public Framework() throws SQLException
	{
		String url = "jdbc:mysql://165.22.14.77/dbPavan?user=Pavankumar&password=Pavankumar";
		connection = DriverManager.getConnection(url);
		statement = connection.createStatement();
		updatableFieldPositons = getConfigData("UpdatableFieldPositions");
		promptMessages = getConfigData("PromptMessages");
		menu = getConfigData("Menu");
		storeFieldNames();
	}

	public void printMenu() throws SQLException
	{
		while (true)
			{
				for (int index = 0; index < menu.length; index++)
				{
					System.out.println((index + 1) + ". " + menu[index]);
				}
				System.out.print("Enter your choice: ");
				String userChoice = scanner.next();
				scanner.nextLine();
				switch (userChoice)
				{
					case "1": insertRecord();
							break;
					case "2": readRecords();
							break;
					case "3": searchRecord();
							break;
					case "4": updateRecord();
							break;
					case "5": deleteRecord();
							break;
					case "6": System.out.print("Do you really want to exit? \nEnter 'y' to confirm or 'n' to continue: ");
							String exitChoice = scanner.next();
							if (exitChoice.toLowerCase().equals("y"))
							{
								System.out.println("Entered exit as choice");
								connection.close();
								System.exit(0);
							}
							else if(exitChoice.toLowerCase().equals("n"))
							{
								continue;
							}
					default: System.out.println("Invalid Choice");
				}
				System.out.println("---------------------------------");
			}
	}

	private void insertRecord() throws SQLException
	{
		query = "INSERT INTO MyTable VALUES(";
		for (int index = 0; index < fieldNames.length; index++)
		{
			query += "'" + getInput(fieldNames[index]) + "', ";
		}
		query += "'A')";
		rowsAffected = statement.executeUpdate(query);
		if(rowsAffected == 1)
		{
			System.out.println(promptMessages[0]);
		}
		else
		{
			System.out.println("Error while adding details");
		}	
	}

	private void readRecords() throws SQLException
	{
		query = "Select * from MyTable where Status = 'A'";
		resultSet = statement.executeQuery(query);
		int countOfRecords = 0;
		while(resultSet.next())
		{
			printRecord(resultSet);
			System.out.println("---------------------------------");
			countOfRecords++;
		}
		System.out.println(promptMessages[1] + ": " + countOfRecords);
	}

	private void updateRecord() throws SQLException
	{
		String idToUpdateRecord = getInput(fieldNames[0]);
		if(checkIdPresentOrNot(idToUpdateRecord))
		{
			int fieldNamesIndex = 0;
			for(int index = 0; index < updatableFieldPositons.length; index++)
			{	
				fieldNamesIndex = Integer.parseInt(updatableFieldPositons[index]);
				System.out.println(index + 1 + ". Update " + fieldNames[fieldNamesIndex]);
			}
			System.out.print("Enter your choice: ");
			try
			{
				int updateChoice = scanner.nextInt();
				scanner.nextLine();
				String columnName = fieldNames[Integer.parseInt(updatableFieldPositons[updateChoice - 1])];
				String fieldValue = getInput(columnName);
				query = "update MyTable set " + columnName + " = '" + fieldValue + "' where AccountNumber = '" + idToUpdateRecord + "'";
				rowsAffected = statement.executeUpdate(query);
				if (rowsAffected == 1)
				{
					System.out.println(columnName + " updated successfully");
				}
				else
				{
					System.out.println("Error while updating " + columnName);
				}
			}
			catch (Exception objException)
			{
				System.out.println("Enter valid update choice");
			}
		}
		else
		{
			System.out.println(promptMessages[3]);
		}
	}

	private void deleteRecord() throws SQLException
	{
		String idToDeleteRecord = getInput(fieldNames[0]);
		if(checkIdPresentOrNot(idToDeleteRecord))
		{
			query = "update MyTable set Status = 'D' where AccountNumber = '" + idToDeleteRecord + "'";
			rowsAffected = statement.executeUpdate(query);
			if (rowsAffected == 1)
			{
				System.out.println(promptMessages[2]);
			}
			else
			{
				System.out.println("Error while deleting, please try again");
			}
		}
		else
		{
			System.out.println(promptMessages[3]);
		}
	}

	private void searchRecord() throws SQLException
	{
		String idToSearchRecord = getInput(fieldNames[0]);
		query = "Select * from MyTable where Status = 'A' and " + fieldNames[0] + " = '" + idToSearchRecord + "'";
		resultSet = statement.executeQuery(query);
		if (resultSet.next())
		{
			printRecord(resultSet);
		}
		else
		{
			System.out.println(promptMessages[3]);
		}
	}

	private boolean checkIdPresentOrNot(String id) throws SQLException
	{
		boolean isIdPresent = false;
		query = "Select " + fieldNames[0] + " from MyTable where Status = 'A' and " + fieldNames[0] + " = '" + id + "'";
		resultSet = statement.executeQuery(query);
		if (resultSet.next())
		{
			isIdPresent = true;
		}
		return isIdPresent;
	}

	private void printRecord(ResultSet resultSet) throws SQLException
	{
		for (int index = 0; index < fieldNames.length; index++)
			{
				System.out.println(fieldNames[index] + ": " + resultSet.getString(fieldNames[index]));
			}
	}

	private String getInput(String fieldName)
	{
		System.out.print("Enter " + fieldName + ": ");
		String input = scanner.nextLine();
		return input;
	}

	private String[] getConfigData(String columnName) throws SQLException
	{
		query = "select DataInFile from Config where FileName = '" + columnName + "'";
		resultSet = statement.executeQuery(query);
		String columnData = "";
		if(resultSet.next())
		{
			columnData = resultSet.getString("DataInFile");
		}
		return columnData.split(", ");
	}

	private void storeFieldNames() throws SQLException
	{
		query = "select * from MyTable";
		resultSet = statement.executeQuery(query);
		ResultSetMetaData rsMetaData = resultSet.getMetaData();
		fieldNames = new String[rsMetaData.getColumnCount() - 1];
		for(int index = 0; index < fieldNames.length; index++)
		{
			String temp = rsMetaData.getColumnName(index + 1);
			if (temp.equals("Status") != true)
			{
				fieldNames[index] = temp;
			}
		}
	}
}