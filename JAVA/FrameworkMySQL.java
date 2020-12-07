//Program to extends Framework

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.sql.ResultSetMetaData;

class MySQL implements iCRUD
{
	Connection connection;
	Statement statement;
	ResultSet resultSet;
	public MySQL() throws Exception
	{
		String url = "jdbc:mysql://165.22.14.77/dbPavan?user=Pavankumar&password=Pavankumar";
		connection = DriverManager.getConnection(url);
		statement = connection.createStatement();
	}

	public int insertRecord(String query) throws SQLException
	{
		return statement.executeUpdate(query);
	}

	public ResultSet readRecords(String query) throws SQLException
	{
		return statement.executeQuery(query);
	}

	public int updateRecord(String query) throws SQLException
	{
		return statement.executeUpdate(query);
	}

	public int deleteRecord(String query) throws SQLException
	{
		return statement.executeUpdate(query);
	}

	public ResultSet searchRecord(String query) throws SQLException
	{
		return statement.executeQuery(query);
	}

	public String[] getConfigData(String columnName) throws SQLException
	{
		String query = "select DataInFile from Config where FileName = '" + columnName + "'";
		resultSet = statement.executeQuery(query);
		String columnData = "";
		if(resultSet.next())
		{
			columnData = resultSet.getString("DataInFile");
		}
		return columnData.split(", ");
	}

	public String[] getFieldNames() throws SQLException
	{
		String query = "select * from MyTable";
		resultSet = statement.executeQuery(query);
		ResultSetMetaData rsMetaData = resultSet.getMetaData();
		String[] fieldNames = new String[rsMetaData.getColumnCount() - 1];
		for(int index = 0; index < fieldNames.length; index++)
		{
			String temp = rsMetaData.getColumnName(index + 1);
			if (temp.equals("Status") != true)
			{
				fieldNames[index] = temp;
			}
		}
		return fieldNames;
	}

}