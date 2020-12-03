// Program to do CRUD operations based on user choice.

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.util.Scanner;
import java.sql.ResultSetMetaData;

class Framework
{
	static Connection connection;
	static Statement statement;
	ResultSet resultSet;
	Scanner scanner = new Scanner(System.in);
	String query;
	static String[] fieldNames;
	static String[] updatableFieldPositons;
	static String[] promptMessages;
	public static void main(String args[]) 
	{
		Framework objFramework = new Framework();
		String url = "jdbc:mysql://165.22.14.77/dbPavan?user=Pavankumar&password=Pavankumar";
		try
		{
			connection = DriverManager.getConnection(url);
			statement = objFramework.connection.createStatement();
			updatableFieldPositons = objFramework.getConfigData("UpdatableFieldPositions");
			promptMessages = objFramework.getConfigData("PromptMessages");
			String[] menu = objFramework.getConfigData("Menu");
			objFramework.storeFieldNames();
			while (true)
			{
				for (int index = 0; index < menu.length; index++)
				{
					System.out.println((index + 1) + ". " + menu[index]);
				}
				System.out.print("Enter your choice: ");
				String userChoice = objFramework.scanner.next();
				switch (userChoice)
				{
					case "1": objFramework.insertRecord();
							break;
					case "2": objFramework.readRecords();
							break;
					case "3": objFramework.searchRecord();
							break;
					case "4": objFramework.updateRecord();
							break;
					case "5": objFramework.deleteRecord();
							break;
					case "6": System.out.println("Do you really want to exit? ");
							String exitChoice = objFramework.getInput("'y' to confirm or 'n' to continue");
							exitChoice = exitChoice.toLowerCase();
							if (exitChoice.charAt(0) == 'y')
							{
								System.out.println("Entered exit as choice");
								objFramework.connection.close();
								System.exit(0);
							}
					default: System.out.println("Invalid Choice");
				}
				System.out.println("---------------------------------");
			}
		}
		catch (SQLException objException)
		{
			System.out.println(objException.getMessage());
		}
	}

	public void insertRecord() throws SQLException
	{
		query = "INSERT INTO MyTable VALUES(";
		for (int index = 0; index < fieldNames.length; index++)
		{
			query += "'" + getInput(fieldNames[index]) + "', ";
		}
		query += "'A')";
		statement.executeUpdate(query);	
		System.out.println(promptMessages[0]);
	}

	public void readRecords() throws SQLException
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

	public void updateRecord() throws SQLException
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
				String columnName = fieldNames[Integer.parseInt(updatableFieldPositons[updateChoice - 1])];
				String fieldValue = getInput(columnName);
				query = "update MyTable set " + columnName + " = '" + fieldValue + "' where AccountNumber = '" + idToUpdateRecord + "'";
				int rowsAffected = statement.executeUpdate(query);
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

	public void deleteRecord() throws SQLException
	{
		String idToDeleteRecord = getInput(fieldNames[0]);
		query = "update MyTable set Status = 'D' where Status = 'A' and AccountNumber = '" + idToDeleteRecord + "'";
		int rowsAffected = statement.executeUpdate(query);
		if (rowsAffected == 1)
		{
			System.out.println(promptMessages[2]);
		}
		else
		{
			System.out.println(promptMessages[3]);
		}
	}

	public void searchRecord() throws SQLException
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

	public boolean checkIdPresentOrNot(String id) throws SQLException
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

	public void printRecord(ResultSet resultSet) throws SQLException
	{
		for (int index = 0; index < fieldNames.length; index++)
			{
				System.out.println(fieldNames[index] + ": " + resultSet.getString(fieldNames[index]));
			}
	}

	public String getInput(String fieldName)
	{
		System.out.print("Enter " + fieldName + ": ");
		String input = scanner.next();
		return input;
	}

	public String[] getConfigData(String columnName) throws SQLException
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

	public void storeFieldNames() throws SQLException
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