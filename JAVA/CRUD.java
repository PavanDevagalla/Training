// Program to create CRUD interface

import org.json.simple.JSONObject;

interface iCRUD
{
	public int insertRecord(String query) throws Exception;
	public JSONObject readRecords(String query) throws Exception;
	public int updateRecord(String query) throws Exception;
	public int deleteRecord(String query) throws Exception;
	public JSONObject searchRecord(String query) throws Exception;
	public String[] getConfigData(String columnName) throws Exception;
	public String[] getFieldNames() throws Exception;
}