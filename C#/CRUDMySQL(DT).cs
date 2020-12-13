// Program to do CRUD operations using DataTable

namespace MySQLLibUsingDT
{
	using System;
	using MySql.Data.MySqlClient;
	using System.Data.Common;
	using System.Data;

	public class CRUDMySQLUsingDT
	{
		MySqlConnection Connection;
		String ConnString;
		MySqlCommand Command;
		public CRUDMySQLUsingDT(String ConnString)
		{
			try
			{
				this.ConnString = ConnString;
				this.Connection = new MySqlConnection(ConnString);
				Connection.Open();
				Console.WriteLine("Connection succesfull");
			}
			catch (Exception error)
			{
				Console.WriteLine(error.Message);
			}
		}

		public int InsertRecord(string Query)
		{
			Command = new MySqlCommand(query, Connection);
			int RowsAffected = Command.ExecuteNonQuery();
			return RowsAffected;
		}

		public DataTable ReadRecords(string Query)
		{
			Command = new MySqlCommand(Query, Connection);
			DataTable Table = new DataTable();
			MySqlDataAdapter Adapter = new MySqlDataAdapter(Command);
			Adapter.Fill(Table);
			return Table;
		}

		public String[] GetFieldNames()
		{
			String Query = "select * from MyTable";
			DataTable Table = ReadRecords(Query);
			String[] FieldNames = new String[Table.Columns.Count - 1];
			for (int Index = 0; Index < Table.Columns.Count; Index++)
			{
				if (!(String.Equals(Table.Columns[Index].ToString(), "Status")))
				{
					FieldNames[Index] = Table.Columns[Index].ToString();
				}
			}
			return FieldNames;
		}
	}
}