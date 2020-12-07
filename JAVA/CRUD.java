// Program to create CRUD interface

import java.sql.SQLException;
import java.sql.ResultSet;

interface iCRUD
{
	public int insertRecord(String query) throws SQLException;
	public ResultSet readRecords(String query) throws SQLException;
	public int updateRecord(String query) throws SQLException;
	public int deleteRecord(String query) throws SQLException;
	public ResultSet searchRecord(String query) throws SQLException;
	public String[] getConfigData(String columnName) throws SQLException;
	public String[] getFieldNames() throws SQLException;
}