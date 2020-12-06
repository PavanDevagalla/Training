// Program to create CRUD interface

import java.sql.SQLException;

interface iCRUD
{
	public void printMenu() throws SQLException;
	public void insertRecord() throws SQLException;
	public void readRecords() throws SQLException;
	public void updateRecord() throws SQLException;
	public void deleteRecord() throws SQLException;
	public void searchRecord() throws SQLException;
}