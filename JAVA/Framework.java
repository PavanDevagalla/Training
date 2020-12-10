// Program to create a framework program which acts as a mediator

import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.Scanner;
import java.sql.ResultSetMetaData;
import org.json.simple.JSONObject;
import org.json.simple.JSONArray;

class Framework
{
	ResultSet resultSet;
	Scanner scanner = new Scanner(System.in);
	String query;
	String[] fieldNames;
	String[] updatableFieldPositons;
	String[] promptMessages;
	String[] menu;
	int rowsAffected;
	iCRUD objCRUD;

	public Framework(String className) throws Exception
	{
		objCRUD = (iCRUD) Class.forName(className).newInstance();
		fieldNames = objCRUD.getFieldNames();
		updatableFieldPositons = objCRUD.getConfigData("UpdatableFieldPositions");
		promptMessages = objCRUD.getConfigData("PromptMessages");
		menu = objCRUD.getConfigData("Menu");
	}

	public void printMenu() throws Exception
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
							scanner.close();
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

	public void insertRecord() throws Exception
	{
		query = "INSERT INTO MyTable VALUES (";
		for (int index = 0; index < fieldNames.length; index++)
		{
			query += "'" + getInput(fieldNames[index]) + "', ";
		}
		query += "'A')";
		rowsAffected = objCRUD.insertRecord(query);
		if(rowsAffected == 1)
		{
			System.out.println(promptMessages[0]);
		}
		else
		{
			System.out.println("Error while adding details");
		}	
	}

	public void readRecords() throws Exception
	{
		query = "Select * from MyTable where Status = 'A'";
		JSONObject objJSON = objCRUD.readRecords(query);
		int countOfRecords = printRecord(objJSON);
		System.out.println(promptMessages[1] + ": " + countOfRecords);
	}

	public void updateRecord() throws Exception
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
				query = "update MyTable set " + columnName + " = '" + fieldValue + "' where " + fieldNames[0] + " = '" + idToUpdateRecord + "'";
				rowsAffected = objCRUD.updateRecord(query);
				if (rowsAffected == 1)
				{
					System.out.println(columnName + " updated successfully");
				}
				else
				{
					System.out.println("Error while updating " + columnName);
				}
			}
			catch (Exception e)
			{
				System.out.println("Enter valid update choice");
			}
		}
		else
		{
			System.out.println(promptMessages[3]);
		}
	}

	public void deleteRecord() throws Exception
	{
		String idToDeleteRecord = getInput(fieldNames[0]);
		if(checkIdPresentOrNot(idToDeleteRecord))
		{
			query = "update MyTable set Status = 'D' where " + fieldNames[0] + " = '" + idToDeleteRecord + "'";
			rowsAffected = objCRUD.deleteRecord(query);
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

	public void searchRecord() throws Exception
	{
		String idToSearchRecord = getInput(fieldNames[0]);
		query = "Select * from MyTable where Status = 'A' and " + fieldNames[0] + " = '" + idToSearchRecord + "'";
		JSONObject objJSON = objCRUD.searchRecord(query);
		if (objJSON.get("MyTable") != null)
		{
			printRecord(objJSON);
		}
		else
		{
			System.out.println(promptMessages[3]);
		}
	}

	public boolean checkIdPresentOrNot(String id) throws Exception
	{
		boolean isIdPresent = false;
		String query = "Select * from MyTable where Status = 'A' and " + fieldNames[0] + " = '" + id + "'";
		JSONObject objJSON = objCRUD.searchRecord(query);
		if (objJSON.get("MyTable") != null)
		{
			isIdPresent = true;
		}
		return isIdPresent;
	}

	private int printRecord(JSONObject objJSON) throws Exception
	{
		JSONArray objJsonArray = (JSONArray) objJSON.get("MyTable");
		for(int index = 0; index < objJsonArray.size(); index++)
		{
			JSONObject fieldValues = (JSONObject)objJsonArray.get(index);
			for(String fieldName : fieldNames)
			{
				System.out.println(fieldName + ": " + fieldValues.get(fieldName));
			}
			System.out.println("---------------------------------");
		}
		return objJsonArray.size();
	}

	private String getInput(String inputPrompt)
	{
		System.out.print("Enter " + inputPrompt + ": ");
		String input = scanner.nextLine();
		return input;
	}

}