// Program to do CRUD operations using DataReader

namespace MySQLLib
{
	using System;
	using MySql.Data.MySqlClient;
	using System.Data.Common;
	using System.Data;

	public class CRUDMySQL
	{
		MySqlConnection Connection;
		String ConnString;
		MySqlCommand Command;
		public CRUDMySQL(String ConnString)
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

		public int InsertRecord(string query)
		{
			Command = new MySqlCommand(query, Connection);
			int RowsAffected = Command.ExecuteNonQuery();
			return RowsAffected;
		}

		public DbDataReader ReadRecords(string query)
		{
			Command = new MySqlCommand(query, Connection);
			DbDataReader Reader = Command.ExecuteReader();
			return Reader;
		}

		public String[] GetFieldNames()
		{
			String Query = "select * from MyTable";
			DbDataReader Reader = ReadRecords(Query);
			String[] FieldNames = new String[Reader.FieldCount  - 1];
			for (int Index = 0; Index < Reader.FieldCount; Index++)
			{
				if (!(String.Equals(Reader.GetName(Index), "Status")))
				{
					FieldNames[Index] = Reader.GetName(Index);
				}
			}
			Reader.Close();
			return FieldNames;
		}
	}
}