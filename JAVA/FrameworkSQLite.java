//Program to implement iCRUD

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.sql.ResultSetMetaData;
import org.json.simple.JSONObject;
import org.json.simple.JSONArray;

class SQLite implements iCRUD
{
	Connection connection;
	Statement statement;
	ResultSet resultSet;
	String[] fieldNames;
	JSONObject objJSON;
	JSONArray array;
	public SQLite() throws Exception
	{
		String url = "jdbc:sqlite:D:/Training/JAVA/framework.db";
		Class.forName("org.sqlite.JDBC");
		connection = DriverManager.getConnection(url);
		statement = connection.createStatement();
		fieldNames = getFieldNames();
	}

	public int insertRecord(String query) throws Exception
	{
		return statement.executeUpdate(query);
	}

	public JSONObject readRecords(String query) throws Exception
	{
		return getJSONObject(query);
	}

	public int updateRecord(String query) throws Exception
	{
		return statement.executeUpdate(query);
	}

	public int deleteRecord(String query) throws Exception
	{
		return statement.executeUpdate(query);
	}

	public JSONObject searchRecord(String query) throws Exception
	{
		return getJSONObject(query);
	}

	public JSONObject getJSONObject(String query) throws Exception
	{
		resultSet = statement.executeQuery(query);
		objJSON = new JSONObject();
		array = new JSONArray();
		if(resultSet.next())
		{
			ResultSet rs = statement.executeQuery(query);
			while(rs.next())
			{
				JSONObject record = new JSONObject();
				for(String fieldName : fieldNames)
				{
					record.put(fieldName, resultSet.getString(fieldName));
				}
				array.add(record);
			}
			objJSON.put("MyTable", array);
		}
		return objJSON;
	}

	public String[] getConfigData(String columnName) throws Exception
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

	public String[] getFieldNames() throws Exception
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